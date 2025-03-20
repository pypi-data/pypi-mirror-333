/* Fast image metric. */

#define PY_SSIZE_T_CLEAN
#include <complex.h>
#include <math.h>
#include <numpy/arrayobject.h>
#include <omp.h>
#include <Python.h>
#include <stdlib.h>
#include "cutcutcodec/core/opti/parallel/threading.h"
#include "cutcutcodec/utils.h"


int compute_psnr_float32(double* psnr, PyArrayObject* im1, PyArrayObject* im2, PyArrayObject* weights) {
  /* Compute the mse for each channel, return the ponderated average. */
  float mse = 0.0;  // we can not declare *mse in reduction
  #pragma omp parallel for simd schedule(static) collapse(2) reduction(+:mse)
  for ( npy_intp i = 0; i < PyArray_DIM(im1, 0); ++i ) {
    for ( npy_intp j = 0; j < PyArray_DIM(im1, 1); ++j ) {
      for ( npy_intp k = 0; k < PyArray_DIM(im1, 2); ++k ) {
        float diff = *(float *)PyArray_GETPTR3(im1, i, j, k) - *(float *)PyArray_GETPTR3(im2, i, j, k);
        diff *= diff;
        diff *= (float)(  // we can't factorise because omp doesn't support array reduction
          *(double *)PyArray_GETPTR1(weights, k)
        );
        mse += diff;  // critical for thread safe
      }
    }
  }
  mse /= (float)PyArray_DIM(im1, 0) * (float)PyArray_DIM(im1, 1);
  *psnr = mse > 1.0e-10 ? -10.0*log10((double)mse) : 100.0;
  return EXIT_SUCCESS;
}


int compute_psnr_float64(double* psnr, PyArrayObject* im1, PyArrayObject* im2, PyArrayObject* weights) {
  /* Compute the mse for each channel, return the ponderated average. */
  double mse = 0.0;  // we can not declare *mse in reduction
  #pragma omp parallel for schedule(static) collapse(2) reduction(+:mse)
  for ( npy_intp i = 0; i < PyArray_DIM(im1, 0); ++i ) {
    for ( npy_intp j = 0; j < PyArray_DIM(im1, 1); ++j ) {
      for ( npy_intp k = 0; k < PyArray_DIM(im1, 2); ++k ) {
        double diff = *(double *)PyArray_GETPTR3(im1, i, j, k) - *(double *)PyArray_GETPTR3(im2, i, j, k);
        diff *= diff;
        diff *= *(double *)PyArray_GETPTR1(weights, k);  // we can't factorise because omp doesn't support array reduction
        mse += diff;  // critical for thread safe
      }
    }
  }
  mse /= (double)PyArray_DIM(im1, 0) * (double)PyArray_DIM(im1, 1);
  *psnr = mse > 1.0e-10 ? -10.0*log10(mse) : 100.0;
  return EXIT_SUCCESS;
}


PyArrayObject* gauss_kernel(npy_intp radius, double sigma) {
  /* Create a gaussian kernel. */
  npy_intp shape[2] = {2*radius + 1, 2*radius + 1};
  PyArrayObject* gauss2d;
  double* gauss1d;
  double sum, buff;
  // verifiactions
  if ( radius < 1 ) {
    PyErr_SetString(PyExc_ValueError, "the gaussian radius must be >= 1");
    return NULL;
  }
  if ( sigma <= 0.0 ) {
    PyErr_SetString(PyExc_ValueError, "the variance has to be strictely positive");
    return NULL;
  }
  // allocations
  gauss1d = (double *)malloc((2 * radius + 1) * sizeof(double));
  if ( gauss1d == NULL ) {
    PyErr_NoMemory();
    return NULL;
  }
  gauss2d = (PyArrayObject *)PyArray_EMPTY(2, shape, NPY_DOUBLE, 0);
  if ( gauss2d == NULL ) {
    free(gauss1d);
    PyErr_NoMemory();
    return NULL;
  }

  // compute gaussian
  Py_BEGIN_ALLOW_THREADS
  buff = -1.0 / (2.0 * sigma * sigma);
  #pragma omp simd
  for ( npy_intp i = 1; i < radius + 1; ++i ) {  // compute gaussian 1d
    gauss1d[radius-i] = gauss1d[radius+i] = exp((double)(i*i) * buff);
  }
  gauss1d[radius] = 1.0;
  sum = 0.0;  // compute gaussian 2d
  #pragma omp simd collapse(2) reduction(+:sum)
  for ( npy_intp i = 0; i < shape[0]; ++i ) {
    for ( npy_intp j = 0; j < shape[0]; ++j ) {
      buff = gauss1d[i] * gauss1d[j];
      *(double *)PyArray_GETPTR2(gauss2d, i, j) = buff;
      sum += buff;
    }
  }
  sum = 1.0 / sum;  // normalise
  #pragma omp simd collapse(2)
  for ( npy_intp i = 0; i < shape[0]; ++i ) {
    for ( npy_intp j = 0; j < shape[0]; ++j ) {
      *(double *)PyArray_GETPTR2(gauss2d, i, j) *= sum;
    }
  }
  free(gauss1d);
  Py_END_ALLOW_THREADS
  return gauss2d;
}


int compute_ssim_float32(
  double* ssim,
  PyArrayObject* im1,  // float32
  PyArrayObject* im2,  // float32
  PyArrayObject* weights,  // double
  PyArrayObject* kernel,  // double
  double data_range
) {
  npy_intp radius[2] = {PyArray_DIM(kernel, 0) / 2, PyArray_DIM(kernel, 1) / 2};  // rigorously (s - 1) / 2
  double local_ssim = 0.0;
  float c1 = 0.01 * (float)data_range, c2 = 0.03 * (float)data_range;
  c1 *= c1, c2 *= c2;
  // iterate on the patch center position
  #pragma omp parallel for schedule(static) collapse(2) reduction(+:local_ssim)
  for ( npy_intp i0 = radius[0]; i0 < PyArray_DIM(im1, 0)-radius[0]; ++i0 ) {
  for ( npy_intp j0 = radius[1]; j0 < PyArray_DIM(im1, 1)-radius[1]; ++j0 ) {
  #pragma omp simd reduction(+:local_ssim)
  for ( npy_intp k = 0; k < PyArray_DIM(im1, 2); ++k ) {  // repeat on each channel
    // iterate within each patch
    npy_intp shift[2] = {i0-radius[0], j0-radius[1]};
    float mu1 = 0.0, mu2 = 0.0, s11 = 0.0, s22 = 0.0, s12 = 0.0;
    float patch_ssim, m11, m22, m12;
    for ( npy_intp i = 0; i < PyArray_DIM(kernel, 0); ++i ) {
    for ( npy_intp j = 0; j < PyArray_DIM(kernel, 1); ++j ) {
      float x1, x2, x1w, x2w, weight;
      weight = (float)(*(double *)PyArray_GETPTR2(kernel, i, j));
      x1 = *(float *)PyArray_GETPTR3(im1, i+shift[0], j+shift[1], k),
      x2 = *(float *)PyArray_GETPTR3(im2, i+shift[0], j+shift[1], k);
      x1w = x1 * weight, x2w = x2 * weight;
      mu1 += x1w, mu2 += x2w;
      s11 += x1 * x1w, s22 += x2 * x2w, s12 += x1 * x2w;
    }}
    m11 = mu1 * mu1, m22 = mu2 * mu2, m12 = mu1 * mu2;
    s11 -= m11, s22 -= m22, s12 -= m12;
    patch_ssim = (  // the ssim of the patch
      (2.0 * m12 + c1) * (2.0 * s12 + c2)
    ) / (
      (m11 + m22 + c1) * (s11 + s22 + c2)
    );
    patch_ssim *= (float)(*(double *)PyArray_GETPTR1(weights, k));  // normalise by the channel weight
    local_ssim += (double)patch_ssim;
  }}}
  local_ssim /= (double)((PyArray_DIM(im1, 0) - 2*radius[0]) * (PyArray_DIM(im1, 1) - 2*radius[1]));
  *ssim = local_ssim;
  return EXIT_SUCCESS;
}


int compute_ssim_float64(
  double* ssim,
  PyArrayObject* im1,  // double
  PyArrayObject* im2,  // double
  PyArrayObject* weights,  // double
  PyArrayObject* kernel,  // double
  double data_range
) {
  npy_intp radius[2] = {PyArray_DIM(kernel, 0) / 2, PyArray_DIM(kernel, 1) / 2};  // rigorously (s - 1) / 2
  double local_ssim = 0.0;
  double c1 = 0.01 * data_range, c2 = 0.03 * data_range;
  c1 *= c1, c2 *= c2;
  // iterate on the patch center position
  #pragma omp parallel for schedule(static) collapse(2) reduction(+:local_ssim)
  for ( npy_intp i0 = radius[0]; i0 < PyArray_DIM(im1, 0)-radius[0]; ++i0 ) {
  for ( npy_intp j0 = radius[1]; j0 < PyArray_DIM(im1, 1)-radius[1]; ++j0 ) {
  #pragma omp simd reduction(+:local_ssim)
  for ( npy_intp k = 0; k < PyArray_DIM(im1, 2); ++k ) {  // repeat on each channel
    // iterate within each patch
    npy_intp shift[2] = {i0-radius[0], j0-radius[1]};
    double mu1 = 0.0, mu2 = 0.0, s11 = 0.0, s22 = 0.0, s12 = 0.0;
    float patch_ssim, m11, m22, m12, weight;
    for ( npy_intp i = 0; i < PyArray_DIM(kernel, 0); ++i ) {
    for ( npy_intp j = 0; j < PyArray_DIM(kernel, 1); ++j ) {
      float x1, x2, x1w, x2w;
      weight = *(double *)PyArray_GETPTR2(kernel, i, j);
      x1 = *(double *)PyArray_GETPTR3(im1, i+shift[0], j+shift[1], k),
      x2 = *(double *)PyArray_GETPTR3(im2, i+shift[0], j+shift[1], k);
      x1w = x1 * weight, x2w = x2 * weight;
      mu1 += x1w, mu2 += x2w;
      s11 += x1 * x1w, s22 += x2 * x2w, s12 += x1 * x2w;
    }}
    m11 = mu1 * mu1, m22 = mu2 * mu2, m12 = mu1 * mu2;
    s11 -= m11, s22 -= m22, s12 -= m12;
    patch_ssim = (  // the ssim of the patch
      (2.0 * mu1 * mu2 + c1) * (2.0 * s12 + c2)
    ) / (
      (mu1 * mu1 + mu2 * mu2 + c1) * (s11 + s22 + c2)
    );
    patch_ssim *= *(double *)PyArray_GETPTR1(weights, k);
    local_ssim += patch_ssim;
  }}}
  local_ssim /= (double)((PyArray_DIM(im1, 0) - 2*radius[0]) * (PyArray_DIM(im1, 1) - 2*radius[1]));
  *ssim = local_ssim;
  return EXIT_SUCCESS;
}


static PyObject* py_ssim(PyObject* Py_UNUSED(self), PyObject* args, PyObject* kwargs) {
  // declaration
  static char *kwlist[] = {"im1", "im2", "data_range", "weights", "sigma", "threads", NULL};
  PyArrayObject *im1, *im2, *weights = NULL;
  double ssim, data_range = 1.0, sigma = 1.5;
  long int threads = 0;
  int error = EXIT_SUCCESS;

  // parse and check
  if ( !PyArg_ParseTupleAndKeywords(
    args, kwargs, "O!O!|dO&d$l", kwlist,
    &PyArray_Type, &im1, &PyArray_Type, &im2, &data_range, &parse_double_array, &weights, &sigma, &threads
    )
  ) {
    return NULL;
  }
  if ( PyArray_NDIM(im1) != 3 ) {
    PyErr_SetString(PyExc_ValueError, "'im1' requires 3 dimensions");
    return NULL;
  }
  if ( PyArray_NDIM(im2) != 3 ) {
    PyErr_SetString(PyExc_ValueError, "'im2' requires 3 dimensions");
    return NULL;
  }
  if ( PyArray_DIM(im1, 0) != PyArray_DIM(im2, 0) ) {
    PyErr_SetString(PyExc_ValueError, "'im1' and 'im2' must have the same height");
    return NULL;
  }
  if ( PyArray_DIM(im1, 1) != PyArray_DIM(im2, 1) ) {
    PyErr_SetString(PyExc_ValueError, "'im1' and 'im2' must have the same width");
    return NULL;
  }
  if ( PyArray_DIM(im1, 2) != PyArray_DIM(im2, 2) ) {
    PyErr_SetString(PyExc_ValueError, "'im1' and 'im2' must have the same channels");
    return NULL;
  }
  if ( PyArray_TYPE(im1) != PyArray_TYPE(im2) ) {
    PyErr_SetString(PyExc_TypeError, "'im1' and 'im2' are not the same type");
    return NULL;
  }
  if ( data_range <= 0.0 ) {
    PyErr_SetString(PyExc_ValueError, "'data_range' must be > 0");
    return NULL;
  }

  // default values
  if ( weights == NULL ) {
    npy_intp dims[1] = {PyArray_DIM(im1, 2)};
    weights = (PyArrayObject *)PyArray_EMPTY(1, dims, NPY_DOUBLE, 0);
    if ( weights == NULL ) {
      PyErr_NoMemory();
      return NULL;
    }
    #pragma omp simd
    for ( npy_intp i = 0; i < PyArray_DIM(weights, 0); ++i ) {
      *(double *)PyArray_GETPTR1(weights, i) = 1.0;
    }
  } else if ( PyArray_DIM(weights, 0) != PyArray_DIM(im1, 2) ) {
    PyErr_SetString(PyExc_ValueError, "the length of weights must match the number of channels");
    return NULL;
  }

  // set omp nbr threads
  set_num_threads(threads);

  // normalise weights
  ssim = 0.0;
  for ( npy_intp i = 0; i < PyArray_DIM(weights, 0); ++i ) {
    ssim += *(double *)PyArray_GETPTR1(weights, i);
  }
  for ( npy_intp i = 0; i < PyArray_DIM(weights, 0); ++i ) {
    *(double *)PyArray_GETPTR1(weights, i) /= ssim;
  }

  // get haussian kernel
  npy_intp radius = (npy_intp)(3.5 * sigma + 0.5);
  PyArrayObject* kernel = gauss_kernel(radius, sigma);  // radius sigma
  if ( kernel == NULL ) {
    Py_DECREF(weights);
    return NULL;
  }
  if ( PyArray_DIM(kernel, 0) > PyArray_DIM(im1, 0) || PyArray_DIM(kernel, 1) > PyArray_DIM(im1, 1) ) {
    PyErr_SetString(PyExc_ValueError, "sigma is to big for the image size");
    Py_DECREF(weights);
    Py_DECREF(kernel);
    return NULL;
  }

  // compute ssim
  switch ( PyArray_TYPE(im1) ) {
    case NPY_FLOAT32:
      Py_BEGIN_ALLOW_THREADS
      error = compute_ssim_float32(&ssim, im1, im2, weights, kernel, data_range);
      Py_END_ALLOW_THREADS
      break;
    case NPY_DOUBLE:
      Py_BEGIN_ALLOW_THREADS
      error = compute_ssim_float64(&ssim, im1, im2, weights, kernel, data_range);
      Py_END_ALLOW_THREADS
      break;
    default:
      PyErr_SetString(PyExc_TypeError, "only the types float64 are accepted");
      error = EXIT_FAILURE;
  }
  Py_DECREF(weights);
  Py_DECREF(kernel);

  // return and manage error
  if ( error == EXIT_FAILURE ) {
    return NULL;
  }
  return Py_BuildValue("d", ssim);
}


static PyObject* py_psnr(PyObject* Py_UNUSED(self), PyObject* args, PyObject* kwargs) {
  // declaration
  static char *kwlist[] = {"im1", "im2", "weights", "threads", NULL};
  PyArrayObject *im1, *im2, *weights = NULL;
  double psnr;
  long int threads = 0;
  int error = EXIT_SUCCESS;

  // parse and check
  if ( !PyArg_ParseTupleAndKeywords(
    args, kwargs, "O!O!|O&$l", kwlist,
    &PyArray_Type, &im1, &PyArray_Type, &im2, &parse_double_array, &weights, &threads
    )
  ) {
    return NULL;
  }
  if ( PyArray_NDIM(im1) != 3 ) {
    PyErr_SetString(PyExc_ValueError, "'im1' requires 3 dimensions");
    return NULL;
  }
  if ( PyArray_NDIM(im2) != 3 ) {
    PyErr_SetString(PyExc_ValueError, "'im2' requires 3 dimensions");
    return NULL;
  }
  if ( PyArray_DIM(im1, 0) != PyArray_DIM(im2, 0) ) {
    PyErr_SetString(PyExc_ValueError, "'im1' and 'im2' must have the same height");
    return NULL;
  }
  if ( PyArray_DIM(im1, 1) != PyArray_DIM(im2, 1) ) {
    PyErr_SetString(PyExc_ValueError, "'im1' and 'im2' must have the same width");
    return NULL;
  }
  if ( PyArray_DIM(im1, 2) != PyArray_DIM(im2, 2) ) {
    PyErr_SetString(PyExc_ValueError, "'im1' and 'im2' must have the same channels");
    return NULL;
  }
  if ( PyArray_TYPE(im1) != PyArray_TYPE(im2) ) {
    PyErr_SetString(PyExc_TypeError, "'im1' and 'im2' are not the same type");
    return NULL;
  }

  // default values
  if ( weights == NULL ) {
    npy_intp dims[1] = {PyArray_DIM(im1, 2)};
    weights = (PyArrayObject *)PyArray_EMPTY(1, dims, NPY_DOUBLE, 0);
    if ( weights == NULL ) {
      PyErr_NoMemory();
      return NULL;
    }
    #pragma omp simd
    for ( npy_intp i = 0; i < PyArray_DIM(weights, 0); ++i ) {
      *(double *)PyArray_GETPTR1(weights, i) = 1.0;
    }
  }

  // set omp nbr threads
  set_num_threads(threads);

  // normalise weights
  psnr = 0.0;
  for ( npy_intp i = 0; i < PyArray_DIM(weights, 0); ++i ) {
    psnr += *(double *)PyArray_GETPTR1(weights, i);
  }
  for ( npy_intp i = 0; i < PyArray_DIM(weights, 0); ++i ) {
    *(double *)PyArray_GETPTR1(weights, i) /= psnr;
  }

  // compute psnr
  switch ( PyArray_TYPE(im1) ) {
    case NPY_FLOAT32:
      Py_BEGIN_ALLOW_THREADS
      error = compute_psnr_float32(&psnr, im1, im2, weights);
      Py_END_ALLOW_THREADS
      break;
    case NPY_DOUBLE:
      Py_BEGIN_ALLOW_THREADS
      error = compute_psnr_float64(&psnr, im1, im2, weights);
      Py_END_ALLOW_THREADS
      break;
    default:
      PyErr_SetString(PyExc_TypeError, "only the types float32 and float64 are accepted");
      error = EXIT_FAILURE;
  }
  Py_DECREF(weights);

  // return and manage error
  if ( error == EXIT_FAILURE ) {
    return NULL;
  }
  return Py_BuildValue("d", psnr);
}


static PyMethodDef metricMethods[] = {
  {
    "psnr", (PyCFunction)py_psnr, METH_VARARGS | METH_KEYWORDS,
    R"(Compute the peak signal to noise ratio of 2 images in C language.

    This function is nearly equivalent to:

    .. code-block:: python

        import math
        import numpy as np

        def psnr(im1: np.ndarray, im2: np.ndarray, weights = None) -> float:
            if weights is None:
                weights = [1.0 for _ in range(im1.shape[2])]
            layers_mse = ((im1 - im2)**2).mean(axis=(0, 1)).tolist()
            tot = sum(weights)
            mse = sum(l*w/tot for w, l in zip(weights, layers_mse))
            return -10.0*math.log10(mse) if mse > 1e-10 else 100.0

    Parameters
    ----------
    im1, im2 : np.ndarray
        The 2 images to be compared, of shape (height, width, channels).
        Supported types are float32 and float64.
    threads : int, optional
        Defines the number of threads.
        The value -1 means that the function uses as many calculation threads as there are cores.
        The default value (0) allows the same behavior as (-1) if the function
        is called in the main thread, otherwise (1) to avoid nested threads.
        Any other positive value corresponds to the number of threads used.

    Returns
    -------
    psnr : float
        The global peak signal to noise ratio,
        as a ponderation of the mean square error of each channel.

    Examples
    --------
    >>> import numpy as np
    >>> from cutcutcodec.core.signal.metric import psnr
    >>> im1 = np.random.random((1080, 1920, 3))
    >>> im2 = 0.8*im1 + 0.2*np.random.random((1080, 1920, 3))
    >>> round(psnr(im1, im2))
    22
    >>>
    )"
  },
  {
    "ssim", (PyCFunction)py_ssim, METH_VARARGS | METH_KEYWORDS,
    R"(Compute the Structural similarity index measure of 2 images in C language.

    This fonction is nearly equivalent to these functions:

    .. code-block:: python

        import cv2
        import numpy as np

        def ssim(
          im1: np.ndarray, im2: np.ndarray, data_range : float = 1.0, weights = None, sigma: float = 1.5
        ) -> float:
            # get gaussian window
            r = int(3.5 * sigma + 0.5)  # same as skimage.metrics.structural_similarity
            gauss = np.exp(-(np.arange(-r, r+1)**2) / (2.0 * sigma**2))
            gauss_i, gauss_j = np.meshgrid(gauss, gauss, indexing="ij")
            gauss = gauss_i * gauss_j
            gauss /= gauss.sum()
            # compute statistics for all patches
            mu1 = cv2.filter2D(im1, ddepth=-1, kernel=gauss)
            mu2 = cv2.filter2D(im2, ddepth=-1, kernel=gauss)
            mu11, mu22, mu12 = mu1 * mu1, mu2 * mu2, mu1 * mu2
            s11 = cv2.filter2D(im1*im1, ddepth=-1, kernel=gauss) - mu11
            s22 = cv2.filter2D(im2*im2, ddepth=-1, kernel=gauss) - mu22
            s12 = cv2.filter2D(im1*im2, ddepth=-1, kernel=gauss) - mu12
            # crop patches
            mu11, mu22, mu12 = mu11[r:-r, r:-r], mu22[r:-r, r:-r], mu12[r:-r, r:-r]
            s11, s22, s12 = s11[r:-r, r:-r], s22[r:-r, r:-r], s12[r:-r, r:-r]
            # ssim formula
            c1, c2 = (0.01 * data_range)**2, (0.03 * data_range)**2
            ssim = ((2.0*mu12 + c1) * (2.0*s12 + c2)) / ((mu11 + mu22 + c1) * (s11 + s22 + c2))
            # average
            if weights is None:
              weights = [1.0 for _ in range(im1.shape[2])]
            weights = np.asarray(weights, dtype=im1.dtype)
            return float((ssim.mean(axis=(0, 1)) * weights).sum() / weights.sum())

    Or directly using scikit-image:

    .. code-block:: python

        from skimage.metrics import structural_similarity

        def ssim(
          im1: np.ndarray, im2: np.ndarray, data_range : float = 1.0, weights = None, sigma: float = 1.5
        ) -> float:
          if weights is None:
              weights = [1.0 for _ in range(im1.shape[2])]
          ssim = 0.0
          for i in range(im1.shape[2]):
              ssim += structural_similarity(
                  im1[:, :, i], im2[:, :, i], data_range=data_range, sigma=sigma, gaussian_weights=True
              ) * weights[i]
          return ssim / sum(weights)

    Parameters
    ----------
    im1, im2 : np.ndarray
        The 2 images to be compared, of shape (height, width, channels).
        Supported types are float32 and float64.
    data_range : float, default=1.0
        The data range of the input image (difference between maximum and minimum possible values).
    weights : iterable[float], optional
        The relative weight of each channel. By default, all channels have the same weight.
    sigma : float, default=1.5
        The standard deviation of the gaussian.
    threads : int, optional
        Defines the number of threads.
        The value -1 means that the function uses as many calculation threads as there are cores.
        The default value (0) allows the same behavior as (-1) if the function
        is called in the main thread, otherwise (1) to avoid nested threads.
        Any other positive value corresponds to the number of threads used.

    Returns
    -------
    ssim : float
        The ponderated structural similarity index measure of each layers.

    Examples
    --------
    >>> import numpy as np
    >>> from cutcutcodec.core.signal.metric import ssim
    >>> im1 = np.random.random((1080, 1920, 3))
    >>> im2 = 0.8*im1 + 0.2*np.random.random((1080, 1920, 3))
    >>> round(ssim(im1, im2), 2)
    0.95
    >>>
    )"
  },
  {NULL, NULL, 0, NULL}
};


static struct PyModuleDef metric = {
  PyModuleDef_HEAD_INIT,
  "metric",
  "This module, implemented in C, offers functions for image metric calculation.",
  -1,
  metricMethods
};


PyMODINIT_FUNC PyInit_metric(void)
{
  import_array();
  if ( PyErr_Occurred() ) {
    return NULL;
  }
  return PyModule_Create(&metric);
}

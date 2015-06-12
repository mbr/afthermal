cimport numpy as np
cimport cython

ctypedef np.uint8_t px_t;

cdef inline void add_err(px_t *img, int rows, int cols, int y, int x, px_t err, int frac):
  if x < 0 or y < 0 or x >= cols or y >= rows:
    return

  cdef px_t newval, val = img[y * cols + x]
  if err < 0:
     newval = max(val + err * frac / 16, 0)
  else:
      newval = min(val + err * frac / 16, 255)
  img[y * cols + x] = newval


# cython: profile=True
@cython.boundscheck(False)
cpdef floydsteinberg(np.ndarray[px_t, ndim=2] img):
    # image should be a grayscale image
    cdef int rows = img.shape[0]
    cdef int cols = img.shape[1]
    cdef px_t orig, npx, err
    cdef int x, y
    cdef px_t* data = <px_t*> img.data

    for y in range(rows):
        for x in range(cols):
            orig = data[y * cols + x]
            npx = 255 if data[y * cols + x] > 127 else 0
            data[y * cols + x] = npx
            err = orig - npx

            add_err(data, rows, cols, y, x+1, err, 7)
            add_err(data, rows, cols, y+1, x-1, err, 3)
            add_err(data, rows, cols, y+1, x, err, 5)
            add_err(data, rows, cols, y+1, x+1, err, 1)

    return img

cimport numpy as np
cimport cython

# cython: profile=True
@cython.boundscheck(False)
cpdef floydsteinberg(np.ndarray[unsigned char, ndim=2] img):
    # image should be a grayscale image

    cdef np.int16_t [:, :] img2
    img2 = img.astype('int16')

    cdef int rows = img2.shape[0]
    cdef int cols = img2.shape[1]
    cdef int orig, npx, err
    cdef int x, y

    for y in range(rows):
        for x in range(cols):
            orig = img2[y,x]
            npx = 255 if img2[y,x] > 127 else 0
            img2[y,x] = npx
            err = orig - npx

            if x < cols - 1:
                img2[y,x+1] += err * 7 / 16

            if y < rows - 1:
                if x > 0:
                    img2[y+1,x-1] +=  err * 3 / 16

                img2[y+1,x-1] += err * 5 / 16
                if x < cols - 1:
                    img2[y+1,x+1] += err * 1 / 16

    return img2

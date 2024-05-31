#@numba.jit(nopython=True,parallel=True)
import numpy as np
def DN_STD(y):
    #y must be numpy array
    # if not isinstance(y,np.ndarray):
    #     y = np.asarray(y)
    return(np.std(y))

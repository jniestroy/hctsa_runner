import numpy as np
def DN_ObsCount(y):
    return np.count_nonzero(~np.isnan(y))

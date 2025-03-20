import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, cophenet


class NMF:
    """
    Non-negative Matrix Factorization class accounting for NaN values.

    This class performs Non-negative Matrix Factorization (NMF) on a 2D numpy array, handling
    missing values (NaN) appropriately. It decomposes the input matrix into two non-negative
    matrices, W and H, where W represents the basis components and H represents the coefficients.

    Args:
        num_components (int, optional): Number of components to extract. Default is 2.
        num_iter (int, optional): Number of iterations for computing NMF statistics. Default is 100.
        nmf_iter (int, optional): Number of iterations for the NMF algorithm. Default is 1000.

    Attributes:
        correlation_coefficient (float): The correlation coefficient computed during factorization.
        consensus_matrix (np.ndarray): A consensus matrix of shape (num_input, num_input) summarizing
                                the factorization results.

    Methods:
        fit(x, init_w=None, init_h=None):
            Fit the NMF model to the input data.
            Args:
                x (np.ndarray): A 2D array of data to be factorized.
                init_w (np.ndarray, optional): Initial non-negative W matrix of shape 
                                            (num_input, num_components). Default is None.
                init_h (np.ndarray, optional): Initial non-negative H matrix of shape 
                                            (num_components, num_features * 2). Default is None.
            Raises:
                TypeError: If `x`, `init_w`, or `init_h` is not a numpy.ndarray.

    Raises:
        TypeError: If `x` is not a numpy.ndarray or pandas DataFrame.
        TypeError: If `init_w` or `init_h` is not a numpy.ndarray.
        ValueError: If `init_w` or `init_h` is not of the correct shape.

    Example:
        >>> import numpy as np
        >>> x = np.array([[1, 2], [3, 4], [5, 6]])
        >>> nmf = NMF(num_components=2, num_iter=50, nmf_iter=500)
        >>> nmf.fit(x)
        >>> nmf.correlation_coefficient
        0.95
        >>> nmf.consensus_matrix.shape
        (3, 3)
    """
    def __init__(self, num_components=2,
                       num_iter=100,
                       nmf_iter=1000):
        self.num_components = num_components
        self.num_iter = num_iter
        self.nmf_iter = nmf_iter
        self.correlation_coefficient = None
        self.consensus_matrix = None

    def fit(self, x, init_w=None, init_h=None):
        if not isinstance(x, (np.ndarray, pd.DataFrame)):
            raise TypeError(f"x must be np.ndarray or pd.DataFrame not {type(x)}.")
        if isinstance(x, pd.DataFrame):
            x = x.values

        if init_w is not None:
            if not isinstance(init_w, np.ndarray):
                raise TypeError(f"init_w must be np.ndarray not {type(init_w)}.")
            if init_w.shape != (x.shape[0], self.num_components):
                raise ValueError(f"init_w must be of shape ({x.shape[0]}, {self.num_components}) not {init_w.shape}.")
        if init_h is not None:
            if not isinstance(init_h, np.ndarray):
                raise TypeError(f"init_h must be np.ndarray not {type(init_h)}.")
            if init_h.shape != (self.num_components, x.shape[1]*2):
                raise ValueError(f"init_h must be of shape ({self.num_components}, {x.shape[1]*2}) not {init_h.shape}.")

        x = np.hstack([x, -x])

        x[x < 0] = 0
        mx, _ = x.shape
        c = np.zeros([mx, mx])

        for _ in range(self.num_iter):
            wt, _ = self._nmf(x, init_w, init_h)
            idx = np.argmax(wt, axis=1)
            ct = (idx[:, None] == idx[None, :]).astype(int)
            c += ct

        consensus_matrix = c / self.num_iter
        y = pdist(consensus_matrix)
        z = linkage(consensus_matrix, method="average")
        coph_corr, coph_dists = cophenet(z, y)
        self.correlation_coefficient = coph_corr
        self.consensus_matrix = consensus_matrix


    def _nmf(self, x, init_w, init_h):
        mx, nx = x.shape

        if init_w is not None:
            w = init_w.astype("float64")
        else:
            w = np.random.uniform(size=[mx, self.num_components])
            w = w.astype("float64")

        if init_h is not None:
            h = init_h.astype("float64")
        else:
            h = np.random.uniform(size=[self.num_components, nx])
            h = h.astype("float64")
        
        eps =  np.finfo("float64").eps

        has_nan = np.isnan(x).any()
        if has_nan:
            nan_idx = np.isnan(x)
            x = np.nan_to_num(x)
            mul1 = mx / np.sum(~nan_idx, 0)[:, np.newaxis]
            mul2 = nx / np.sum(~nan_idx, 1)[np.newaxis, :]
        else:
            mul1 = np.zeros([1, 1])
            mul2 = np.zeros([1, 1])

        for _ in range(self.nmf_iter):
            if has_nan:
                h = h * np.sqrt((w.T @ x * mul1.T + eps) / (w.T @ w @ h + eps))
                w = w * np.sqrt((x @ h.T * mul2.T + eps) / ((w @ h) @ (x.T @ w * mul1) + eps))
                w = w / np.sum(w, axis=0)
            else:
                h = h * np.sqrt((w.T @ x + eps) / (w.T @ w @ h + eps))
                w = w * np.sqrt((x @ h.T + eps) / ((w @ h) @ (x.T @ w) + eps))
                w = w / np.sum(w, axis=0)

        return w, h


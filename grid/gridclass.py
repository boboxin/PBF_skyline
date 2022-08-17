from cgi import test
from ctypes import sizeof
import itertools
from turtle import width

import attr
import numpy as np
import validators as vlds

from dataclass import Data,batchImport

@attr.s
class Grid:
    """Grid indexing.

    Grid is a regular grid indexing algorithm. This class indexes a set of
    k-dimensional points in a regular grid.

    Parameters
    ----------
    data: ndarray, shape(n,k)
        The n data points of dimension k to be indexed. This array is not
        copied, and so modifying this data may result in erroneous results.
        The data can be copied if the grid is built with copy_data=True.
    N_cells: positive int, optional
        The number of cells of each dimension to build the grid. The final
        grid will have N_cells**k number of cells. Default: 64
    copy_data: bool, optional
        Flag to indicate if the data should be copied in memory.
        Default: False

    Attributes
    ----------
    dim: int
        The dimension of a single data-point.
    grid: dict
        This dictionary contains the data indexed in a grid. The key is a
        tuple with the k-dimensional index of each grid cell. Empty cells
        do not have a key. The value is a list of data points indices which
        are located within the given cell.
    k_bins: ndarray, shape (N_cells + 1, k)
        The limits of the grid cells in each dimension.
    edges: ndarray, shape (2, k)
        Grid edges or bound values. The lower and upper bounds per dimension.
    epsilon: float
        Value of increment used to create the grid edges.
    ndata: int
        Total number of a data-points.
    shape: tuple
        Number of cells per dimension.
    size: int
        Total number of cells.
    cell_width: ndarray
        Cell size in each dimension.

    """

    # User input params
    data = attr.ib(default=None, kw_only=False, repr=False)
    N_cells = attr.ib(default=64)
    copy_data = attr.ib(
        default=False, validator=attr.validators.instance_of(bool)
    )

    # =========================================================================
    # ATTRS INITIALIZATION
    # =========================================================================

    def __attrs_post_init__(self):
        """Init more params and build the grid."""
        if self.copy_data:
            self.data = self.data.copy()

        self.k_bins = self._make_bins()
        self.grid = self._build_grid()

    @data.validator
    def _validate_data(self, attribute, value):
        """Validate init params: data."""
        # Chek if numpy array
        if not isinstance(value, np.ndarray):
            raise TypeError(
                "Data: Argument must be a numpy array."
                "Got instead type {}".format(type(value))
            )
        # Check if data has the expected dimension
        if value.ndim != 2:
            raise ValueError(
                "Data: Array has the wrong shape. Expected shape of (n, k), "
                "got instead {}".format(value.shape)
            )
        # Check if data has the expected dimension
        if len(value.flatten()) == 0:
            raise ValueError("Data: Array must have at least 1 point")

        # Check if every data point is valid
        if not np.isfinite(value).all():
            raise ValueError("Data: Array must have real numbers")

    @N_cells.validator
    def _validate_N_cells(self, attr, value):
        """Validate init params: N_cells."""
        # Chek if int
        if not isinstance(value, int):
            raise TypeError(
                "N_cells: Argument must be an integer. "
                "Got instead type {}".format(type(value))
            )
        # Check if N_cells is valid, i.e. higher than 1
        if value < 1:
            raise ValueError(
                "N_cells: Argument must be higher than 1. "
                "Got instead {}".format(value)
            )

    # =========================================================================
    # PROPERTIES
    # =========================================================================

    @property
    def dim(self):
        """Grid dimension."""
        return self.data.shape[1]

    @property
    def edges(self):
        """Edges of the grid in each dimension."""
        return self.k_bins[[0, -1], :].copy()

    @property
    def epsilon(self):
        """Epsilon used to expand the grid."""
        # Check the resolution of the input data and increase it
        # two orders of magnitude. This works for float{32,64}
        # Fix issue #7
        dtype = self.data.dtype

        if np.issubdtype(dtype, np.integer):
            return 1e-1
        # assume floating
        return np.finfo(dtype).resolution * 1e2

    @property
    def ndata(self):
        """Total number of a data-points."""
        return len(self.data)

    @property
    def shape(self):
        """Grid shape, i.e. number of cells per dimension."""
        return (self.N_cells,) * self.dim

    @property
    def size(self):
        """Grid size, i.e. total number of cells."""
        return self.N_cells ** self.dim

    @property
    def cell_width(self):
        """Cell size in each dimension."""
        id0 = np.zeros((1, self.dim), dtype=int)
        lower, upper = self.cell_walls(id0)
        return upper - lower

    # =========================================================================
    # INTERNAL IMPLEMENTATION
    # =========================================================================

    def _make_bins(self):
        """Return bins values."""
        dmin = self.data.min(axis=0) - self.epsilon
        dmax = self.data.max(axis=0) + self.epsilon
        return np.linspace(dmin, dmax, self.N_cells + 1)

    def _digitize(self, data, bins):
        """Return data bin index."""
        if bins.ndim == 1:
            d = (data - bins[0]) / (bins[1] - bins[0])
        else:
            d = (data - bins[0, :]) / (bins[1, :] - bins[0, :])
        # allowed indeces with int16: (-32768 to 32767)
        return d.astype(np.int16)

    def _build_grid(self):
        """Build the grid."""
        # Digitize data points
        k_digit = self._digitize(self.data, self.k_bins)

        # Store in grid all cell neighbors
        compact_ind = np.ravel_multi_index(
            k_digit.T, self.shape, order="F", mode="clip"
        )

        compact_ind_sort = np.argsort(compact_ind)
        compact_ind = compact_ind[compact_ind_sort]
        k_digit = k_digit[compact_ind_sort]

        split_ind = np.searchsorted(compact_ind, np.arange(self.size))
        deleted_cells = np.diff(np.append(-1, split_ind)).astype(bool)
        split_ind = split_ind[deleted_cells]

        data_ind = np.arange(self.ndata)
        if split_ind[-1] > data_ind[-1]:
            split_ind = split_ind[:-1]

        list_ind = np.split(data_ind[compact_ind_sort], split_ind[1:])
        k_digit = k_digit[split_ind]

        grid = dict()
        for i, j in enumerate(k_digit):
            grid[tuple(j)] = tuple(list_ind[i])

        return grid

    # =========================================================================
    # GRID API
    # =========================================================================

    def contains(self, points):
        """Check if points are contained within the grid.

        Parameters
        ----------
        points: ndarray, shape (m,k)
            The point or points to check against the grid domain.

        Returns
        -------
        bool: ndarray, shape (m,)
            Boolean array indicating if a point is contained within the grid.
        """
        # Validate inputs
        vlds.validate_centres(points, self.data)

        lower = self.edges[0, :] < points
        upper = self.edges[-1, :] > points
        return (lower & upper).prod(axis=1, dtype=bool)

    def cell_digits(self, points):
        """Return grid cell indices for a given point.

        Parameters
        ----------
        points: ndarray, shape (m,k)
            The point or points to calculate the cell indices.

        Returns
        -------
        digits: ndarray, shape (m,k)
            Array of cell indices with same shape as `points`. If a point is
            outside of the grid edges `-1` is returned.
        """
        # Validate inputs
        vlds.validate_centres(points, self.data)

        digits = self._digitize(points, bins=self.k_bins)

        # Check if outside the grid
        outside = ~self.contains(points)
        if outside.any():
            digits[outside] = -1
        return digits

    def cell_id(self, points):
        """Return grid cell unique id for a given point.

        Parameters
        ----------
        points: ndarray, shape (m,k)
            The point or points to calculate the cell unique id.

        Returns
        -------
        ids: ndarray, shape (m,)
            Array of cell unique ids for each point. If a point is
            outside of the grid edges `-1` is returned.
        """
        # Validate points
        vlds.validate_centres(points, self.data)

        digits = self._digitize(points, bins=self.k_bins)
        ids = np.ravel_multi_index(
            digits.T, self.shape, order="F", mode="clip"
        )

        # Check if outside the grid
        outside = ~self.contains(points)
        if outside.any():
            ids[outside] = -1
        return ids

    def cell_digits2id(self, digits):
        """Return unique id of cells given their digits.

        Parameters
        ----------
        digits: ndarray, shape (m,k)
            Array of cell indices. Must be integers.

        Returns
        -------
        ids: ndarray, shape (m,)
            Array of cell unique ids for each point.
        """
        # Validate digits
        vlds.validate_digits(digits, self.N_cells)

        return np.ravel_multi_index(
            digits.T, self.shape, order="F", mode="clip"
        )

    def cell_id2digits(self, ids):
        """Return cell digits given their unique id.

        Parameters
        ----------
        ids: ndarray, shape (m,)
            Array of cell unique ids for each point.

        Returns
        -------
        digits: ndarray, shape (m,k)
            Array of cell indices.
        """
        # Validate ids
        vlds.validate_ids(ids, self.size)

        digits = np.unravel_index(ids, self.shape, order="F")
        digits = np.vstack(digits).T
        # Convert to int16 for consistency with _digitize
        return digits.astype(np.int16)

    def cell_walls(self, digits):
        """Return cell wall coordinates for given cell digits.

        Parameters
        ----------
        digits: ndarray, shape (m,k)
            Array of cell indices. Must be integers.

        Returns
        -------
        lower: ndarray, shape (m, 3)
            Lower cell wall values for each point.
        upper: ndarray, shape (m, 3)
            Upper cell wall values for each point.
        """
        # Validate digits
        vlds.validate_digits(digits, self.N_cells)

        kb = self.k_bins
        # get bin values for the walls
        lower = np.vstack([kb[digits[:, k], k] for k in range(self.dim)]).T
        upper = np.vstack([kb[digits[:, k] + 1, k] for k in range(self.dim)]).T
        return lower, upper

    def cell_centre(self, digits):
        """Return cell centre coordinates for given cell digits.

        Parameters
        ----------
        digits: ndarray, shape (m,k)
            Array of cell indices. Must be integers.

        Returns
        -------
        centres: ndarray, shape (m, k)
            Cell centre for each point.
        """
        # Validate digits
        vlds.validate_digits(digits, self.N_cells)

        lower, upper = self.cell_walls(digits)
        centre = (lower + upper) * 0.5
        return centre

    def cell_count(self, digits):
        """Return number of points within given cell digits.

        Parameters
        ----------
        digits: ndarray, shape (m,k)
            Array of cell indices. Must be integers.

        Returns
        -------
        count: ndarray, shape (m,)
            Cell count for each for each cell.
        """
        # Validate digits
        vlds.validate_digits(digits, self.N_cells)

        get = self.grid.get
        counts = [len(get(tuple(dgt), ())) for dgt in digits]
        return np.asarray(counts)

    def cell_points(self, digits):
        """Return indices of points within given cell digits.

        Parameters
        ----------
        digits: ndarray, shape (m,k)
            Array of cell indices. Must be integers.

        Returns
        -------
        points: list, length m
            List of m arrays. Each array has the indices to the
            neighbors of that cell.
        """
        # Validate digits
        vlds.validate_digits(digits, self.N_cells)

        get = self.grid.get
        points = [np.asarray(get(tuple(dgt), ())) for dgt in digits]
        return points

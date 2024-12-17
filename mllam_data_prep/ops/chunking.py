import numpy as np
from loguru import logger

# Max chunk size warning
CHUNK_MAX_SIZE_WARNING = 1 * 1024**3  # 1GB


def check_chunk_size(ds, chunks):
    """
    Check the chunk size and warn if it exceed CHUNK_MAX_SIZE_WARNING.

    Parameters
    ----------
    ds: xr.Dataset
        Dataset to be chunked
    chunks: Dict[str, int]
        Dictionary with keys as dimensions to be chunked and
        chunk sizes as the values

    Returns
    -------
    ds: xr.Dataset
        Dataset with chunking applied
    """

    # Check the chunk size
    for var_name, var_data in ds.data_vars.items():
        total_size = 1

        for dim, chunk_size in chunks.items():
            dim_size = ds.sizes.get(dim, None)
            if dim_size is None:
                raise KeyError(f"Dimension '{dim}' not found in the dataset.")
            total_size *= chunk_size

        dtype = var_data.dtype
        bytes_per_element = np.dtype(dtype).itemsize

        memory_usage = total_size * bytes_per_element

        if memory_usage > CHUNK_MAX_SIZE_WARNING:
            logger.warning(
                f"The chunk size for '{var_name}' exceeds '{CHUNK_MAX_SIZE_WARNING}' GB."
            )

import numpy as np


def convert_numpy_int64(data):
    if isinstance(data, np.int64):
        return int(data)
    elif isinstance(data, dict):
        return {k: convert_numpy_int64(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_int64(i) for i in data]
    return data

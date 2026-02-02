# Task: Implement normalize_slice(seq_len, start=None, stop=None, step=1).
# Requirements:
# - seq_len must be int (bool not allowed) and >= 0 else ValueError("seq_len must be a non-negative int")
# - start/stop may be None or int (bool not allowed); else TypeError("start/stop must be int or None")
# - step must be int (bool not allowed) and not 0; else ValueError("step must be a non-zero int")
# - Return a tuple (start_i, stop_i, step) equivalent to Python slicing bounds for a sequence of length seq_len
#   (Use slice(start, stop, step).indices(seq_len) once inputs are validated.)
# Expected outcome:
# - normalize_slice(10, 2, None, 2) returns (2,10,2)
# - normalize_slice(5, 0, 5, 0) raises ValueError("step must be a non-zero int")


def normalize_slice(seq_len, start=None, stop=None, step=1):
    # TODO
    pass


if __name__ == "__main__":
    print(normalize_slice(10, 2, None, 2))
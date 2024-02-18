def read_file(p: str, mode='r') -> str | bytes:
    with open(p, mode=mode) as f:
        return f.read()

def slash_tile(tile: str):
    if len(tile) != 5:
        raise ValueError(f"tile should be a str of len 5, not {tile}")

    return f"{tile[:2]}/{tile[2]}/{tile[3:]}"

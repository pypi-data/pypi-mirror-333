def clamp(value: int, lower: int, upper: int) -> int:
    return max(lower, min(value, upper))


def unpack_singleton_value(obj):
    if isinstance(obj, list):
        processed = [unpack_singleton_value(item) for item in obj]
        non_empty = [item for item in processed if not (isinstance(item, list) and len(item) == 0)]

        if len(non_empty) == 1:
            return non_empty[0]
        else:
            return non_empty
    else:
        return obj


def is_not_none_orElse(value, default):
    return value if value is not None else default


def is_not_none_then_orElse(value, then, default):
    return then if value is not None else default

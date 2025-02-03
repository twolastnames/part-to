def common_repr(object, *attrs):
    using = [
        "{}={}".format(attr, getattr(object, attr))
        for attr in attrs
        if hasattr(object, attr)
    ]
    return "[ {} ]".format(" ".join(using))

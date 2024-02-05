import datetime
import json
import time


def get_filename(filename, request):
    return filename.upper()


def merge(o1, o2):
    for key in o2:
        val2 = o2[key]
        if isinstance(val2, dict) and key in o1:
            val1 = o1[key]
            for k in val2:
                val1[k] = val2[k]
        else:
            o1[key] = val2
    return o1


def json_dumps(value):
    return json.dumps(value, default=json_handler)


def json_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    return repr(x)


def byte_to_file(file):
    import base64
    import io

    image_bytes = base64.b64decode(file)
    image = io.BytesIO(image_bytes)

    return image

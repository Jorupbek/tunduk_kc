import uuid

from apps.history.models import TundukRequestLog

REQUEST_TYPE = {
    'Infocom': TundukRequestLog.RequestType.INFOCOM,
    'Minjyst': TundukRequestLog.RequestType.MINJYST,
    'Unaa': TundukRequestLog.RequestType.UNAA,
    'Kadastr': TundukRequestLog.RequestType.KADASTR,
    'MinSelXoz': TundukRequestLog.RequestType.MINSELXOZ,
}


def tunduk_request_logic(request, result, service, file=None, filename=None, full_name=None, wallet=None):
    tunduk_request = TundukRequestLog(
        user=request.user,
        data=result,
        request_type=REQUEST_TYPE.get(service.system_name)
    )
    if file:
        filename = filename if filename else f'{request.user}/{uuid.uuid4()}.jpeg'
        tunduk_request.file.save(filename, file)

    tunduk_request.save()

    return tunduk_request

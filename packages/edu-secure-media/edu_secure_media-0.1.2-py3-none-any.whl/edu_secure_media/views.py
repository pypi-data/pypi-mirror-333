import os
from typing import (
    TYPE_CHECKING,
    Union,
)
from django.conf import (
    settings,
)
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
)
from django_sendfile import (
    sendfile,
)

from . import (
    config,
)
from .utils import (
    validate_descriptor,
)


if TYPE_CHECKING:
    from django.http import (
        HttpRequest,
    )
    from django.http.response import (
        FileResponse,
    )


def check_media_permission_view(request: 'HttpRequest') -> Union[HttpResponse, 'FileResponse']:
    """Проверяет наличие разрешений для доступа к media.

    Args:
        request:
            Объект запроса.

    Returns:
        объект 'HttpResponse' либо 'FileResponse'.

    """
    ret = None
    descriptor = None

    if config.DESCRIPTOR_PARAM_NAME in request.GET:
        descriptor = validate_descriptor(request.get_full_path())

    for regex, handler, options in config.get_handlers_config():
        if regex is None or (descriptor and regex.search(descriptor)):
            ret = handler(request=request, descriptor=descriptor, **options)
            if ret is not None:
                break

    if isinstance(ret, HttpResponse):
        return ret

    if ret:
        ret = sendfile(request, os.path.join(settings.MEDIA_ROOT, request.path.replace(settings.MEDIA_URL, '', 1)))
    else:
        ret = HttpResponseNotFound('Media Not Found!')

    return ret

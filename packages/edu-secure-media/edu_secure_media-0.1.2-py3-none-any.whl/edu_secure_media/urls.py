from django.conf import (
    settings,
)
from django.urls import (
    re_path,
)

from .views import (
    check_media_permission_view,
)


urlpatterns = (re_path(r'^%s' % settings.MEDIA_URL.lstrip('/'), check_media_permission_view),)

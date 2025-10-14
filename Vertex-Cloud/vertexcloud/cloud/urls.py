from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

        #AUTH PATHS

        path("", views.api_health, name="api_health"),
        path("signup/", views.create_user, name="create_user"),
        path("login/", views.login_user, name="login_user"),
        path("delete/user/", views.delete_user, name="delete_user"),

        #CLOUD PATHS

        path("create/file/", views.add_file, name="add_file"),
        path("get/files/", views.get_files, name="get_file"),
        path("token/", views.my_key, name="my_key"),
        path("get/file/", views.get_file, name="get_file"),
        path("delete/file", views.delete_file, name="delete_file"),
        path("clear/session/", views.remove_session,name="delete_session"),


        ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

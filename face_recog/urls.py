from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^face/recognition',
        views.verify_face_recognition,
        name='verify_face_recognition'
    ),
]

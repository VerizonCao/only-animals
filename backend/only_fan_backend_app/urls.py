from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # chat endpoint
    path("chat/", views.chat, name="chat"),
    path("get_history/", views.get_history, name="get_history"),
    path('ai/is_image_request/', views.is_image_request, name='is_image_request'),
    path('ai/generate_image/', views.generate_image, name='generate_image'),
]
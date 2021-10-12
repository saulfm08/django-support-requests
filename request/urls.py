from django.urls import path
from . import views

urlpatterns = [
    path('', views.FormRequest.as_view(), name='home'),
    path('request-list', views.RequestList.as_view(), name='requests'),
    path('post-request', views.post_request, name='post_request'),
]
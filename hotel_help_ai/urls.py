
from django.contrib import admin
from django.urls import path
from .views import chatbot



urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/chatbot/", chatbot, name="chatbot_api"),
    path("api/v1/chatbot", chatbot),
]



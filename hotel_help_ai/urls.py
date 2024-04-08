
from django.contrib import admin
from django.urls import path
from .views import chatbot_api



urlpatterns = [
    path('admin/', admin.site.urls),
    path("chatbot/", chatbot_api, name="chatbot_api"),
]



from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import SpeechToTextView, TextToSpeechView, TextToDocView

urlpatterns = [
    path('speech-to-text/', SpeechToTextView.as_view(), name='speech-to-text'),
    path('text-to-speech/', TextToSpeechView.as_view(), name='text-to-speech'),
    path('text-to-doc/', TextToDocView.as_view(), name='text-to-doc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

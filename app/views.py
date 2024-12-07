from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import speech_to_text, text_to_speech, text_to_doc
from django.conf import settings
import os




class SpeechToTextView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        audio_file = request.FILES.get('audio')
        save_to_doc = request.data.get("save_to_doc", False)  

        if audio_file:
            text = speech_to_text(audio_file)
            
            if save_to_doc:
                doc_filename = text_to_doc(text)

                if doc_filename:
                    # Make the doc file URL accessible for download
                    doc_url = os.path.join(settings.MEDIA_URL, os.path.basename(doc_filename))
                    return Response({
                        "text": text, 
                        "message": "Text converted and saved to doc.",
                        "file": doc_url  # Return the URL of the file
                    }, status=status.HTTP_200_OK)
            
            return Response({"text": text}, status=status.HTTP_200_OK)
        
        return Response({"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)


class TextToSpeechView(APIView):
    def post(self, request):
        text = request.data.get("text")
        if text:
            text_to_speech(text)
            return Response({"message": "Speech generated successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)


class TextToDocView(APIView):
    def post(self, request):
        text = request.data.get("text")
        if text:
            filename = text_to_doc(text)
            return Response({"message": "DOC file created.", "file": filename}, status=status.HTTP_200_OK)
        return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)
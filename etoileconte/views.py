import environ
from openai import OpenAI
import uuid
import logging
from django.core.files.base import ContentFile
from .models import Story
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Story, CustomUser
from .serializers import StorySerializer
from random import randint
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer

env = environ.Env()
environ.Env.read_env()

#get an instance of a logger
logger = logging.getLogger(__name__)

# Initialize the OpenAI client once
openai_client = OpenAI(api_key=env('OPENAI_API_KEY'))

def get_story_from_api():
    try:
        response = openai_client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt="Générer une courte histoire en français qui peut être lue en deux minute. Titre:",
            max_tokens=1000,
        )
        story_text = response.choices[0].text.strip()
        return story_text
    except Exception as e:
        logger.info(f"Error during story generation: {e}")
        return None
    

def get_audio():
    try:
        text_response = get_story_from_api()
        if text_response:

            #Extract the title from the story text
            title, story_body = text_response.split('\n', 1)

            response = openai_client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text_response,
                response_format="mp3",
            )

             # Define a unique filename for the audio file
            audio_filename = f"audio_{uuid.uuid4()}.mp3"
            audio_file_path = ContentFile(response.content, name=audio_filename)

            # Write audio data to the file in the media folder
            # with open(audio_file_path, 'wb') as audio_file:
            #     audio_file.write(response.content)

            #create a new Story instance and save to the datanase
            story = Story(title=title, text=story_body, audio_file=audio_file_path)
            story.save()

            # Return both text and audio URL
            logger.info(f"Successfully saved story '{title}' with audio.")
        else:
            logger.info("Error generating text for audio.")
    except Exception as e:
        logger.info(f"Error during audio generation : {e}")

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    @action(detail=False, methods=['get'])
    def random(self, request):
        count = Story.objects.count()
        if count == 0:
            return Response({'message': 'No stories available.'}, status=status.HTTP_404_NOT_FOUND)
        
        random_index = randint(0, count - 1)
        story = Story.objects.only('id')[random_index]
        story = Story.objects.get(id=story.id)  # Fetch the full story details
        serializer = self.get_serializer(story)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginViewSet(viewsets.ViewSet):

    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({'message': 'OK'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

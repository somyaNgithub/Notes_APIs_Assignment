from django.shortcuts import render
from rest_framework.decorators import api_view
from Auth.token_utils import get_user_id_from_token
from Auth.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import NotesSerializer

# Create your views here.

#-----view to create questions-----
@api_view(['POST'])
def create_note(request):
    # Get user ID from token
    user_id = get_user_id_from_token(request)
    print(user_id)

    if user_id is not None:
        # Retrieve user instance based on user ID
        try:
            user = CustomUser.objects.get(U_id=user_id)
            print(user)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create a new question with user association
        request.data['U_id'] = user_id
        deserializer = NotesSerializer(data=request.data, partial=True)
        if deserializer.is_valid():
            # serializer.validated_data['user'] = user  # Associate the question with the user
            deserializer.save()
            return Response({'data' : deserializer.data, 'api_status' : True}, status=status.HTTP_201_CREATED)
        
        else:
            return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)




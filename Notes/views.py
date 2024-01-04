from django.shortcuts import render
from rest_framework.decorators import api_view
from Auth.token_utils import get_user_id_from_token
from Auth.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import NotesSerializer
from .models import Notes

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

            # Create a new question with user association
            request.data['U_id'] = user_id
            deserializer = NotesSerializer(data=request.data, partial=True)
            if deserializer.is_valid():
            # serializer.validated_data['user'] = user  # Associate the question with the user
                deserializer.save()
                return Response({'data' : deserializer.data, 'api_status' : True}, status=status.HTTP_201_CREATED)
        
            else:
                return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)






@api_view(['GET'])
def AllNotes_by_user(request):
    user_id = get_user_id_from_token(request)
    if user_id is not None:
        try:
                # Retrieve questions for the specified user
                notes = Notes.objects.filter(U_id=user_id)
        
                # Serialize the questions
                serializer = NotesSerializer(notes, many=True)
        
                return Response({'data':serializer.data, 'api_status':True}, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)
    




@api_view(['GET'])
def get_note(request, uid):
    user_id = get_user_id_from_token(request)
    print('flag1')
    if user_id is not None:
        try:
            # Retrieve questions for the specified user
            notes = Notes.objects.filter(N_id=uid)
            print('flag2')
        
            # Serialize the questions
            serializer = NotesSerializer(notes, many=True)
            print('flag3')
            print(serializer)
        
            return Response({'data':serializer.data, 'api_status':True}, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)





@api_view(['PUT'])
def update_note(request, uid):
    user_id = get_user_id_from_token(request)
    if user_id is not None:
        # Retrieve user instance based on user ID
        try:
            user = CustomUser.objects.get(U_id=user_id)
            
            note = Notes.objects.get(N_id=uid)
            deserializer = NotesSerializer(instance=note, data=request.data, partial=True)
            print('flag2')
            if deserializer.is_valid():
                deserializer.save()
                return Response({'data' : deserializer.data, 'api_status' : True}, status=status.HTTP_201_CREATED)
        
            else:
                return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)
    



@api_view(['DELETE'])
def delete_Note(request,uid):
    user_id = get_user_id_from_token(request)
    if user_id is not None:
        try:
            note = Notes.objects.get(N_id=uid)
            if str(user_id) == str(note.U_id):    # note  convert  <class 'restAPI.models.CustomUser'> = question.user_id  in to string 
                return Response({"error": "You do not have permission to delete this question.",
                "userids" :f"user->{type(user_id)} note-> {type(note.U_id)}"
                }, status=status.HTTP_403_FORBIDDEN)

            # Delete the question
            note.delete()

            return Response({"message": f"Note with id {uid} deleted successfully"
            "userids"
            }, status=status.HTTP_204_NO_CONTENT)

        except Notes.DoesNotExist:
            return Response({"error": "Notes not found"}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({"error": "Authentication token not valid"}, status=status.HTTP_401_UNAUTHORIZED)
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''
    email = request.data.get('email')
    password = request.data.get('password')

    if email and password:
        try:
            user = User.objects.get(email=email)
            authenticated_user = authenticate(username=user.username, password=password)
            
            if authenticated_user is not None:
                token = Token.objects.get(user=authenticated_user)
                data = {
                    'valid': True,
                    'token': token.key,
                    'user_id': authenticated_user.id
                }
                return Response(data)
            else:
                data = {'valid': False, 'error': 'Invalid credentials'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            data = {'valid': False, 'error': 'User with this email does not exist'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {'valid': False, 'error': 'Email and password are required'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if email and password:
        new_user = User.objects.create_user(
            username=email,  # You can set email as the username
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        token = Token.objects.create(user=new_user)

        data = {
            'valid': True,
            'token': token.key,
            'user_id': new_user.id
        }

        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {'valid': False, 'error': 'Email and password are required'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

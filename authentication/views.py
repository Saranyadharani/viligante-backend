from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import jwt
from datetime import datetime, timedelta
from django.conf import settings

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        # Find user by email
        user = User.objects.get(email=email)
        # Authenticate with username and password
        auth_user = authenticate(username=user.username, password=password)
        
        if auth_user is not None:
            # Create JWT token
            token = jwt.encode({
                'user_id': user.id,
                'email': user.email,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, settings.SECRET_KEY, algorithm='HS256')
            
            return Response({
                'success': True,
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'name': f"{user.first_name} {user.last_name}".strip() or user.username
                }
            })
        else:
            return Response({
                'success': False,
                'message': 'Invalid password'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User with this email does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Login failed',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def register(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username', email.split('@')[0])
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response({
                'success': False,
                'message': 'User with this email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        return Response({
            'success': True,
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Registration failed',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
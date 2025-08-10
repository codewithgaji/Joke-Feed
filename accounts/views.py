from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from .serializers import SignupSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.views import View

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, mixins
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.

# API Views (for JSON responses)
class LoginAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip().lower()
            password = data.get('password', '')
            remember = data.get('remember', False)
            
            if not email or not password:
                return JsonResponse({
                    'error': True,
                    'message': 'Email and password are required'
                }, status=400)
            
            # Authenticate using email as username
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if remember:
                        request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
                    else:
                        request.session.set_expiry(0)  # session only
                    
                    # Get or create DRF token
                    token, _ = Token.objects.get_or_create(user=user)
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Login successful!',
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name
                        },
                        'token': token.key,
                        'session_key': request.session.session_key
                    }, status=200)
                else:
                    return JsonResponse({
                        'error': True,
                        'message': 'Your account has been deactivated'
                    }, status=401)
            else:
                return JsonResponse({
                    'error': True,
                    'message': 'Invalid email or password'
                }, status=401)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'error': True,
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': True,
                'message': f'An error occurred: {str(e)}'
            }, status=500)

class SignupAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
          
            # Validation: Ensure all fields are present
            if not username or not email or not password:
                return JsonResponse({
                    'error': True,
                    'message': 'Username, email, and password are required.'
                }, status=400)
            
            # Get User model
            User = get_user_model()
            
            # Validation: Check for existing email
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'error': True,
                    'message': 'Email already exists'
                }, status=400)
          
            # Validation: Check for existing username
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'error': True,
                    'message': 'Username already exists'
                }, status=400)
          
            # Create user with a more robust try-except block
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
              
                # Critical Fix: Check if the user object was created successfully
                if user is not None:
                    return JsonResponse({
                        'success': True,
                        'message': 'Account created successfully',
                        'user_id': user.id
                    }, status=201)
                else:
                    return JsonResponse({
                        'error': True,
                        'message': 'Failed to create user account unexpectedly'
                    }, status=500)
                  
            except Exception as e:
                # This catches any errors from the create_user call itself
                return JsonResponse({
                    'error': True,
                    'message': f'Failed to create user: {str(e)}'
                }, status=500)
        except json.JSONDecodeError:
            return JsonResponse({
                'error': True,
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            # This catches any other unexpected errors
            return JsonResponse({
                'error': True,
                'message': str(e)
            }, status=500)

# Template views (for serving the HTML pages)
def signup_page(request):
    return render(request, 'auth/signup.html')

def login_page(request):
    return render(request, 'auth/login.html')


@login_required
def homeView(request):
    return render(request, "index.html")




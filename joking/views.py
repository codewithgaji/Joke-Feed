from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import JokesModel, TrackVote
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, mixins
from django.shortcuts import get_object_or_404
from .serializers import JokesSerializer
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


# Create your views here.

User = get_user_model()


@login_required
def homeView(request):
    return render(request, "index.html")

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            # Validation
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'error': True,
                    'message': 'Email already exists'
                }, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'error': True,
                    'message': 'Username already exists'
                }, status=400)
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Account created successfully',
                'user_id': user.id
            }, status=201)
            
        except Exception as e:
            return JsonResponse({
                'error': True,
                'message': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')

class LoginView(View):
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
# Optional: Logout view
@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request):
        try:
            from django.contrib.auth import logout
            logout(request)
            return JsonResponse({
                'success': True,
                'message': 'Logged out successfully'
            }, status=200)
        except Exception as e:
            return JsonResponse({
                'error': True,
                'message': f'Logout failed: {str(e)}'
            }, status=500)

# Template views (for serving the HTML pages)
def signup_page(request):
    return render(request, 'auth/signup.html')

def login_page(request):
    return render(request, 'auth/login.html')

def home_page(request):
    return render(request, 'home.html')


def landing_page(request):
    return render(request, "landing.html")


def about_page(request):
    return render(request, "about.html")

# Working on this to better my skills
class CreateJoke(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JokesSerializer
    queryset = JokesModel.objects.all()
    
    def post(self, request:Request, *args, **kwargs):
        user = request.user
        data_incoming = request.data
        serializer = self.serializer_class(data=data_incoming)

        if serializer.is_valid():
            # Manually assigning user to "created_by" in the model
            joke = JokesModel.objects.create(content = serializer.validated_data['content'], created_by=user)
        # serializer.save() Not needed, since I'm already creating the object
            serialized_joke = self.serializer_class(joke) 

            return Response(data=serialized_joke.data, status=status.HTTP_201_CREATED)
    
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request: Request):
        jokes = JokesModel.objects.all().order_by('-created_at')  # Get all jokes, newest first
        serializer = self.serializer_class(jokes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

        
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def get_queryset(self):
        return self.queryset

# Getting one joke at a time

class GetDeleteJoke(generics.GenericAPIView,mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = JokesModel.objects.all()
    serializer_class = JokesSerializer
    def get(self, request:Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def delete(self, request:Request, *args, **kwargs):
          return self.destroy(request, *args, **kwargs)





class VotesView(generics.GenericAPIView):
  permission_classes = [IsAuthenticated]
  def post(self, request:Request, joke_id, vote_type):  # vote_type = 'upvote' or 'downvote'
      user = request.user
      joke = JokesModel.objects.get(id=joke_id)

      # Check if user already voted on this joke
      existing_vote = TrackVote.objects.filter(user=user, joke=joke).first()

      if existing_vote:
          if existing_vote.vote_type == vote_type:
              return Response({'detail': 'You have already voted this way.'}, status=status.HTTP_400_BAD_REQUEST)
          else:
              # User wants to change their vote
              if vote_type == 'upvote':
                  joke.upvotes += 1
                  joke.downvotes -= 1
              else:
                  joke.downvotes += 1
                  joke.upvotes -= 1
              existing_vote.vote_type = vote_type
              existing_vote.save()
              joke.save()
              return Response({'detail': 'Vote updated.'})

      else:
          # First time voting
          TrackVote.objects.create(user=user, joke=joke, vote_type=vote_type)
          if vote_type == 'upvote':
              joke.upvotes += 1
          else:
              joke.downvotes += 1
          joke.save()
          return Response({'detail': 'Vote registered.'})
      

  # This is to get the number of votes for each joke Id
  def get(self, request:Request, joke_id, vote_type=None):
      # To track what the user voted as
      user_vote = TrackVote.objects.filter(user=request.user, joke_id=joke_id).first()
      your_vote = user_vote.vote_type if user_vote else None

      joke = get_object_or_404(JokesModel, id=joke_id)
      content = {
          "Joke Id": joke.id,
          "Upvotes" : joke.upvotes,
          "Downvotes": joke.downvotes,
          "Yourvote": your_vote,
      }

      return Response(data=content, status=status.HTTP_200_OK)

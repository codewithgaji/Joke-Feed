from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # API endpoints
    path("api/signup/", views.SignupAPIView.as_view(), name="signup"),

    path('login/home/', views.homeView, name='home'),

    path("api/login/", views.LoginAPIView.as_view(), name="api_login"),  # Changed to api/login/
    
    # HTML page views
    path('signup/', views.signup_page, name='signup_page'),
    path('login/', views.login_page, name='login_page'),  # This now works for GET requests
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
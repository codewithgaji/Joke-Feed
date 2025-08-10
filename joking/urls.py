from django.urls import path
from .views import VotesView, CreateJoke, GetDeleteJoke, LogoutView,  landing_page, about_page
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", landing_page, name="landingpage"),

    path("about/", about_page, name="about"),
   

    # path("api/signup/", SignupView.as_view(), name="signup"),

    # path("api/view/login/", LoginView.as_view(), name="login"),

    path('api/logout/', LogoutView.as_view(), name='logout_api'),

    path("<int:joke_id>/<str:vote_type>/", VotesView.as_view(), name="postvotes"),

    path("<int:joke_id>/votes/", VotesView.as_view(), name="getvotes"),

    path("Added/", CreateJoke.as_view(), name="jokecreated"),

    path("<int:pk>/", GetDeleteJoke.as_view(), name="retrieve_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)



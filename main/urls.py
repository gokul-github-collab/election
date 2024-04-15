from django.urls import path
from . import views
from django.conf import  settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('sign-up', views.register, name='register'),


    path('', views.home, name='home'),
    path('voters', views.voters, name='voters'),
    path('voter-form', views.create_voter, name='voter_form'),
    path('voter-profile/<slug:aadhar>', views.voter_profile, name='voter-profile'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
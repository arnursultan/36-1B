from django.urls import path
from .views import RegisterView, MeView, UserListView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('me/', MeView.as_view()),
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
]
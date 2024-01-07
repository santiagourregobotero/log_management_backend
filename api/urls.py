from django.urls import path, include
from users import views as UserView
from syslogs.views import LogDetailView, LogListCreateView, LogAnalyticsView

urlpatterns = [
    path('auth/register', UserView.RegisterAPIView.as_view(), name='user-login'),
    path('auth/login', UserView.LoginAPIView.as_view(), name='user-register'),
    path('auth/access-token', UserView.LoginWithTokenAPIView.as_view(), name='user-register'),
    
    path('profile', UserView.ProfileView.as_view(), name='profile'),
    path('users', UserView.UserListView.as_view(), name='user-list'),
    path('user', UserView.UserCreateView.as_view(), name='user-create'),
    path('user/<int:pk>', UserView.UserRUDView.as_view(), name='user'),
    
    path('logs', LogListCreateView.as_view(), name='log-create'),
    path('logs/<int:pk>', LogDetailView.as_view(), name='log-detail'),
    path('logs/analytics', LogAnalyticsView.as_view(), name='log-analytics'),
]
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('profileimage', views.ProfileImageViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('user/', views.UserView.as_view(), name = 'user'),
    path('register/', views.UserRegistrationApiView.as_view(), name = 'register'),
    path('login/', views.UserLoginApiView.as_view(), name = 'login'),
    path('logout/', views.UserLogoutView.as_view(), name = 'logout'),
    # path('logout/', views.UserLogoutView.as_view(), name = 'logout'),
    # path('logout/', views.UserView.as_view(), name = 'logout'),
    path('active/<uid64>/<token>', views.activate, name = 'activate'),
    path('updateprofile/', views.UpdateProfileView.as_view(), name = 'update_profile'),
    path('uploadprofile/', views.UploadProfileView.as_view(), name = 'upload_profile'),
    path('resetpassemail/', views.ResetPasswordEmailView.as_view(), name = 'resetpass_email'),
    path('resetpassnew/<uidb64>/<token>', views.ResetPasswordNewView.as_view(), name = 'resetpass_new'),
    path('changepass/', views.ChangePasswordView.as_view(), name = 'change_pass'),
]
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('profile/' , views.profile , name='profile'),
    path('my_booking/' , views.my_booking , name='my_booking'),
    path('profile/edit/' , views.edit_profile , name='edit_profile'),
    path('change_password/' , views.change_password , name='change_password'),
]
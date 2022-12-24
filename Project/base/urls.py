from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),


    path('', views.home, name="home"),
    path('profile/<str:pk>', views.profile, name="profile"),
    path('edit-profile/<str:pk>', views.editProfile, name="edit-profile"),


    path('content/<str:pk>/', views.content, name="content"),

    path('create-content/', views.createContent, name="create-content"),
    path('update-content/<str:pk>', views.updateContent, name="update-content"),
    path('delete-content/<str:pk>', views.deleteContent, name="delete-content"),

]

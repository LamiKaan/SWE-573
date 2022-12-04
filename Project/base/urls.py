from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),


    path('', views.home, name="home"),
    path('content/<str:pk>/', views.content, name="content"),

    path('create-content/', views.createContent, name="create-content"),
    path('update-content/<str:pk>', views.updateContent, name="update-content"),
    path('delete-content/<str:pk>', views.deleteContent, name="delete-content"),

]

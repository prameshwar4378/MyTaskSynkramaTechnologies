from django.contrib import admin
from django.urls import path
from .import views
from .views import LoginView,Post_Create_And_Show_List, Post_Update_And_Delete

urlpatterns = [
    path('', views.index,name='index'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', views.sign_out, name='logout'),
    path('api/posts/', Post_Create_And_Show_List.as_view(),name="create_and_get"),
    path('api/posts/<int:pk>/', Post_Update_And_Delete.as_view(),name="update_and_delete"),
]

from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login,logout
from .serializers import LoginSerializer
from django.views.decorators.csrf import csrf_exempt

from rest_framework.generics import ListCreateAPIView, UpdateAPIView,DestroyAPIView,RetrieveAPIView
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import BasePermission

from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Create your views here.
def index(request):
    data=Post.objects.all()
    if request.method=="GET":
        if 'txt_id' in request.GET:
            val_id=request.GET.get('txt_id')
            data=Post.objects.filter(id=val_id)
    return render(request,'index.html',{'data':data})

def sign_out(request):
    logout(request)
    return redirect('/')

class LoginView(APIView):
    @csrf_exempt
    def post(self, request): 
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Is_authenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

class PostPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 5

class Post_Create_And_Show_List(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [Is_authenticated]
    pagination_class = PostPagination
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        body = self.request.query_params.get('body')
        author = self.request.query_params.get('author')
        if title:
            queryset = queryset.filter(title__icontains=title)
        if body:
            queryset = queryset.filter(body__icontains=body)
        if author:
            queryset = queryset.filter(author__username__icontains=author)
        return queryset

class Post_Update_And_Delete(UpdateAPIView,DestroyAPIView,RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [Is_authenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    pagination_class = PostPagination


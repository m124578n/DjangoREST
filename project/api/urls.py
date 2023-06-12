from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'todolists', views.ToDoListViewset, basename='todolist')
router.register(r'users', views.UserViewset, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('hello/', views.HelloView.as_view(), name='hello'),
]


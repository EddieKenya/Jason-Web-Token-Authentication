from django.urls import path
from.import views
from rest_framework_simplejwt.views import (
    
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('list/', views.PostList.as_view(), name='postlist'),
    path('list/<pk>', views.PostDetail.as_view(), name='postdetail' ),
    path('create/', views.CreatePost.as_view(), name = 'CreatePost'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserRegistration.as_view(), name='registration'),
    path('logout/', views.BlackListTokenView.as_view(), name='logout'),
    path('search/', views.PostSearchFilter.as_view(), name='search')
]
from django.urls import path
from .views import CreateUserView

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('get-user/<int:id>/', GetUserView.as_view(), name='get-user'),
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('get-post/<int:id>/', GetPostView.as_view(), name='get-post'),
    path('create-comment/', CreateCommentView.as_view(), name='create-comment')
]
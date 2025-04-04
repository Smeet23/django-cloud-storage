from django.urls import path
from .views import file_upload_view,file_list_view,signup_view,login_view,logout_view,home,file_delete

urlpatterns = [
    path('upload/', file_upload_view, name="file_upload"),
    path('', signup_view, name='home'),
    path('files/', file_list_view, name="file_list"),
    path('signup/', signup_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('delete/<int:pk>/', file_delete, name='file_delete'),
]

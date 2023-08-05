from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload, name='home'),
    path('allfiles', views.all_file, name='allfiles'),
    path('file/<int:id>/', views.file, name='file'),
    path('allchildfiles', views.all_child_files, name='allchildfiles'),
    # path('compare/<int:id>', views.compare),
]

from django.urls import path
from task import views

urlpatterns = [
    path('tasks/', views.TaskList.as_view()),
]

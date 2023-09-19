# from django.http import Http404
# from rest_framework import status, permissions, filters
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Task
# from .serializers import TaskSerializer, TaskDetailSerializer
# from drf_api.permissions import IsOwnerOrReadOnly


# class TaskList(APIView):
#     serializer_class = TaskSerializer
#     permission_classes = [
#         permissions.IsAuthenticatedOrReadOnly
#     ]

#     def get(self, request):
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(
#             tasks, many=True, context={'request': request}
#             )
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = TaskSerializer(
#             data=request.data, context={'request': request}
#         )
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(
#                 serializer.data, status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TaskDetail(APIView):
#     serializer_class = TaskDetailSerializer
#     permission_classes = [IsOwnerOrReadOnly]

#     def get_object(self, pk):
#         try:
#             task = Task.objects.get(pk=pk)
#             self.check_object_permissions(self.request, task)
#             return task
#         except Task.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         task = self.get_object(pk)
#         serializers = TaskDetailSerializer(
#             task, context={'request': request}
#         )
#         return Response(serializers.data)

#     def put(self, request, pk):
#         task = self.get_object(pk)
#         serializer = TaskDetailSerializer(
#             task, data=request.data, context={'request': request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(
#             serializer.errors, status=status.HTTP_400_BAD_REQUEST
#             )

#     def delete(self, request, pk):
#         task = self.get_object(pk)
#         task.delete()
#         return Response(
#             status=status.HTTP_204_NO_CONTENT
#         )

from rest_framework import generics, permissions, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Task
from .serializers import TaskSerializer, TaskDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Task.objects.all()
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = [
        'owner__username',
        'category__category_title',
        'title',
    ]
    filterset_fields = [  # Define the fields you want to filter
        'completed',
        'is_urgent',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()


class IncompleteTaskCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        incomplete_count = Task.objects.filter(owner=user, completed=False).count()
        return Response({'incomplete_task_count': incomplete_count}, status=status.HTTP_200_OK)

class UrgentTaskCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        urgent_count = Task.objects.filter(owner=user, completed=False, is_urgent=True).count()
        return Response({'urgent_task_count': urgent_count}, status=status.HTTP_200_OK)
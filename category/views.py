from rest_framework import generics, permissions, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Category
from .serializers import CategorySerializer


class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = [
        'category_title',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # Filter categories to only include those created by the current user
        return Category.objects.filter(owner=self.request.user)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

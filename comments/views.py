from django.shortcuts import get_object_or_404
from .models import Comment
from .serializers import CommentSerializer 
from rest_framework import generics  # pyright: ignore[reportMissingImports]
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError, PermissionDenied
from products.models import Product

class AdminCommentList(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CommentSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Comment.objects.all()
        if pk : 
            queryset = Comment.objects.filter(product_id = pk)
        return queryset.order_by('-update')

class AdminCommentEdit(generics.UpdateAPIView):
    queryset =Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

class AdminCommentDelete(generics.DestroyAPIView):
    queryset =Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]


class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comment.objects.filter(product_id = pk, active=True).order_by('-update')

class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('pk')
        user = self.request.user
        product = get_object_or_404(Product, pk=product_id)

        existing_comment = Comment.objects.filter(product_id=product_id, user=user)
        if existing_comment.exists():
            raise ValidationError({'message': 'you have already commentd on this product'})

        serializer.save(product=product, user=user)

class CommentEdit(generics.UpdateAPIView):
    queryset =Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied('You dont have permission to edit this comment.')
        return obj

class CommentDelete(generics.DestroyAPIView):
    queryset= Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied('You dont have permission to delete this comment.')
        return obj

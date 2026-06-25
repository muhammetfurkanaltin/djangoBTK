from rest_framework import serializers
from .models import Comment
from users.serializer import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    # user=serializer.SlugRelatedField(read_only=True, slug_field='username')
    
    class Meta:
        model = Comment
        fields =['id', 'rating', 'description', 'active', 'created_at', 'update', 'product', 'user']

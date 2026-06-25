from rest_framework import serializers
from .models import Product
from rest_framework.validators import UniqueValidator
from categories.models import Category
import re
from comments.serializers import CommentSerializer
from categories.serializers import CategorySerializer

class ProductListSerializer(serializers.ModelSerializer) : 
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ['id','name','price','stock','slug','category']

class ProductDetailsSerializer(serializers.ModelSerializer) : 
    comments = CommentSerializer(many=True, read_only= True)
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ['id','name','description','price','stock','slug','category','comments']

class ProductSerializer(serializers.ModelSerializer) : 
    name = serializers.CharField(max_length =200,validators = [UniqueValidator(queryset=Category.objects.all())])
    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        error_messages= {
            'does_not_exist': 'The seelcted category is not available.',
            'incorrect_type':'the category id is invalid.',
        }
    )
    class Meta:
        model = Product
        # fields = '__all__' # bu sekilde kullanıldıgı vakit "comments" gelmiyor  
        fields = ['id','name','description','price','stock','slug','category']
        
    def validate_price(self, value):
        if value < 0 : 
            raise serializers.ValidationError('Price must be greater that 0.')
        
        if value > 1000000:
            raise serializers.ValidationError('Price seems unusually high.')
        return value
    
    def validate_stock (self, value):
        if value < 0 : 
            raise serializers.ValidationError('Srock cannot be negative.')
        return value
    
    def validate_slug (self, value):
        if self.instace is None :
            if Product.objects.filter(slug = value).exists():
                raise serializers.ValidationError('Slug must be unique.')
        else :
            if Product.objects.filter(slug = value).exclude(pk = self.instance.pk).exists():
                raise serializers.ValidationError('Slug must be unique.')

        if not re.match('^[a-z0-9]+(?:-[a-z0-9]+)*$', value):
            raise serializers.ValidationError('Slug must be lowercase and can only contain hyphens and alphanumeric characters.')
        return value

from rest_framework import serializers
from .models import MenuItem, Category
from decimal import Decimal
#Validator
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator

#Data Sanitization
import bleach



class CategorySerializers(serializers.ModelSerializer):
    
    class Meta:
        
        model = Category
        fields = [
            'id',
            'slug',
            'title',
        ]

#class MenuItemSerializer(serializers.ModelSerializer):

class MenuItemSerializer(serializers.HyperlinkedModelSerializer):

    
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    #category = serializers.StringRelatedField()
    category = CategorySerializers(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    #price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=500)
    
    """ category = serializers.HyperlinkedRelatedField(
        queryset = Category.objects.all(),
        view_name='category-detail'
        ) """
        
        #Method:3 Using validate_field() method 
    """ def validate_price(self, value):
        if (value < 500):
            raise serializers.ValidationError('Price should not be less than 500')
    def validate_stock(self, value):
        if (value < 0):
            raise serializers.ValidationError('Stock cannot be negative') """
            
            
        #Method 4: Using the validate() method 
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        if(attrs['price']<500):
            raise serializers.ValidationError('Price should not be less than 500')
        if(attrs['inventory']<0):
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)

    #title = serializers.CharField(max_length=255,validators=[UniqueValidator(queryset=MenuItem.objects.all())])
    
    """ def validate_title(self, value):
        return bleach.clean(value) """
            
        
    class Meta:

        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        validators = [
            UniqueTogetherValidator(
                queryset=MenuItem.objects.all(),
                fields=['title', 'price']
                ),
            ]
        """ extra_kwargs = {
            'title': {
                'validators': [
                    UniqueValidator(
                        queryset=MenuItem.objects.all()
                        )
                    ]
                }
            } """  
        
        
        """ extra_kwargs = {
            'price': {'min_value': 500},
            'stock':{'source':'inventory', 'min_value': 0}       
            } """
        
        #depth = 1
        
    def calculate_tax(self, product=MenuItem):
        
        return product.price * Decimal(1.1)








""" class MenuItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    inventory = serializers.IntegerField() """
        
        


        

from django.shortcuts import render

from rest_framework import generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializers
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.

@api_view(['GET', 'POST'])
def menu_items(request):
    
    items = MenuItem.objects.select_related('category').all()
    #return Response(items.values())
    serialized_items = MenuItemSerializer(items, many=True, context={'request': request})
    return Response(serialized_items.data)

@api_view(['GET','POST','PUT', 'PATCH'])
def single_item(request, id):
    
    #item = MenuItem.objects.get(pk=id)
    
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category,pk=pk)
    serialized_category = CategorySerializers(category)
    return Response(serialized_category.data) 
    
    
    
    
    

class MenuItemView(generics.ListCreateAPIView):

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    
class CategoryView(generics.ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class SingleCategoryView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializers



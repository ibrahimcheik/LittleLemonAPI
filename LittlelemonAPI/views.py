from django.shortcuts import render

from rest_framework import generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework_csv.renderers import CSVRenderer
from rest_framework_yaml.renderers import YAMLRenderer

#pagination
from django.core.paginator import Paginator, EmptyPage

# Built in Pagination, filtering and sorting
from rest_framework import viewsets

#Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes



class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields=['price','inventory']
    search_fields=['title', 'category__title'] #RelatedModelName_FieldName


@api_view() 
@renderer_classes ([TemplateHTMLRenderer])
def menu(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializer(items, many=True)
    return Response({'data':serialized_item.data}, template_name='menu-item.html')

@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
    return Response(data)


# Create your views here.

@api_view(['GET', 'POST'])
#@renderer_classes([CSVRenderer])
#@renderer_classes([YAMLRenderer])

def menu_items(request):
    if request.method == 'GET':
        
        items = MenuItem.objects.select_related('category').all()        
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering') #/menu-items?ordering=price,inventory.
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price=to_price) # lte = Less Then or Equal to given value
        if search:
            items = items.filter(title_startswith=search) #istartswith, contains, icontains
        if ordering:
            #items = items.order_by(ordering)    
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
            
        paginator = Paginator(items, per_page=perpage) #Test /?perpage=3&page=1
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
            
        serialized_items = MenuItemSerializer(items, many=True, context={'request': request})
        
        return Response(serialized_items.data)
    
    if request.method == 'POST':
        serialized_items = MenuItemSerializer(data=request.data)
        serialized_items.is_valid(raise_exception=True)
        serialized_items.save()
        return Response(serialized_items.data, status.HTTP_201_CREATED)
        
        #return Response(items.values())

        
        
@api_view(['GET','POST','PUT', 'PATCH'])
def single_item(request, id):
    
    #item = MenuItem.objects.get(pk=id)
    
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)


#PERMISSIONS & AUTHAURIZATION

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "Some secret here"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message": "Only Manager should see this"})
    else:
        return Response({"message": "You are not authorizes"}, 403)





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



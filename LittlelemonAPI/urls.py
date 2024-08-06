from django.urls import path
from . import views

urlpatterns = [
    #path('menu-items/', views.menu_items),
    #path('menu-items/<int:id>', views.single_item),
    path('menu-items-generic', views.MenuItemView.as_view()),
    path('menu-items-generic/<int:id>', views.SingleMenuItemView.as_view()),
    
    path('category', views.CategoryView.as_view()),
    path('category/<int:id>', views.SingleCategoryView.as_view()),
    path('category-detail/<int:pk>',views.category_detail, name='category-detail'),
    path('menu',views.menu),
    path('welcome',views.welcome),
    
    path('menu-items/',views.MenuItemsViewSet.as_view({'get':'list'})),
    path('menu-items/<int:pk>',views.MenuItemsViewSet.as_view({'get':'retrieve'})),
    
]


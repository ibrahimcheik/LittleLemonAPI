from django.urls import path
from . import views
#
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #path('menu-items/', views.menu_items),
    #path('menu-items/<int:id>', views.single_item),
    path('secret/', views.secret),
    path('api-token-auth/', obtain_auth_token),
    path('manager-view/', views.manager_view),
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


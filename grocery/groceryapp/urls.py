from rest_framework import views
from .views import *
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls import url
from knox import views as knox_views
from django.urls import path
from groceryapp import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
#for images
from django.conf import settings
from django.conf.urls.static import static


...

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
# from rest_framework_swagger.views import get_swagger_view
# schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('api/register/', RegisterApi.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('products' , ProductView.as_view() ),
    path('productsgeneric' , productsgeneric.as_view() ),
    path('demo' , DemoView.as_view()),
    path('orders/<int:customerId>/<int:productCode>' , OrderView.as_view()), 
    path('ordersgeneric' , ordersgeneric.as_view()),#it will update in cart and delete in orders
    path('delivery' , DeliveryView.as_view()),
    path('deliverygeneric' , deliverygeneric.as_view() ),
    path('cartpost' , cartpost.as_view() ),#for cart post
    path('deliveryAssignedgeneric' , deliveryAssignedgeneric.as_view() ),#for delivery asssigned post
    path('deliveryAddressget' , deliveryaddresspost.as_view() ),#for delivery address post
    path('deliveryAddressget' , deliveryaddressget.as_view() ),#for delivery address get
    path('quantitypost' , quantitypost.as_view() ),#for quantity post
    path('quantityget' , quantityget.as_view() ),#for quantity get
    #path('productstest' , views.productsyerapi ),
    url('ordertest' , views.orderapi ),
    url('cartget' , cartView.as_view()),
    #url('orderdelete' , orderdelete.as_view()),
    url('carttest' , views.cartapi ),
    url('deliverytest' , views.deliveryapi ),
    url('deliveryAssignedtest' , views.deliverAssignedyapi ),

    url('login' , views.LoginAPI ),
    url('register' , views.RegisterApi ),
    path('CaseID/<int:customerId>/<int:productCode>' ,views.getDetailsBasedOnCaseID),
    #path('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # re_path(r'^admin/', admin.site.urls),
    # re_path(r'^api/', include('grocery.urls', namespace='account')),
    # re_path(r'^assess/', include('check.urls', namespace='check')),
    path('productpost', productpost.as_view()),#for product post
    path(r'^productget/(?P<pk>[0-9]+)$', productget.as_view()),#for product get
    path('quantityput/<int:pk>' , quantityput.as_view()), 
    path(r'^deliveryput/(?P<pk>[0-9]+)$', deliveryupdate.as_view()),#for delivery put
    path(r'^deliverassignedyput/(?P<pk>[0-9]+)$', deliveryassignedupdate.as_view()),#get
    url(r'^orderput/(?P<pk>[0-9]+)$', orderupdate.as_view()),#get
    path(r'^deliveryaddressput/(?P<pk>[0-9]+)$', deliveryaddressput.as_view()),#get


]


# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
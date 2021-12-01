from rest_framework import views
from .views import RegisterAPI,LoginAPI,ProductView,DemoView,OrderView,DeliveryView, deliveryassignedupdate, deliveryupdate, ordersgeneric, orderupdate, productget, productpost, productsgeneric,deliverygeneric,deliveryAssignedgeneric
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
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('products' , ProductView.as_view() ),
    path('productsgeneric' , productsgeneric.as_view() ),
    path('demo' , DemoView.as_view()),
    path('orders' , OrderView.as_view()),
    path('ordersgeneric' , ordersgeneric.as_view()),
    path('delivery' , DeliveryView.as_view()),
    path('deliverygeneric' , deliverygeneric.as_view() ),
    path('deliveryAssignedgeneric' , deliveryAssignedgeneric.as_view() ),
    path('productstest' , views.productsyerapi ),
    url('ordertest' , views.orderapi ),
    url('carttest' , views.cartapi ),
    url('deliverytest' , views.deliveryapi ),
    url('deliveryAssignedtest' , views.deliverAssignedyapi ),
    url('login' , views.LoginAPI ),
    url('register' , views.RegisterAPI ),
    #path('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # re_path(r'^admin/', admin.site.urls),
    # re_path(r'^api/', include('grocery.urls', namespace='account')),
    # re_path(r'^assess/', include('check.urls', namespace='check')),
    path('/productpost', productpost.as_view()),
    path(r'^productget/(?P<pk>[0-9]+)$', productget.as_view()),#get
    path(r'^deliveryput/(?P<pk>[0-9]+)$', deliveryupdate.as_view()),#get
    path(r'^deliverassignedyput/(?P<pk>[0-9]+)$', deliveryassignedupdate.as_view()),#get
    path(r'^orderput/(?P<pk>[0-9]+)$', orderupdate.as_view()),#get


]


# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
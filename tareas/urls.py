from django.urls import path
from .views import PedidoApiView
from .views_auth import RegistroApiView, LoginApiView
from .views_perfil import PerfilImagenApiView

urlpatterns = [
    path('pedidos/', PedidoApiView.as_view(), name='pedidos'),
    path('pedidos/<str:id>/', PedidoApiView.as_view(), name='update'),
    path('pedidos/<str:id>/', PedidoApiView.as_view(), name='delete'),

    path('auth/registro/', RegistroApiView.as_view(), name= 'api_registro'),
    path('auth/login/', LoginApiView.as_view(), name= 'api_login'),

    path('perfil/foto/', PerfilImagenApiView.as_view(), name='api_perfil_foto')

]

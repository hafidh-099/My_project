from django.urls import path
from Myapp import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    # path("login/",TokenObtainPairView.as_view()),
    # path("token/refresh/",TokenRefreshView.as_view()),
    path('login/', views.login_view),
    path('home/',views.manage_foodItem),
    path('home/<int:id>/',views.manage_foodItem),
    path('cust/',views.manage_customer),
    path('cust/<int:id>/',views.manage_customer),
    path('confirm_order/', views.confirm_order),
    path('signup/',views.manage_customer),
    path('order/',views.manage_order),
    path('order/<int:id>/',views.manage_order)
]

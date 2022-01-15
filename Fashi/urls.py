"""Fashi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mainApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('checkout/',views.checkoutPage),
    path('confirmation/',views.confirmation),
    path('contact/',views.contactPage),
    path('faq/',views.fagPage),
    path('login/',views.loginPage),
    path("logout/",views.logout),
    path('product/<int:num>/',views.productPage),
    path('register/',views.registerPage),
    path('shop/<str:MC>/<str:SC>/<str:BR>/',views.shopPage),
    path('cart/',views.cartPage),
    path('deleteCart/<int:pid>/',views.deleteCart),
    path("profile/",views.profile),
    path("sellerProfile/",views.sellerProfile),
    path("editProfileSeller/",views.editProfileSeller),
    path("buyerProfile/",views.buyerProfile),
    path("editProfileBuyer/",views.editProfileBuyer),
    path("addProduct/",views.addProduct),
    path("editProduct/<int:num>/",views.editProduct),
    path("deleteWishlist/<int:num>/",views.deleteWishlist),
    path("deleteProduct/<int:num>/",views.deleteProduct),
    path("wishlist/<int:num>/",views.addToWishlist),
    path("search/",views.search),
    path("forgetPassword/",views.forgotPassword),
    path("otp/<str:username>/",views.otp),
    path("resetPassword/<str:username>/",views.resetPassword),
    path("paymentSucesss/<str:rppid>/<str:rpoid>/<str:rpsid>/",views.paymentSuccesss),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

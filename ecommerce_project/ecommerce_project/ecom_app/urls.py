from django.contrib import admin

from .import views
from django.urls import path
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MypasswordResetForm, MypasswordChangeForm, MySetPasswordForm

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('category/<slug:val>/',views.CategoryView.as_view(),name='category'),
    path('category-title/<val>/', views.CategoryTitle.as_view(), name='category-title'),
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('UpdateAddress/<int:pk>/', views.UpdateAddress.as_view(), name='UpdateAddress'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('cart/',views.showcart,name='showcart'),
    path('checkout/',views.checkout.as_view(),name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),
    path('search/', views.search, name='search'),
    path('wishlist/', views.wishlist, name='wishlist'),

    path('pluscart/',views.pluscart),
    path('minuscart/', views.minuscart),
    path('removecart/', views.removecart),
    path('pluswishlist/', views.plus_whishlist),
    path('minuswhishlist/', views.minus_whishlist),
    path('payment/', views.checkout.as_view(), name='checkout'),


    # login Authentification

    path('registration/',views.CustomerRegistrationView.as_view(), name='registration'),
    path('login/',auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=MypasswordResetForm),name='password-reset'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='changepassword.html',form_class=MypasswordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),


    path('password_reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=MypasswordResetForm),name='password_reset'),

    path('password_reset_done',auth_view.PasswordResetView.as_view(template_name='password_reset_done.html', form_class=MypasswordResetForm),name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm),name='password_reset_confirm'),

    path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

]
admin.site.site_header='Diary Product'
admin.site.site_title='Diary Product'
admin.site.site_index_title='Welcome to Diary Product'
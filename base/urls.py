from django.urls import path
from . import views
from .views import EmailLogin , LogoutView , EmailSignup , CreateCompanyAccount
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home , name="home" ),
    path('login/', EmailLogin.as_view() , name="login" ),
    path('logout/', LogoutView.as_view(next_page='login') , name="logout" ),
    path('signup/', EmailSignup.as_view() , name="signup" ),
    
    path('create/company_account', CreateCompanyAccount.as_view() , name="create_company_account" ),
    path('waiting_approval/', views.awaiting_approval , name="awaiting_approval" ),
    path('cart/add_to_cart/<int:product_id>/<int:company_id>/', views.add_to_cart , name="add_to_cart" ),
    path('cart/delete_from_cart/<int:product_id>/<int:company_id>/', views.delete_from_cart , name="delete_from_cart" ),
    path('cart/view/<int:company_id>/', views.cart_view , name="cart_view" ),
    
    
    #admin dashboard
    path('site/admin/pending_approval/', views.admin_approval , name="admin_approval" ),
    path('site/admin/pending_approval/approve/<int:account_id>', views.admin_approval_approve , name="admin_approval_approve" ),
    path('site/admin/pending_approval/archive/<int:account_id>', views.admin_approval_archive , name="admin_approval_archive" ),
    

]

if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

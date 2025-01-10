from django.shortcuts import render , get_object_or_404 , redirect 
from django.http import HttpResponse , Http404 
from django.contrib.auth.views import LoginView , LogoutView 
from django.views.generic.edit import CreateView , FormView
from .forms import EmailSignupForm
from .models import CompanyUser , Product , Cart , CartItem

from django.urls import reverse_lazy , reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin , LoginRequiredMixin
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
import django.contrib.messages as messages
from decimal import Decimal

# Create your views here.
@login_required
def home(request):
    context ={}
    company_account = CompanyUser.objects.filter(user=request.user)

    if company_account.exists() and not(company_account[0].is_approved):
        return redirect(reverse_lazy("awaiting_approval"))
    
    if not company_account.exists():
        return redirect(reverse_lazy("create_company_account"))
    
    try:
        cart=get_object_or_404(Cart , user=request.user , is_active=True)
        products = Product.objects.filter(in_stock = True)
        context = {
        'products':products,
        'company':company_account[0],
        'cart': cart
        }
        return render(request , "base/home.html" , context)
    
    except Http404:
        cart= Cart.objects.create(
        user = request.user,
        brand = company_account[0],
        )
        return redirect(reverse("cart_view" , kwargs={"company_id": company_account[0].id}))

class EmailLogin(LoginView):
    template_name="base/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")


class EmailSignup(UserPassesTestMixin , FormView):
    form_class = EmailSignupForm
    template_name ='base/signup.html'
    success_url = reverse_lazy("create_company_account")

    def test_func(self):
        return not(self.request.user.is_authenticated)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request , user)

        return super().form_valid(form)
    
class CreateCompanyAccount(CreateView , LoginRequiredMixin):
    model=CompanyUser
    fields = ['gstin' , 'brand_name' , 'phone' , 'address']
    template_name="base/create_account.html"

    def form_valid(self, form):
        account = form.save(commit=False)
        account.user = self.request.user
        account.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("home")

@login_required
def awaiting_approval(request):
    company_account = CompanyUser.objects.filter(user=request.user)
    if company_account.exists() and company_account[0].is_approved:
        return redirect(reverse_lazy("home"))
    return render(request , "base/waiting_approval.html")

@login_required
def add_to_cart(request , product_id , company_id):
    company = get_object_or_404(CompanyUser , id=company_id)
    product_template = get_object_or_404(Product , id=product_id)
    cart, cart_created = Cart.objects.get_or_create(
        user = request.user,
        brand = company,
        is_active=True
    )
    cart_item , item_created = CartItem.objects.get_or_create(
        user = request.user ,
        product = product_template
    )

    if not item_created and not cart_created:
        cart.cart_quantity-=cart_item.quantity
    cart_item.quantity += 1
    cart_item.total_amount = Decimal(cart_item.product.price * Decimal(cart_item.quantity)) 

    cart_item.save()

    cart.items.add(cart_item)
    cart.cart_total += cart_item.product.price
    cart.cart_quantity += cart_item.quantity
    cart.save()

    messages.add_message(request , messages.INFO , f"Your Item '{cart_item.product.name}' has been Added to the Cart")
    return redirect(reverse("cart_view" , kwargs={"company_id":company_id}))


@login_required
def delete_from_cart(request , product_id , company_id):
    company = get_object_or_404(CompanyUser , id=company_id)
    product = get_object_or_404(Product , id=product_id)
    
    cart = get_object_or_404( Cart,
        user=request.user,
        brand = company,
        is_active=True
    )

    cart_item = get_object_or_404( CartItem,
        user=request.user,
        product=product_id,
    )

    if cart_item.quantity > 1 :
        cart_item.quantity-= 1
        cart_item.total_amount -= cart_item.product.price
        cart_item.save()
    elif cart_item.quantity <=1:
        cart_item.delete()
    cart.cart_quantity -= 1
    cart.cart_total -= cart_item.product.price
    cart.save() 

    messages.add_message(request , messages.INFO , f"Your Item '{cart_item.product.name}' has been Removed from the Cart")
    return redirect(reverse("cart_view" , kwargs={"company_id":company_id}))


@login_required
def cart_view(request , company_id):
    company = get_object_or_404(CompanyUser , id=company_id)
    if request.user != company.user:
        raise PermissionDenied
    
    cart = Cart.objects.filter(
        user=request.user,
        brand=company,
        is_active=True
    )
    cart_items_count = cart[0].items.count()
    if not(cart.exists()) or cart[0].cart_quantity==0 or cart_items_count==0:
        messages.add_message(request , messages.ERROR , "Cart Empty ! Add Products to Your Cart First")
        return redirect(reverse_lazy("home"))
    context = {
        'cart':cart[0]
    }

    return render(request , "base/cart.html" , context)



#admin approval view
@login_required
def admin_approval(request):
    if not(request.user.is_staff):
        raise PermissionDenied
    else:
        pending_accounts = CompanyUser.objects.filter(is_approved = False).order_by('-created')
        context = {
            'pending_accounts': pending_accounts
        }
        return render(request , "base/admin_approval.html" , context)
    
@login_required
def admin_approval_approve(request , account_id):
    if not(request.user.is_staff):
        raise PermissionDenied
    account = get_object_or_404(CompanyUser , id=account_id)
    account.is_approved = True
    account.save()
    return redirect(reverse_lazy("admin_approval"))
   


@login_required
def admin_approval_archive(request , account_id):
    if not(request.user.is_staff):
        raise PermissionDenied
    account = get_object_or_404(CompanyUser , id=account_id)
    account.is_archived = not(account.is_archived)
    account.save()
    return redirect(reverse_lazy("admin_approval"))

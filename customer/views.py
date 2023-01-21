from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,TemplateView,ListView,DetailView,View
from customer.forms import RegistrationForm,LoginForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from api.models import Products,Carts,Orders
from django.db.models import Sum
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'You Must Login')
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
    return wrapper


desc=[never_cache,signin_required]


class RegistrationView(CreateView):
    template_name='signup.html'
    form_class=RegistrationForm
    success_url=reverse_lazy('signin')

    def form_valid(self, form):
        messages.success(self.request,'Account has been created')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,'Account creation failed')
        return super().form_invalid(form)


class SignInView(FormView):
    template_name='cust-login.html'
    form_class=LoginForm
    
    def post(self, request, *args,**kwargs) :
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,'You are loggedin')
                return redirect('user-home')
            else:
                messages.error(request,'Invalid Credentials')
                return render(request,'cust-login.html' ,{"form":form})



@method_decorator(desc,name='dispatch')
class ProductsListView(ListView):
    template_name='cust-home.html'
    context_object_name='products'
    model=Products




@method_decorator(desc,name='dispatch')
class ProductDetailView(DetailView):
    template_name='cust-productdetail.html'
    context_object_name='product'
    pk_url_kwarg='id'
    model=Products




desc
def add_to_cart(request,*args,**kwargs):
    id=kwargs.get('id')
    product=Products.objects.get(id=id)
    usr=request.user
    Carts.objects.create(user=usr,product=product)
    messages.success(request,'Item has been added to cart')

    return redirect('user-home')


@method_decorator(desc,name='dispatch')
class CartListView(ListView):
    template_name='cart-list.html'
    model=Carts
    context_object_name='carts'
    
    def get(self, request, *args, **kwargs):
        qs=Carts.objects.filter(user=request.user,status='in-cart')
        total=Carts.objects.filter(user=request.user,status='in-cart').aggregate(tot=Sum('product__price'))

        context={'carts':qs,'tot':total}
        return render(request,'cart-list.html',context)

    # def get_queryset(self):
    #     return Carts.objects.filter(user=self.request.user)


@method_decorator(desc,name='dispatch')
class CartDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        obj=Carts.objects.filter(id=id).delete( )
        return redirect('carts-all')



@method_decorator(desc,name='dispatch')
class OrderView(TemplateView):
    template_name='checkout.html'

    def get(self,request,*args,**kwargs):
        pid=kwargs.get('pid')
        qs=Products.objects.get(id=pid)
        return render(request,'checkout.html',{"product":qs})

    def post(self,request,*args,**kwargs):
        pid=kwargs.get('pid')
        cid=kwargs.get('cid')
        cart=Carts.objects.get(id=cid)
        product=Products.objects.get(id=pid)
        user=request.user
        address=request.POST.get('address')
        mobile=request.POST.get('mobile')
        Orders.objects.create(product=product,user=user,address=address,phone=mobile)
        cart.status='order-placed'
        cart.save()
        messages.success(request,'Your item has been placed')
        return redirect('user-home')


@method_decorator(desc,name='dispatch')
class MyOrdersView(ListView):
    model=Orders
    template_name='order-list.html'
    context_object_name='orders'

    def get_queryset(self):
    
        return Orders.objects.filter(user=self.request.user)



desc
def ordercancel(request,*args,**kwargs):
    id=kwargs.get('id')
    Orders.objects.filter(id=id).update(status='cancelled')
    messages.success(request,'Your Order has been Cancelled')
    return redirect('user-home')

def signout(request,*args,**kwargs):
        logout(request)
        return redirect('signin')
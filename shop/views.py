import datetime

from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView
from django.shortcuts import render, redirect
from .models import Merchandise, ShopBuyer, Return, Order
from .froms import UserRegistrationForm, MerchandiseQuantityForm, MerchandiseForm


class ProductView(ListView):
    template_name = 'index.html'
    context_object_name = 'products'
    model = Merchandise
    extra_context = {'form': MerchandiseQuantityForm}

    def post(self, request):
        print('enter post')
        pk = int(request.POST.get('id'))
        quantity = int(request.POST.get('quantity'))
        product = Merchandise.objects.get(id=pk)
        order_value = product.price * quantity
        print(f'buying quantity {quantity}, product {product}, value {order_value} pk is {pk}')
        new_order = Order(
            merchandise=product,
            buyer_id=request.user.id,
            order_quantity=quantity
        )
        if not new_order.is_merchandise_in_stock:
            raise ValidationError('not enough stock to serve your order')
        if not new_order.is_enough_money:
            raise ValidationError('you dont have enough money')
        new_order.save()
        print('new order saved')
        user = ShopBuyer.objects.get(username=request.user)
        user.wallet -= order_value
        user.save()
        print('user wallet ok')
        product.stock -= quantity
        product.save()
        print('product deduct ok')
        return redirect('shop:index')


class OrderHistory(ListView):
    template_name = 'order_history.html'
    model = Order
    context_object_name = 'purchases'

    def get_queryset(self):
        return Order.objects.filter(buyer__username=self.request.user).order_by('-bought_at')

    def post(self, request):
        pk = request.POST['return_id']
        order_to_return = Order.objects.get(id=pk)
        print(datetime.datetime.now())
        print(order_to_return.bought_at)
        print(f'difference {datetime.datetime.now(datetime.timezone.utc) - order_to_return.bought_at}')
        print(f'type {type(datetime.datetime.now(datetime.timezone.utc) - order_to_return.bought_at)}')
        if datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=3) > order_to_return.bought_at:
            print('it is too late')
            raise ValidationError('You cant return this purchase as your time is up')
        print('here we go!')
        Return.objects.create(order_to_return_id=order_to_return.id)
        # message
        # if we try to return the purchase which has already been applied for return try?
        return redirect('shop:order_history')


class CreatePurchaseView(CreateView):
    model = Order


class UserLogin(LoginView):
    # next_page = 'shop:index'
    success_url = '/'


class UserLogout(LogoutView):
    pass


class RegisterUser(CreateView):
    template_name = 'shop/registration/register_user.html'
    model = ShopBuyer
    form_class = UserRegistrationForm

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if ShopBuyer.objects.filter(username=request.POST['username']).exists():
            raise ValidationError('this username is taken, choose another')
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.wallet = 100_000
            new_user.save()
            return redirect('shop:index')
        else:
            raise ValidationError('Wrong data, try again')


class ReviewMerchandise(ListView):
    template_name = 'review_merchandise.html'
    model = Merchandise
    context_object_name = 'merchandises'


class AddMerchandise(CreateView):
    template_name = 'add_merchandise.html'
    model = Merchandise
    form_class = MerchandiseForm


class UpdateMerchandise(UpdateView):
    template_name = 'update_merchandise.html'
    model = Merchandise
    fields = ['name', 'description', 'price', 'picture', 'stock']
    success_url = '/review_merchandise/'


class ReturnedMerchandise(ListView):
    template_name = 'return_merchandise.html'
    model = Return
    context_object_name = 'returns'

    def post(self, request):
        pk = request.POST['return']
        # delete purchase
        # delete return
        return_doc = Return.objects.get(id=pk)
        order_to_cancel = Order.objects.get(id=return_doc.order_to_return_id)
        # return money
        user = ShopBuyer.objects.get(id=order_to_cancel.buyer.id)
        user.wallet += return_doc.order_to_return.get_order_value
        user.save()
        # return goods
        merchandise = Merchandise.objects.get(id=return_doc.order_to_return.merchandise_id)
        merchandise.stock += return_doc.order_to_return.order_quantity
        merchandise.save()
        # delete order (and return as cascade)
        order_to_cancel.delete()
        return redirect('shop:returned_merchandise')


class DeleteMerchandise(DeleteView):
    pass

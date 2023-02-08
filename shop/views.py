import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect
from .models import Merchandise, ShopBuyer, Return, Order
from .froms import UserRegistrationForm, MerchandiseQuantityForm, MerchandiseForm


class RegisterUserView(CreateView):
    template_name = 'shop/registration/register_user.html'
    model = ShopBuyer
    form_class = UserRegistrationForm

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        # if ShopBuyer.objects.filter(username=request.POST['username']).exists():
        #     form.add_error('username', 'this username is taken, choose another')
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.wallet = 1_000_000
            new_user.save()
            messages.add_message(request, messages.SUCCESS, f'user was created and granted {new_user.wallet}$')
            return redirect('shop:login')
        return render(request, 'shop/registration/register_user.html', {'form': form})


class UserLoginView(LoginView):
    """logging user"""
    template_name = 'shop/registration/login.html'

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        if self.request.user.is_staff:
            redirect_to = '/review_merchandise/'
        else:
            redirect_to = '/'
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ""


class UserLogoutView(LogoutView):
    """logout user"""


class ProductView(ListView):
    template_name = 'index.html'
    context_object_name = 'products'
    model = Merchandise
    extra_context = {'form': MerchandiseQuantityForm}
    success_message = 'congratulations, you made a purchase'

    def post(self, request):
        pk = int(request.POST.get('id'))
        quantity = int(request.POST.get('quantity'))
        product = Merchandise.objects.get(id=pk)
        order_value = product.price * quantity
        new_order = Order(
            merchandise=product,
            buyer_id=request.user.id,
            order_quantity=quantity
        )
        bad_news = []
        if not new_order.is_merchandise_in_stock:
            bad_news.append('not enough stock to serve your order')
        if not new_order.is_enough_money:
            bad_news.append('you dont have enough money')
        if bad_news:
            [messages.add_message(request, messages.ERROR, item) for item in bad_news]
            return redirect('shop:index')
        new_order.save()
        user = ShopBuyer.objects.get(username=request.user)
        user.wallet -= order_value
        user.save()
        product.stock -= quantity
        product.save()
        messages.add_message(request, messages.SUCCESS, 'congratulations you place the order')
        return redirect('shop:index')


class OrderHistoryView(LoginRequiredMixin, ListView):
    template_name = 'order_history.html'
    model = Order
    context_object_name = 'purchases'

    def get_queryset(self):
        return Order.objects.filter(buyer__username=self.request.user).order_by('-bought_at')

    def post(self, request):
        pk = request.POST['return_id']
        order_to_return = Order.objects.get(id=pk)
        if datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=3) > order_to_return.bought_at:
            messages.add_message(request, messages.ERROR, 'it is too late, you cannot return the purchase')
        else:
            try:
                Return.objects.create(order_to_return_id=order_to_return.id)
            except IntegrityError:
                messages.add_message(request, messages.ERROR, 'you have already applied for return, please wait')
            else:
                messages.add_message(request, messages.SUCCESS, 'you applied for return, please wait for feedback')
        return redirect('shop:order_history')


class ReviewMerchandiseView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'review_merchandise.html'
    model = Merchandise
    context_object_name = 'merchandises'
    redirect_field_name = reverse_lazy('shop:login')
    # raise_exception = False

    def test_func(self):
        return self.request.user.is_staff


class AddMerchandiseView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    template_name = 'add_merchandise.html'
    model = Merchandise
    form_class = MerchandiseForm
    success_url = reverse_lazy('shop:review_merchandise')
    success_message = 'the merchandise was successfully added'
    redirect_field_name = reverse_lazy('shop:login')

    def test_func(self):
        return self.request.user.is_staff


class UpdateMerchandiseView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    template_name = 'update_merchandise.html'
    model = Merchandise
    fields = ['name', 'description', 'price', 'picture', 'stock']
    success_url = reverse_lazy('shop:review_merchandise')
    success_message = 'the item has been successfully updated'
    redirect_field_name = reverse_lazy('shop:login')

    def test_func(self):
        return self.request.user.is_staff


class ReturnedMerchandiseView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, ListView):
    template_name = 'return_merchandise.html'
    model = Return
    context_object_name = 'returns'
    redirect_field_name = reverse_lazy('shop:login')

    def post(self, request):
        pk_of_return = request.POST.get('accept_return') or request.POST.get('decline_return')
        return_instance = Return.objects.get(id=pk_of_return)
        if 'accept_return' in request.POST:
            order_to_cancel = Order.objects.get(id=return_instance.order_to_return_id)
            user = ShopBuyer.objects.get(id=order_to_cancel.buyer.id)
            user.wallet += return_instance.order_to_return.get_order_value
            user.save()
            merchandise = Merchandise.objects.get(id=return_instance.order_to_return.merchandise_id)
            merchandise.stock += return_instance.order_to_return.order_quantity
            merchandise.save()
            order_to_cancel.delete()
            messages.add_message(request, messages.SUCCESS, 'return accepted (money returned, goods received back')
        if 'decline_return' in request.POST:
            return_instance.delete()
            messages.add_message(request, messages.SUCCESS, 'return declined, record deleted')
        return redirect('shop:returned_merchandise')

    def test_func(self):
        return self.request.user.is_staff



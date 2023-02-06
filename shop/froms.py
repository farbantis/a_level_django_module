from django import forms
from django.core.exceptions import ValidationError

from .models import ShopBuyer, Order, Merchandise


class PurchaseForm(forms.Form):
    pass


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = ShopBuyer
        fields = ['username', 'password', 'password1']

    def clean(self):
        cd = super().clean()
        if cd['password'] != cd['password1']:
            raise ValidationError('passwords dont match', code='invalid')


class MerchandiseQuantityForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_quantity']


class MerchandiseForm(forms.ModelForm):
    class Meta:
        model = Merchandise
        fields = ('name', 'description', 'price', 'picture', 'stock')

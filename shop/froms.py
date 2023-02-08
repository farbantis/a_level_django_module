from django import forms
from django.core.exceptions import ValidationError
from .models import Order, Merchandise, ShopBuyer


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

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise ValidationError('username should be at least 4 characters', code='invalid')
        return username


class MerchandiseQuantityForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_quantity']


class MerchandiseForm(forms.ModelForm):
    class Meta:
        model = Merchandise
        fields = ['name', 'description', 'price', 'picture', 'stock']

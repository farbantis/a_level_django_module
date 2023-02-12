from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib import messages
from .models import Merchandise, Order, ShopBuyer, ShopUser


class ProductViewTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.shop_buyer = ShopBuyer.objects.create(username=self.username, password=self.password, wallet=100)
        self.client.login(username=self.username, password=self.password)
        self.product = Merchandise.objects.create(name='Test Product', price=10, stock=100)
        #self.order = Order.objects.create(merchandise_id=self.product.id, buyer_id=self.shop_buyer.id, order_quantity=10)

    def test_product_view_post_with_sufficient_stock_and_funds(self):
        #browser_response = self.client.post(reverse('shop:index'), {'id': 1, 'quantity': 10})
        #print(browser_response)
        #browser_response = self.client.post(reverse('shop:index'), {'id': self.product.id, 'quantity': 10})
        self.assertEqual(Merchandise.objects.get(id=self.product.id).stock, 100)
        self.assertEqual(ShopBuyer.objects.get(username=self.username).wallet, 100)
        print(self.shop_buyer.id, self.shop_buyer.username, self.shop_buyer.wallet)
        print(self.product.id, self.product.name, self.product.price, self.product.stock)
        # self.assertRedirects(response, reverse('shop:index'))
#         self.assertEqual(len(messages.get_messages(response.wsgi_request)), 1)
#         self.assertEqual(str(messages.get_messages(response.wsgi_request)[0]), 'congratulations you place the order')

    # def test_product_view_post_with_insufficient_stock(self):
    #     response = self.client.post(reverse('shop:index'), {'id': self.product.id, 'quantity': 200})
    #     self.assertRedirects(response, reverse('shop:index'))
    #     self.assertEqual(len(messages.get_messages(response.wsgi_request)), 1)
    #     self.assertEqual(str(messages.get_messages(response.wsgi_request)[0]), 'not enough stock to serve your order')
    #
    # def test_product_view_post_with_insufficient_funds(self):
    #     self.shop_buyer.wallet = 5
    #     self.shop_buyer.save()
    #     response = self.client.post(reverse('shop:index'), {'id': self.product.id, 'quantity': 10})
    #     self.assertRedirects(response, reverse('shop:index'))
    #     self.assertEqual(len(messages.get_messages(response.wsgi_request)), 1)
    #     self.assertEqual(str(messages.get_messages(response.wsgi_request)[0]), 'you dont have enough money')


class LoginViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = ShopBuyer.objects.create_user(username=self.username, password=self.password, email='test@example.com', wallet=100)

    def tearDown(self) -> None:
        self.user.delete()

    def test_correct(self):
        user = authenticate(username=self.username, password=self.password)
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_is_superuser_or_is_staff(self):
        user = authenticate(username=self.username, password=self.password)
        self.assertFalse(user.is_superuser and user.is_staff)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password=self.password)
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username=self.username, password='wrong')
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_normal_user_redirect(self):
        client = Client()
        response = client.post(reverse('shop:login'), {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('shop:index'))

    def test_staff_user_redirect(self):
        self.user.is_staff = True
        self.user.save()
        client = Client()
        response = client.post(reverse('shop:login'), {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('shop:review_merchandise'))

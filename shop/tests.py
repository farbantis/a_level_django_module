from django.contrib.auth import authenticate
from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Merchandise, Order, ShopBuyer
from .views import OrderHistoryView


class OrderHistoryTests(TestCase):
    def setUp(self) -> None:
        product1 = Merchandise.objects.create(
            name='item1',
            description='item1-desc',
            price=10,
            picture='/media/pictures/2023/02/airpods.jpg',
            stock=100
        )
        product2 = Merchandise.objects.create(
            name='item2',
            description='item2-desc',
            price=20,
            picture='/media/pictures/2023/02/airpods1.jpg',
            stock=200
        )
        self.user = ShopBuyer.objects.create(username='testuser', password='testuserpassword', wallet=200)
        Order.objects.create(
            merchandise_id=product1.id,
            buyer_id=self.user.id,
            order_quantity=10
        )
        Order.objects.create(
            merchandise_id=product2.id,
            buyer_id=self.user.id,
            order_quantity=20
        )

    def test_get_queryset(self):
        list_view = OrderHistoryView()
        request = self.client.get(reverse('shop:order_history'))
        request.user = self.user
        list_view.setup(request)

        queryset = list_view.get_queryset()
        self.assertEqual(queryset.count(), 2)
        self.assertEqual(str(queryset[0].merchandise), 'item1')
        self.assertEqual(str(queryset[1].merchandise), 'item2')


class ProductViewTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.wallet = 200
        self.stock = 100
        self.price = 10
        self.order_quantity = 20
        self.shop_buyer = ShopBuyer.objects.create_user(
            username=self.username,
            password=self.password,
            wallet=self.wallet)
        self.product = Merchandise.objects.create(
            name='Test Product',
            price=self.price,
            stock=self.stock,
            picture='/media/pictures/2023/02/airpods.jpg')
        self.order = Order.objects.create(
            merchandise_id=self.product.id,
            buyer_id=self.shop_buyer.id,
            order_quantity=self.order_quantity)
        self.user = ShopBuyer.objects.get(username=self.username)

    def tearDown(self) -> None:
        self.order.delete()
        self.product.delete()
        self.shop_buyer.delete()

    def test_not_enough_stock(self):
        self.order.order_quantity = 1000
        self.assertFalse(self.order.is_merchandise_in_stock)

    def test_enough_stock(self):
        self.assertTrue(self.order.is_merchandise_in_stock)

    def test_not_enough_money(self):
        self.order.buyer.wallet = 199
        self.assertFalse(self.order.is_enough_money)

    def test_is_enough_money(self):
        self.assertTrue(self.order.is_enough_money)

    def test_order_object_creation(self):
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.order.order_quantity, self.order_quantity)
        self.assertEqual(self.product.stock, self.stock)

    # ? тупой тест...
    def test_is_money_deduction_after_order(self):
        self.user.wallet -= self.order.get_order_value
        self.assertEqual(self.user.wallet, self.wallet - self.order.get_order_value)

    def test_is_stock_decreases_after_order(self):
        self.product.stock -= self.order.order_quantity
        self.assertEqual(self.product.stock, self.stock - self.order.order_quantity)


class LoginViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = ShopBuyer.objects.create_user(username=self.username, password=self.password,
                                                  email='test@example.com', wallet=100)

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
        response = self.client.post(reverse('shop:login'), {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('shop:index'))

    def test_staff_user_redirect(self):
        self.user.is_staff = True
        self.user.save()
        response = self.client.post(reverse('shop:login'), {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('shop:review_merchandise'))

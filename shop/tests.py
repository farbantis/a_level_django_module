import factory
from django.contrib.auth import authenticate
from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Merchandise, Order, ShopBuyer
from .views import OrderHistoryView


class ShopBuyerFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'testuser%d' % n)
    password = factory.PostGenerationMethodCall('set_password', 'testpassword')
    email = factory.Faker('email')
    wallet = 200

    class Meta:
        model = ShopBuyer


class MerchandiseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Merchandise
    name = factory.Faker('name')
    description = factory.Faker('text')
    price = 10
    picture = '/media/pictures/2023/02/airpods.jpg'
    stock = 100


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
    merchandise = factory.SubFactory(MerchandiseFactory)
    buyer = factory.SubFactory(ShopBuyerFactory)
    order_quantity = 20


class OrderHistoryTests(TestCase):
    def setUp(self) -> None:
        product1 = MerchandiseFactory(name='item1')
        product2 = MerchandiseFactory(name='item2')
        self.user = ShopBuyerFactory()
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
        self.shop_buyer = ShopBuyerFactory()
        self.product = MerchandiseFactory()
        self.wallet = 200
        self.stock = 100
        self.order_quantity = 20
        self.order = OrderFactory()
        # self.order = Order.objects.create(
        #     merchandise_id=self.product.id,
        #     buyer_id=self.shop_buyer.id,
        #     order_quantity=self.order_quantity)

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

    # ? тупой тест...
    def test_is_money_deduction_after_order(self):
        self.shop_buyer.wallet -= self.order.get_order_value
        self.assertEqual(self.shop_buyer.wallet, self.wallet - self.order.get_order_value)

    def test_is_stock_decreases_after_order(self):
        self.product.stock -= self.order.order_quantity
        self.assertEqual(self.product.stock, self.stock - self.order.order_quantity)


class LoginViewTests(TestCase):
    def setUp(self):
        self.password = 'testpassword'
        self.user = ShopBuyerFactory()

    def tearDown(self) -> None:
        self.user.delete()

    def test_is_superuser_or_is_staff(self):
        user = authenticate(username=self.user.username, password=self.password)
        self.assertFalse(user.is_superuser and user.is_staff)

    def test_normal_user_redirect(self):
        response = self.client.post(reverse('shop:login'), {'username': self.user.username, 'password': self.password})
        self.assertRedirects(response, reverse('shop:index'))

    def test_staff_user_redirect(self):
        self.user.is_staff = True
        self.user.save()
        response = self.client.post(reverse('shop:login'), {'username': self.user.username, 'password': self.password})
        self.assertRedirects(response, reverse('shop:review_merchandise'))

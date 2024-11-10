from django.test import TestCase
from django.contrib.auth.models import User
from pages.models import Farmer, Post
from datetime import datetime, timedelta

class FarmerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

        self.farmer = Farmer.objects.create(
            user=self.user,
            phone="1234567890",
            country="Colombia",
            state="Guajira",
            postal_code=12345
        )

    def test_farmer_creation(self):
        farmer = Farmer.objects.get(pk=self.farmer.id)
        self.assertEqual(farmer.user.username, "testuser")
        self.assertEqual(farmer.country, "Colombia")
        self.assertEqual(farmer.state, "Guajira")
        self.assertEqual(farmer.postal_code, 12345)

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            password='password123'
        )

        self.farmer = Farmer.objects.create(
            user=self.user,
            phone="0987654321",
            country="Colombia",
            state="Amazonia",
            postal_code=67890
        )

        self.post = Post.objects.create(
            farmer=self.farmer,
            name="Manzanas",
            stock=100,
            delivery_date=datetime.now() + timedelta(days=7),
            description="Manzanas frescas",
            fare=150,
            arrival_date=datetime.now() + timedelta(days=8),
            Origin="Leticia",
            Destination="Bogotá"
        )

    def test_post_creation(self):
        post = Post.objects.get(pk=self.post.id)
        self.assertEqual(post.name, "Manzanas")
        self.assertEqual(post.stock, 100)
        self.assertEqual(post.description, "Manzanas frescas")
        self.assertEqual(post.fare, 150)
        self.assertEqual(post.Origin, "Leticia")
        self.assertEqual(post.Destination, "Bogotá")

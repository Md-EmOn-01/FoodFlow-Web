from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from locations.models import Location
from accounts.models import Donor, Recipient

User = get_user_model()


class AccountsModelAndAuthTests(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            address="123 Green Rd",
            area="Dhanmondi",
            city="Dhaka",
            postal_code="1209"
        )

    def test_custom_user_creation_and_roles(self):
        donor_user = User.objects.create_user(
            username="donor1",
            email="donor1@test.com",
            password="password123",
            role=User.ROLE_DONOR,
            phone="+8801700000001"
        )
        self.assertTrue(donor_user.is_donor)
        self.assertFalse(donor_user.is_recipient)

        donor_profile = Donor.objects.create(
            user=donor_user,
            donor_type="restaurant",
            organization_name="Tasty Bites",
            location=self.location,
            is_verified=True
        )
        self.assertEqual(donor_user.donor_profile.organization_name, "Tasty Bites")

        recipient_user = User.objects.create_user(
            username="recipient1",
            email="recipient1@test.com",
            password="password123",
            role=User.ROLE_RECIPIENT,
            phone="+8801700000002"
        )
        self.assertTrue(recipient_user.is_recipient)
        self.assertFalse(recipient_user.is_donor)

        recipient_profile = Recipient.objects.create(
            user=recipient_user,
            recipient_type="ngo",
            location=self.location,
            is_verified=False
        )
        self.assertEqual(recipient_user.recipient_profile.recipient_type, "ngo")

    def test_registration_flow(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newdonor',
            'email': 'newdonor@test.com',
            'phone': '+8801999999999',
            'role': 'donor',
            'donor_type': 'restaurant',
            'organization_name': 'Fresh Eats',
            'address': '45 Lake View',
            'area': 'Gulshan',
            'city': 'Dhaka',
            'postal_code': '1212',
            'password': 'StrongPassword123',
            'password_confirm': 'StrongPassword123',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newdonor')
        self.assertTrue(user.is_donor)
        self.assertEqual(user.donor_profile.organization_name, 'Fresh Eats')
        self.assertEqual(user.donor_profile.location.city, 'Dhaka')

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('create-user')  # reverse looks up the view name
        data = {  # test data to create a user
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], 'failing case')
        # ensure password isn't returned
        self.assertNotIn('password', response.data)

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('create-user')
        data = {
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
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertNotIn('password', response.data)

    def test_create_username_already_exists(self):
        url = reverse('create-user')
        existing_user = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }
        response = self.client.post(url, existing_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], existing_user['username'])

        test_user = {
            'username': 'testuser',
            'email': 'differenttest@test.com',
            'password': 'differenttestpassword',
            'first_name': 'differenttestfirst',
            'last_name': 'differenttestlast'
        }
        test_response = self.client.post(url, test_user, format='json')

        self.assertEqual(test_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', test_response.data)
        self.assertEqual(test_response.data['username'], 'A user with that username already exists.')

    def test_create_blank_username(self):
        url = reverse('create-user')

        test_user = {
            'username': '',
            'email': 'differenttest@test.com',
            'password': 'differenttestpassword',
            'first_name': 'differenttestfirst',
            'last_name': 'differenttestlast'
        }
        response = self.client.post(url, test_user, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'], 'This field may not be blank.')

    def test_get_user(self):
        post_url = reverse('create-user')
        get_url_template = reverse('get-user', args=['{id}'])

        existing_user = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }

        post_response = self.client.post(post_url, existing_user, format='json')

        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        user_id = post_response.data['id']

        get_url = get_url_template.format(id=user_id)

        get_response = self.client(get_url, format='json')

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['username'], existing_user['username'])

    def test_get_user_doesnt_exist(self):
        get_url = reverse('get-user', args=[5])
        get_response = self.client(get_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_users(self):
        post_url = reverse('create-user')
        get_all_url = reverse('get-users')

        existing_user = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }
        response = self.client.post(post_url, existing_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        existing_user2 = {
            'username': 'testuser2',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }
        response2 = self.client.post(post_url, existing_user2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        get_response = self.client(get_all_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

        usernames = [user['username'] for user in get_response.data]
        self.assertIn('testuser', usernames)
        self.assertIn('testuser2', usernames)


class PostTests(APITestCase):
    def test_create_post(self):
        user_url = reverse('create-user')
        post_url = reverse('create-post')

        existing_user = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }

        user_response = self.client.post(user_url, existing_user, format='json')
        self.assertEqual(user_response.status_code, status.HTTP_201_CREATED)

        user_id = user_response.data['id']

        post_data = {
            'title': 'test post title',
            'content': 'This is the content of the test post.',
            'user': user_id
        }

        post_response = self.client.post(post_url, post_data, format='json')

        self.assertEqual(post_response.data['title'], post_data['title'])
        self.assertEqual(post_response.data['content'], post_data['content'])
        self.assertEqual(post_response.data['user'], user_id)

        created_at = post_response.data.get('created_at')
        self.assertIsNotNone(created_at, "'created at' not found.")

    def test_create_post_invalid_user(self):
        post_url = reverse('create-post')

        post_data = {
            'title': 'Test Post Title',
            'content': 'Test content.',
            'user': 5
        }
        response = self.client.post(post_url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)

    def test_create_post_no_title(self):
        user_url = reverse('create-user')
        post_url = reverse('create-post')

        existing_user = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }

        user_response = self.client.post(user_url, existing_user, format='json')
        self.assertEqual(user_response.status_code, status.HTTP_201_CREATED)

        user_id = user_response.data['id']

        post_data = {
            'content': 'Test content',
            'user': user_id
        }
        response = self.client.post(post_url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)

    def test_create_post_no_content(self):
        user_url = reverse('create-user')
        post_url = reverse('create-post')

        existing_user = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }

        user_response = self.client.post(user_url, existing_user, format='json')
        self.assertEqual(user_response.status_code, status.HTTP_201_CREATED)

        user_id = user_response.data['id']

        post_data = {
            'title': 'Test Title',
            'user': user_id
        }
        response = self.client.post(post_url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)
        self.assertEqual(response.data['content'][0], 'This field is required.')

    def test_get_post(self):
        user_url = reverse('create-user')
        post_url = reverse('create-post')

        existing_user = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }
        user_response = self.client.post(user_url, existing_user, format='json')
        self.assertEqual(user_response.status_code, status.HTTP_201_CREATED)

        user_id = user_response.data['id']

        post_data = {
            'title': 'Test Post Title',
            'content': 'This is the content of the post.',
            'user': user_id
        }
        post_response = self.client.post(post_url, post_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        post_id = post_response.data['id']
        get_post_url = reverse('get-post', args=[post_id])
        get_response = self.client.get(get_post_url, format='json')

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['id'], post_id)
        self.assertEqual(get_response.data['title'], 'Test Post Title')
        self.assertEqual(get_response.data['content'], 'This is the content of the post.')
        self.assertEqual(get_response.data['user'], user_id)


class CommentTests(APITestCase):
    def test_create_comment(self):
        user_url = reverse('create-user')
        post_url = reverse('create-post')
        comment_url = reverse('create-comment')

        existing_user = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }

        user_response = self.client.post(user_url, existing_user, format='json')
        self.assertEqual(user_response.status_code, status.HTTP_201_CREATED)

        user_id = user_response.data['id']

        post_data = {
            'title': 'Test Post Title',
            'content': 'This is the content of the test post.',
            'user': user_id
        }

        post_response = self.client.post(post_url, post_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        post_id = post_response.data['id']

        comment_data = {
            'content': 'This is a test comment.',
            'user': user_id,
            'post': post_id
        }

        comment_response = self.client.post(comment_url, comment_data, format='json')
        self.assertEqual(comment_response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(comment_response.data['content'], comment_data['content'])
        self.assertEqual(comment_response.data['user'], user_id)
        self.assertEqual(comment_response.data['post'], post_id)

        created_at = comment_response.data.get('created_at')
        self.assertIsNotNone(created_at, "'created_at' not found.")
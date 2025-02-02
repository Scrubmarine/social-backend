from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserTests(APITestCase):
    def setUp(self):
        self.url = reverse('create-user')
        self.data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }

        self.post_response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)

    def test_create_user(self):
        self.assertEqual(self.post_response.data['username'], self.data['username'])
        self.assertEqual(self.post_response.data['email'], self.data['email'])
        self.assertEqual(self.post_response.data['first_name'], self.data['first_name'])
        self.assertEqual(self.post_response.data['last_name'], self.data['last_name'])
        self.assertNotIn('password', self.post_response.data)

    def test_create_username_already_exists(self):
        data = {
            'username': 'testuser',
            'email': 'differenttest@test.com',
            'password': 'differenttestpassword',
            'first_name': 'differenttestfirst',
            'last_name': 'differenttestlast'
        }
        test_response = self.client.post(self.url, data, format='json')

        self.assertEqual(test_response.status_code, status.HTTP_400_BAD_REQUEST)
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
        self.assertEqual(str(response.data['username'][0]), 'This field may not be blank.')

    def test_get_user(self):
        user_id = self.post_response.data.get('id')
        get_url = reverse('get-user', kwargs={'id': user_id})
        get_response = self.client.get(get_url, format='json')

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data.get('username'), self.post_response.data.get('username'))

    def test_get_user_doesnt_exist(self):
        get_url = reverse('get-user', args=[5])
        get_response = self.client.get(get_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_users(self):
        data2 = {
            'username': 'testuser2',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }
        response2 = self.client.post(self.url, data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        get_all_url = reverse('get-users')
        get_response = self.client.get(get_all_url, format='json')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

        usernames = [user['username'] for user in get_response.data]
        self.assertIn('testuser', usernames)
        self.assertIn('testuser2', usernames)


class PostTests(APITestCase):
    def setUp(self):
        self.user_url = reverse('create-user')
        self.post_url = reverse('create-post')

        self.user_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword',
            'first_name': 'testfirst',
            'last_name': 'testlast'
        }

        self.user_response = self.client.post(self.user_url, self.user_data, format='json')
        self.assertEqual(self.user_response.status_code, status.HTTP_201_CREATED)

        self.user_id = self.user_response.data['id']

        self.post_data = {
            'title': 'Test Post Title',
            'content': 'This is the content of the post.',
            'user': self.user_id
        }

        self.post_response = self.client.post(self.post_url, self.post_data, format='json')
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)

    def test_create_post(self):
        self.assertEqual(self.post_response.data['title'], self.post_data['title'])
        self.assertEqual(self.post_response.data['content'], self.post_data['content'])
        self.assertEqual(self.post_response.data['user'], self.user_id)

        created_at = self.post_response.data.get('created_at')
        self.assertIsNotNone(created_at, "'created at' not found.")

    def test_create_post_invalid_user(self):
        post_data = {
            'title': 'Test Post Title',
            'content': 'Test content.',
            'user': 5
        }

        response = self.client.post(self.post_url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)

    def test_create_post_no_title(self):
        post_data = {
            'content': 'Test content',
            'user': self.user_id
        }
        response = self.client.post(self.post_url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['title'][0]), 'This field is required.')

    def test_create_post_no_content(self):
        post_data = {
            'title': 'Test Title',
            'user': self.user_id
        }
        response = self.client.post(self.post_url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)
        self.assertEqual(response.data['content'][0], 'This field is required.')

    def test_get_post(self):
        post_id = self.post_response.data.get('id')
        get_url = reverse('get-post', kwargs={'id': post_id})
        get_response = self.client.get(get_url, format='json')

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['id'], post_id)
        self.assertEqual(get_response.data['title'], 'Test Post Title')
        self.assertEqual(get_response.data['content'], 'This is the content of the post.')
        self.assertEqual(get_response.data['user'], self.user_id)

    def test_get_posts_by_user(self):
        post_data = {
                'title': 'Another Test Post Title',
                'content': 'This is the content of the post 2.',
                'user': self.user_id
        }

        post_data_list = [self.post_data, post_data]

        post_response = self.client.post(self.post_url, post_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        get_url = reverse('get-posts-by-user', kwargs={'user_id': self.user_id})
        get_response = self.client.get(get_url, format='json')

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

        response_data = get_response.json()
        self.assertEqual(len(response_data), 2)

        for i in range(len(response_data)):
            self.assertEqual(response_data[i]['title'], post_data_list[i]['title'])
            self.assertEqual(response_data[i]['content'], post_data_list[i]['content'])
            self.assertEqual(response_data[i]['user'], post_data_list[i]['user'])


class CommentTests(APITestCase):
    def setUp(self):
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

        self.user_id = user_response.data['id']

        post_data = {
            'title': 'Test Post Title',
            'content': 'This is the content of the test post.',
            'user': self.user_id
        }

        post_response = self.client.post(post_url, post_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        self.post_id = post_response.data['id']

        self.comment_data = {
            'content': 'This is a test comment.',
            'user': self.user_id,
            'post': self.post_id
        }

        self.comment_response = self.client.post(comment_url, self.comment_data, format='json')
        self.assertEqual(self.comment_response.status_code, status.HTTP_201_CREATED)

    def test_create_comment(self):
        self.assertEqual(self.comment_response.data['content'], self.comment_data['content'])
        self.assertEqual(self.comment_response.data['user'], self.user_id)
        self.assertEqual(self.comment_response.data['post'], self.post_id)

        created_at = self.comment_response.data.get('created_at')
        self.assertIsNotNone(created_at, "'created_at' not found.")

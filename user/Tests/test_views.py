from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse

from user import views, serializers

import json

User = get_user_model()


class TestViews(APITestCase):
    '''
        Test Case to test User views
    '''

    def setUp(self):
        '''
            Setup for Tests
        '''
        self.user_range = 5

        self.admin = User.objects.create(
            email='user@mail.com',
            first_name='Test',
            last_name='User',
            gender='Female',
            password='Test@123',
            is_admin=True,
        )

        for iter in range(self.user_range):
            User.objects.create(
                email=f'user{iter}@mail.com',
                first_name=f'Test{iter}',
                last_name='User',
                gender='Male',
                password='Test@123',
            )

        self.forbidden_user = User.objects.create(
            email='unauth@mail.com',
            first_name='Test',
            last_name='User',
            gender='Female',
            password='Test@123',
        )

        self.user_range = self.user_range + 2

        self.client.force_authenticate(user=self.admin)

    def tearDown(self):
        '''
            Cleanup after running Tests
        '''
        self.client.force_authenticate(user=None)

    def test_UserListing(self):
        '''
            Test listing of users Authenticated
        '''
        resp = self.client.get(reverse('user-list-create'))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), self.user_range)

    def test_UserListing_unauthenticated(self):
        '''
            Test Unauthenticated access to User List
        '''
        self.client.force_authenticate(user=None)
        resp = self.client.get(reverse('user-list-create'))

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_UserListing_forbidden(self):
        '''
            Test forbidden access to User List
        '''
        self.client.force_authenticate(user=self.forbidden_user)
        resp = self.client.get(reverse('user-list-create'))

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_UserCreate(self):
        '''
            Test User Creation
        '''
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@email.com',
            'gender': 'Female',
            'password': 'Test@123',
            'confirm_password': 'Test@123'
        }

        resp = self.client.post(reverse('user-list-create'), data)
        created_user = User.objects.get(email=data['email'])

        self.assertEqual(resp.data, {'detail': 'User Created Successfully'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.assertEqual(created_user.email, data['email'])

    def test_UserRetrieve(self):
        '''
            Test Retrieving User
        '''
        resp = self.client.get(
            reverse('user-retrieve-update-destroy', kwargs={'pk': 1}))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertEqual(resp.data['email'], self.admin.email)

    def test_UserUpdate(self):
        '''
            Test Updating User
        '''
        data = {
            'first_name': 'Update',
            'last_name': 'User',
            'email': 'update@user.com',
            'gender': 'Male',
            'password': 'Test@123',
            'confirm_password': 'Test@123'
        }

        self.client.post(reverse('user-list-create'), data)

        update_user = User.objects.get(email='update@user.com')
        resp = self.client.patch(
            reverse('user-retrieve-update-destroy',
                    kwargs={'pk': update_user.id}),
            {'email': 'update1@user.com'})

        updated_resp = self.client.get(
            reverse('user-retrieve-update-destroy',
                    kwargs={'pk': update_user.id}))

        self.assertEqual(resp.data, {'detail': 'User Updated Successfully'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_resp.data['email'], 'update1@user.com')

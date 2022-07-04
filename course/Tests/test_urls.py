from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user import models


class UrlsTest(APITestCase):
    '''
        Test to check if any one can access the 
        course endpoint with admin login credentials
    '''

    def test_urls(self):
        url = reverse('Course-list-create')
        self.testuser1 = models.User.objects.create_superuser(
            email='Test@mail.com',
            password='123456789',
        )
        # self.testuser1.is_staff = True

        self.client.login(
            email='Test@mail.com',
            password='123456789',
        )
        response = self.client.get(url, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APISimpleTestCase


class UrlsTest(APISimpleTestCase):
    '''
        Test to check if any one can access the 
        course endpoint without login credentials
    '''

    def test_urls(self):
        url = reverse('Course-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

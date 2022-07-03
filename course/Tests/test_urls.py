from urllib import response
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APISimpleTestCase
from . import models


class TestUrls(APISimpleTestCase):
    '''
        Test cases to check the status code
    '''

    def test_urls(self):
        url = reverse('Course-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

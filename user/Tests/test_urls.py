from django.urls import reverse, resolve

from rest_framework.test import APISimpleTestCase
from user import views


class TestUrls(APISimpleTestCase):
    '''
        Test cases to resolve urls to their views
    '''

    def test_UserListCreateAPIView_resolves(self):
        url = reverse('user-list-create')
        self.assertEquals(
            resolve(url).func.view_class, views.UserListCreateAPIView)

    def test_UserRetrieveUpdateDestroyAPIView_resolves(self):
        url = reverse('user-retrieve-update-destroy', kwargs={'pk': 1})
        self.assertEquals(
            resolve(url).func.view_class,
            views.UserRetrieveUpdateDestroyAPIView)

    def test_UserPasswordUpdateAPIView_resolves(self):
        url = reverse('user-password-update')
        self.assertEquals(
            resolve(url).func.view_class, views.UserPasswordUpdateAPIView)

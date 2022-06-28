from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestModels(TestCase):
    '''
        Test Case to test User models
    '''

    def test_User_create(self):
        user = User.objects.create(
            profile_image='https://i.pravatar.cc/300',
            email='test@user.com',
            first_name='Test',
            last_name='User',
            gender='Rather not Say',
            password='Test@123',
        )

        fetched_user = User.objects.get(pk=user.id)

        self.assertEqual(user.id, fetched_user.id)
        self.assertEquals(user, fetched_user)
        self.assertEqual(User.objects.count(), 1)

    def test_User_update(self):
        user = User.objects.create(
            profile_image='https://i.pravatar.cc/300',
            email='test@user.com',
            first_name='Test',
            last_name='User',
            gender='Rather not Say',
            password='Test@123',
        )
        updated_user = User.objects.get(pk=user.id)
        updated_user.email = 'updatedtest@user.com'
        updated_user.save()

        updated_user = User.objects.get(pk=user.id)

        self.assertEqual(user.id, updated_user.id)
        self.assertEquals(user, updated_user)
        self.assertEqual(User.objects.count(), 1)

    def test_User_delete(self):
        user = User.objects.create(
            profile_image='https://i.pravatar.cc/300',
            email='test@user.com',
            first_name='Test',
            last_name='User',
            gender='Rather not Say',
            password='Test@123',
        )
        fetched_user = User.objects.get(pk=user.id)

        fetched_user.delete()

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(User.objects.filter(pk=user.id).count(), 0)

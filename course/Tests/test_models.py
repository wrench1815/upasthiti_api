# from rest_framework.test import APITestCase
# from django.test import TestCase
# from course import models
# from user import models


# #! Failed test
# class ModelTest(APITestCase):

#     @classmethod
#     def test_course_create(self):
#         self.testuser1 = models.User.objects.create_superuser(
#             email='Test@mail.com',
#             password='123456789',
#         )
#         # self.testuser1.is_staff = True

#         self.client.login(
#             email='Test@mail.com',
#             password='123456789',
#         )
#         test_course = models.CourseModel.objects.create(
#             course_name='New Course',
#             course_code='100',
#             teacher_assigned=1,
#             is_practical=True,
#             classes=1,
#         )

#         fetched_course = models.CourseModel.objects.get(pk=test_course.id)

#         self.assertEqual(test_course.id, fetched_course.id)
#         self.assertEquals(test_course, fetched_course)
#         self.assertEqual(test_course.objects.count(), 1)

#     # def test_course_content(self):
#     #     course_name=

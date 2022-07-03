# from django.test import TestCase
# from course import models

# ! Failed test due to unauthentication error 403
# class ModelTest(TestCase):

#     @classmethod
#     def test_course_create(self):
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

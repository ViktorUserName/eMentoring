from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f'{self.username} -- ({self.role})'

class Course(models.Model):
    name = models.CharField(max_length=100)

    teachers = models.ManyToManyField(
        User,
        limit_choices_to={'role': 'teacher'},
        related_name='courses',
        blank=True
    )
    def __str__(self):
        return self.name

class TeacherSelection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='teacherselections_as_teacher'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='teacherselections_as_student'
    )

    class Meta:
        unique_together = ('course', 'student')

    def __str__(self):
        return f'{self.course} {self.teacher} {self.student}'


class Lesson(models.Model):
    name = models.CharField(max_length=100)

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'},
                                related_name='lessons')

    def __str__(self):
        return f'{self.name} ({self.student} — {self.teacher})'

class Hometask(models.Model):
    task = models.CharField(max_length=100)

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='hometasks')


class HometaskSubmission(models.Model):
    hometask = models.ForeignKey('Hometask', on_delete=models.CASCADE, related_name='submissions')

    answer_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    grade = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ('hometask', 'student')

    def __str__(self):
        return f'Submission by {self.student} for {self.hometask}'
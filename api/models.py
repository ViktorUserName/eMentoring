from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


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

    def __str__(self):
        return self.name

class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='teacher_profile',
    )
    bio = models.TextField(blank=True)

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teachers'
    )

    def __str__(self):
        return f'TeacherProfile: {self.user.username} - {self.course.name if self.course else "No Course"}'

    def clean(self):
        if self.course:
            existing = TeacherProfile.objects.filter(course=self.course).exclude(id=self.id)
            if existing.exists():
                raise ValidationError("This teacher is already assigned to a course.")


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})


class TeacherSelection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name='assigned_students'
    )
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='teacher_selections'
    )

    class Meta:
        unique_together = ('course', 'student')

    def clean(self):
        if self.teacher.course != self.course:
            raise ValidationError("Teacher must be assigned to this course.")


class Lesson(models.Model):
    name = models.CharField(max_length=100)

    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='teacher_lessons')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return f'{self.name} ({self.student} — {self.teacher})'

class Hometask(models.Model):
    task = models.CharField(max_length=100)

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='hometasks')


class HometaskSubmission(models.Model):
    hometask = models.ForeignKey('Hometask', on_delete=models.CASCADE, related_name='submissions')

    answer_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='hometasks')
    grade = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ('hometask', 'student')

    def __str__(self):
        return f'Submission by {self.student} for {self.hometask}'
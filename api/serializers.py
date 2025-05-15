from rest_framework import serializers

from api.models import Course, TeacherSelection, Lesson, Hometask, HometaskSubmission


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class TeacherSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSelection
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class HometaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hometask
        fields = '__all__'

class HometaskSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HometaskSubmission
        fields = '__all__'

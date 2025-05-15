from rest_framework import serializers

from api.models import Course, TeacherSelection, Lesson, Hometask, HometaskSubmission, TeacherProfile


class TeacherSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSelection
        fields = '__all__'


class TeacherReadSerializer(serializers.ModelSerializer):
    teacher_name = serializers.PrimaryKeyRelatedField(source='user.username', read_only=True)
    course_name = serializers.PrimaryKeyRelatedField(source='course.name', read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ('id', 'teacher_name', 'bio', 'course_name')
        # fields = '__all__'

class TeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = '__all__'



class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'teachers')
        # fields = '__all__'

    def get_teachers(self, obj):
        return [teacher.user.username for teacher in obj.teachers.all()]

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

from rest_framework import serializers

from api.models import Course, TeacherSelection, Lesson, Hometask, HometaskSubmission, TeacherProfile, User, \
    StudentProfile


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

# --------USERS

class UserApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'role', 'course')

    def validate(self, attrs):
        role = attrs.get('role', 'student')
        course = attrs.get('course', None)
        if role == 'teacher' and not course:
            raise serializers.ValidationError('Для роли учителя надо указать курс')
        return attrs

    def create(self, validated_data):
        course = validated_data.pop('course', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'student')
        )
        if user.role == 'teacher':
            TeacherProfile.objects.create(user=user, course=course)
        if user.role == 'student':
            StudentProfile.objects.create(user=user)
        return user

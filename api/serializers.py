from rest_framework import serializers

from api.models import Course, TeacherSelection, Lesson, Hometask, HometaskSubmission, TeacherProfile, User, \
    StudentProfile

# ======USER

class TeacherReadSerializer(serializers.ModelSerializer):
    teacher_name = serializers.PrimaryKeyRelatedField(source='user.username', read_only=True)
    course_name = serializers.PrimaryKeyRelatedField(source='course.name', read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ('id', 'teacher_name', 'bio', 'course_name')

class StudentReadSerializer(serializers.ModelSerializer):
    class TeacherSelectionReadSerializer(serializers.ModelSerializer):
        course_name = serializers.CharField(source='course.name', read_only=True)
        teacher_name = serializers.CharField(source='teacher.user.username', read_only=True)

        class Meta:
            model = TeacherSelection
            fields = ('id', 'course_name', 'teacher_name')

    student_name = serializers.PrimaryKeyRelatedField(source='user.username', read_only=True)
    teacher_selections = TeacherSelectionReadSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = ('id', 'student_name', 'teacher_selections' )

# =========

# ===== Выбор учителя
class TeacherSelectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSelection
        fields = ('teacher',)

    def create(self, validated_data):
        student = self.context['request'].user.studentprofile
        teacher = validated_data['teacher']
        course = teacher.course
        return TeacherSelection.objects.create(
            student=student,
            teacher=teacher,
            course=course,
        )

    def validate(self, attrs):
        teacher = attrs['teacher']
        course = teacher.course
        if not course:
            raise serializers.ValidationError('У учителя не назначен курс')

        return attrs

# =======

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

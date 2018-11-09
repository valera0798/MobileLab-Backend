from rest_framework import serializers

from .models import Skill, Student


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class StudentSerializerSkillsID(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'skills')


class StudentSerializerSkillsIntermediate(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'skills')

    def create(self, validated_data):
        skills_data = validated_data.pop('skills')
        student = Student.objects.create(**validated_data)
        for skill_data in skills_data:
            Skill.objects.create(student=student, **skill_data)
        return student

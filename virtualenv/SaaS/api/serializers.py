from rest_framework import serializers

from .models import *


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name')


class WorkStepStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkStepStatus
        fields = ('id', 'name')


class SuggestionThemeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionThemeStatus
        fields = ('id', 'name')


class SuggestionThemeProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionThemeProgress
        fields = ('id', 'title', 'description', 'date_update')


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


class StudentSerializerNoSkills(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'last_name', 'patronymic', 'description')
        

class CuratorSerializerSkillsID(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Curator
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'skills')


class CuratorSerializerSkillsIntermediate(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Curator
        fields = ('id', 'name', 'last_name', 'patronymic', 'description', 'skills')

    def create(self, validated_data):
        skills_data = validated_data.pop('skills')
        curator = Curator.objects.create(**validated_data)
        for skill_data in skills_data:
            Skill.objects.create(curator=curator, **skill_data)
        return curator


class CuratorSerializerNoSkills(serializers.ModelSerializer):
    class Meta:
        model = Curator
        fields = ('id', 'name', 'last_name', 'patronymic', 'description')


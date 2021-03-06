from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication

from ..models.theme import Theme
from ..models.suggestion import SuggestionTheme, SuggestionThemeStatus, SuggestionThemeProgress
from ..models.curator import Curator
from ..models.work import Work, WorkStep

from ..serializers.curator import CuratorSerializerSkillsIntermediate, CuratorSerializerNoSkills, CuratorSerializerSkillsID
from ..serializers.skill import SkillSerializer
from ..serializers.work import WorkSerializerRelatedID, WorkSerializerRelatedIntermediate, \
    WorkStepSerializer, WorkStepSerializerRelatedID, WorkStepSerializerRelatedIDNoStatus, \
    WorkStepMaterialSerializer, WorkStepMaterialSerializerNoRelated, \
    WorkStepCommentSerializer, WorkStepCommentSerializerNoRelated
from ..serializers.theme import ThemeSerializerRelatedID, ThemeSerializerRelatedIntermediate
from ..serializers.suggestion import \
    SuggestionThemeSerializerRelatedID, SuggestionThemeSerializerRelatedChangeable, SuggestionThemeSerializerRelatedIntermediate, \
    SuggestionThemeSerializerRelatedIDNoProgress, \
    SuggestionThemeProgressSerializer, \
    SuggestionThemeCommentSerializer, SuggestionThemeCommentSerializerNoRelated

from ..permissions.group_curators import IsMemberOfCuratorsGroup


class CuratorBaseViewAbstract:
    """
    Curator base view
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMemberOfCuratorsGroup,)  # TODO Change behavior when student app will be developed

    def get_curator(self, curator_id: int) -> Curator:
        return get_object_or_404(Curator, pk=curator_id)

    def get_related_work(self, curator_id: int, work_id: int) -> Work:
        return get_object_or_404(Work, theme__curator__id=curator_id, pk=work_id)

    def get_related_step(self, curator_id: int, work_id: int, step_id: int) -> WorkStep:
        return get_object_or_404(WorkStep, work__theme__curator__id=curator_id, work_id=work_id, pk=step_id)

    def get_related_theme(self, curator_id: int, theme_id: int) -> Theme:
        return get_object_or_404(Theme, curator__id=curator_id, pk=theme_id)

    def get_related_suggestion(self, curator_id: int, suggestion_id: int) -> SuggestionTheme:
        return get_object_or_404(SuggestionTheme, curator__id=curator_id, pk=suggestion_id)

    def get_related_suggestion_progress(self, curator_id: int, suggestion_id: int) -> SuggestionThemeProgress:
        suggestion = self.get_related_suggestion(curator_id, suggestion_id)
        return get_object_or_404(SuggestionThemeProgress, suggestion=suggestion)


class CuratorBaseView(CuratorBaseViewAbstract, GenericAPIView):
    pass


class CuratorList(CuratorBaseViewAbstract, ListAPIView):
    """
    get:
    READ - List of curators.
    """
    queryset = Curator.objects.all()
    serializer_class = CuratorSerializerNoSkills


class CuratorDetail(CuratorBaseView):
    """
    get:
    READ - Curator instance details.

    put:
    UPDATE - Curator instance details.
    """
    serializer_class = CuratorSerializerSkillsID

    def get(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = CuratorSerializerSkillsIntermediate(curator)
        return Response(serializer.data)

    def put(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = CuratorSerializerSkillsID(curator, data=request.data)
        if serializer.is_valid():
            serializer.update(curator, validated_data=serializer.validated_data)
            # serializing response
            serializer_resp = CuratorSerializerSkillsIntermediate(curator)
            return Response(serializer_resp.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related skills
class CuratorSkillList(CuratorBaseView):
    """
    get:
    READ - List of curator instance related skills.
    """
    def get(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = SkillSerializer(curator.skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# related works
class CuratorWorkList(CuratorBaseView):
    """
    get:
    READ - List of curator instance related works.

    post:
    CREATE - Curator instance related work.
    """
    serializer_class = WorkSerializerRelatedID

    def get(self, request, curator_id):
        curator = self.get_curator(curator_id)
        related_works = []
        for theme in curator.theme_set.all():
            for work in theme.work_set.all():
                related_works.append(work)
        serializer = WorkSerializerRelatedIntermediate(related_works, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CuratorWorkDetail(CuratorBaseView):
    """
    get:
    READ - Curator instance related work.

    put:
    UPDATE - Curator instance related work.

    delete:
    DELETE - Curator instance related work.
    """
    serializer_class = WorkSerializerRelatedID

    def get(self, request, curator_id, work_id):
        work = self.get_related_work(curator_id, work_id)
        serializer = WorkSerializerRelatedIntermediate(work)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, curator_id, work_id):
        work = self.get_related_work(curator_id, work_id)
        serializer = WorkSerializerRelatedID(work, data=request.data)
        if serializer.is_valid():
            serializer.update(work, validated_data=serializer.validated_data)
            # serializing response
            serializer_resp = WorkSerializerRelatedIntermediate(work)
            return Response(serializer_resp.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curator_id, work_id):
        work = self.get_related_work(curator_id, work_id)
        if work.delete():
            # serializing response
            serializer = WorkSerializerRelatedIntermediate(work)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# related work-steps
class CuratorWorkStepList(CuratorBaseView):
    """
    get:
    READ - Curator instance related work steps.

    post:
    CREATE - Curator instance related work step.
    """
    serializer_class = WorkStepSerializerRelatedIDNoStatus

    def get(self, request, curator_id, work_id):
        work = self.get_related_work(curator_id, work_id)
        related_steps = []
        for step in work.step_set.all():
            related_steps.append(step)
        serializer = WorkStepSerializer(related_steps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id, work_id):
        work = self.get_related_work(curator_id, work_id)
        serializer = WorkStepSerializerRelatedIDNoStatus(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["work_id"] = work_id
            step = serializer.create(validated_data=serializer.validated_data)
            work.step_set.add(step)
            # serializing response
            serializer_resp = WorkStepSerializer(step)
            return Response(serializer_resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuratorWorkStepDetail(CuratorBaseView):
    """
    get:
    READ - Curator instance related work step details.

    put:
    UPDATE - Curator instance related work step details.

    delete:
    DELETE - Curator instance related work step.
    """
    serializer_class = WorkStepSerializerRelatedID

    def get(self, request, curator_id, work_id, step_id):
        step = self.get_related_step(curator_id, work_id, step_id)
        serializer = WorkStepSerializer(step)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, curator_id, work_id, step_id):
        step = self.get_related_step(curator_id, work_id, step_id)
        serializer = WorkStepSerializerRelatedID(step, data=request.data)
        if serializer.is_valid():
            serializer.update(step, validated_data=serializer.validated_data)
            # serializing response
            serializer_resp = WorkStepSerializer(step)
            return Response(serializer_resp.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curator_id, work_id, step_id):
        step = self.get_related_step(curator_id, work_id, step_id)
        if step.delete():
            serializer = WorkStepSerializer(step)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# related work-step-materials
class CuratorWorkStepMaterialList(CuratorBaseView):
    """
    get:
    READ - Curator instance related work step materials.

    post:
    CREATE - Curator instance related work step material.
    """
    serializer_class = WorkStepMaterialSerializerNoRelated

    def get(self, request, curator_id, work_id, step_id):
        step = self.get_related_step(curator_id, work_id, step_id)
        related_materials = []
        for material in step.material_set.all():
            related_materials.append(material)
        serializer = WorkStepMaterialSerializer(related_materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id, work_id, step_id):
        step = self.get_related_step(curator_id, work_id, step_id)
        serializer = WorkStepMaterialSerializerNoRelated(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["step_id"] = step_id
            material = serializer.create(validated_data=serializer.validated_data)
            step.material_set.add(material)
            # serializing response
            serializer_resp = WorkStepMaterialSerializer(material)
            return Response(serializer_resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related work-step-comments
class CuratorWorkStepCommentList(CuratorBaseView):
    """
    get:
    READ - Curator instance related work step comments.

    post:
    CREATE - Curator instance related work step comment.
    """
    serializer_class = WorkStepCommentSerializerNoRelated

    def get(self, request, curator_id, work_id, step_id):
        step = self.get_related_step(curator_id, work_id, step_id)
        related_comments = []
        for comment in step.comment_set.all():
            related_comments.append(comment)
        serializer = WorkStepCommentSerializer(related_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id, work_id, step_id):
        step = self.get_related_step(curator_id, work_id, step_id)
        serializer = WorkStepCommentSerializerNoRelated(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["step_id"] = step_id
            comment = serializer.create(validated_data=serializer.validated_data)
            step.comment_set.add(comment)
            # serializing response
            serializer_resp = WorkStepCommentSerializer(comment)
            return Response(serializer_resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related themes
class CuratorThemeList(CuratorBaseView):
    """
    get:
    READ - Curator instance related themes.

    post:
    CREATE - Curator instance related theme.
    """
    serializer_class = ThemeSerializerRelatedID

    def get(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = ThemeSerializerRelatedIntermediate(curator.theme_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = ThemeSerializerRelatedID(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data["student"]:
                serializer.validated_data.pop("student")  # it must be suggested until that!
            theme = serializer.create(validated_data=serializer.validated_data)
            curator.theme_set.add(theme)
            # serializing response
            serializer_resp = ThemeSerializerRelatedIntermediate(theme)
            return Response(serializer_resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuratorThemeDetail(CuratorBaseView):
    """
    get:
    READ - Curator instance related theme details.

    put:
    UPDATE - Curator instance related theme details.

    delete:
    DELETE - Curator instance related theme.
    """
    serializer_class = ThemeSerializerRelatedID

    def get(self, request, curator_id, theme_id):
        theme = self.get_related_theme(curator_id, theme_id)
        serializer = ThemeSerializerRelatedIntermediate(theme)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, curator_id, theme_id):
        theme = self.get_related_theme(curator_id, theme_id)
        serializer = ThemeSerializerRelatedID(theme, data=request.data)
        if serializer.is_valid():
            serializer.update(theme, validated_data=serializer.validated_data)
            # serializing response
            serializer_resp = ThemeSerializerRelatedIntermediate(theme)
            return Response(serializer_resp.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curator_id, theme_id):
        theme = self.get_related_theme(curator_id, theme_id)
        if theme.delete():
            serializer = ThemeSerializerRelatedIntermediate(theme)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# related suggestions
class CuratorSuggestionList(CuratorBaseView):
    """
    get:
    READ - Curator instance related suggestions.

    post:
    CREATE - Curator instance related suggestion.
    """
    serializer_class = SuggestionThemeSerializerRelatedIDNoProgress

    def get(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = SuggestionThemeSerializerRelatedIntermediate(curator.suggestiontheme_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id):
        curator = self.get_curator(curator_id)
        serializer = SuggestionThemeSerializerRelatedIDNoProgress(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["status_id"] = SuggestionThemeStatus.objects.get(name__exact="WAITING_STUDENT").id
            suggestion = serializer.create(validated_data=serializer.validated_data)
            curator.suggestiontheme_set.add(suggestion)
            # serializing response
            serializer_resp = SuggestionThemeSerializerRelatedIntermediate(suggestion)
            return Response(serializer_resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuratorSuggestionDetail(CuratorBaseView):
    """
    get:
    READ - Curator instance related suggestion details.

    put:
    UPDATE - Curator instance related suggestion details.

    delete:
    DELETE - Curator instance related suggestion.
    """
    serializer_class = SuggestionThemeSerializerRelatedChangeable

    def get(self, request, curator_id, suggestion_id):
        suggestion = self.get_related_suggestion(curator_id, suggestion_id)
        serializer = SuggestionThemeSerializerRelatedIntermediate(suggestion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, curator_id, suggestion_id):
        suggestion = self.get_related_suggestion(curator_id, suggestion_id)
        serializer = SuggestionThemeSerializerRelatedChangeable(suggestion, data=request.data)
        if serializer.is_valid():
            serializer.update(suggestion, validated_data=serializer.validated_data)
            # serializing response
            serializer_resp = SuggestionThemeSerializerRelatedIntermediate(suggestion)
            return Response(serializer_resp.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curator_id, suggestion_id):
        suggestion = self.get_related_suggestion(curator_id, suggestion_id)
        if suggestion.delete():
            serializer = SuggestionThemeSerializerRelatedIntermediate(suggestion)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CuratorSuggestionProgressDetail(CuratorBaseView):
    """
    get:
    READ - Curator instance related suggestion progress details.

    put:
    UPDATE - Curator instance related suggestion progress details.
    """
    serializer_class = SuggestionThemeProgressSerializer

    def get(self, request, curator_id, suggestion_id):
        progress = self.get_related_suggestion_progress(curator_id, suggestion_id)
        serializer = SuggestionThemeProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, curator_id, suggestion_id):
        progress = self.get_related_suggestion_progress(curator_id, suggestion_id)
        serializer = SuggestionThemeProgressSerializer(progress, data=request.data)
        if serializer.is_valid():
            serializer.update(progress, validated_data=serializer.validated_data)
            # serializing response
            serializer_resp = SuggestionThemeProgressSerializer(progress)
            return Response(serializer_resp.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# related suggestion-comments
class CuratorSuggestionCommentList(CuratorBaseView):
    """
    get:
    READ - Curator instance related suggestion comments.

    post:
    CREATE - Curator instance related suggestion comment.
    """
    serializer_class = SuggestionThemeCommentSerializerNoRelated

    def get(self, request, curator_id, suggestion_id):
        suggestion = self.get_related_suggestion(curator_id, suggestion_id)
        serializer = SuggestionThemeCommentSerializer(suggestion.comment_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, curator_id, suggestion_id):
        suggestion = self.get_related_suggestion(curator_id, suggestion_id)
        serializer = SuggestionThemeCommentSerializerNoRelated(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["suggestion_id"] = suggestion_id
            comment = serializer.create(validated_data=serializer.validated_data)
            suggestion.comment_set.add(comment)
            # serializing response
            serializer_resp = SuggestionThemeCommentSerializer(comment)
            return Response(serializer_resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.filters import AuthorAndTagFilter, IngredientSearchFilter
from api.pagination import LimitPageNumberPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (IngredientSerializer, CustomUserCreateSerializer,
                             CustomUserSerializer, RecipeSerializer,
                             SubscribeCreateSerializer, TagSerializer)
from recipes.models import (Cart, Favorite, Ingredient, IngredientAmount,
                            Recipe, Tag)
from users.models import Follow, User


class TagsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_class = AuthorAndTagFilter
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return self.add_obj(Favorite, request.user, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return self.delete_obj(Favorite, request.user, pk)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self.add_obj(Cart, request.user, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.delete_obj(Cart, request.user, pk)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientAmount.objects
            .filter(recipe__cart__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount_sum=Sum('amount'))
        )
        pdfmetrics.registerFont(TTFont('Slimamif', 'Slimamif.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('Slimamif', size=24)
        page.drawString(200, 800, 'Список ингредиентов')
        page.setFont('Slimamif', size=16)
        height = 750
        for i, data in enumerate(ingredients, 1):
            name = data['ingredient__name']
            measurement_unit = data['ingredient__measurement_unit']
            amount = data['amount_sum']
            page.drawString(
                75, height, f'<{i}> {name} - {amount}, {measurement_unit}')
            height -= 25

        page.showPage()
        page.save()
        return response

    def add_obj(self, model, user, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = RecipeSerializer(
            data={'user': user.id, 'recipe': recipe.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        get_object_or_404(model, user=user, recipe_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        return CustomUserSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ],
        url_path='subscribe'
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        user = request.user
        if request.method == 'POST':
            serializer = SubscribeCreateSerializer(
                data={
                    'user': user.id,
                    'author': author.id
                },
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = user.follower.filter(author=author)
            if subscription.exists():
                subscription.delete()
                return Response(
                    {'message': 'Вы больше не подписаны на пользователя'},
                    status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя!'},
                status=status.HTTP_400_BAD_REQUEST)

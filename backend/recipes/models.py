from django.core import validators
from django.db import models

from users.models import User

HEX_COLOR_LENGTH = 7
NAME_MAX_LENGTH = 200


class Ingredient(models.Model):
    """Модель ингридиентов"""
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=NAME_MAX_LENGTH,
                                        verbose_name='Единица измерения')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_ingredient')
        ]

    def __str__(self):
        return self.name


hex_color_validator = validators.RegexValidator(
    regex=f'^#{r"[0-9a-fA-F]{6}"}$',
    message='Введите цвет в формате HEX, например, "#RRGGBB"',
)


class Tag(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True,
                            verbose_name='Название тега')
    color = models.CharField(max_length=HEX_COLOR_LENGTH,
                             validators=[hex_color_validator],
                             verbose_name='Цвет в HEX')
    slug = models.SlugField(max_length=NAME_MAX_LENGTH, unique=True,
                            verbose_name='Уникальный слаг')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


MIN_COOKING_TIME = 1
MIN_INGREDIENT_AMOUNT = 1
MAX_COOKING_TIME = 1440
MAX_INGREDIENT_AMOUNT = 30000


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Название рецепта')
    image = models.ImageField(upload_to='recipes/',
                              verbose_name='Картинка рецепта')
    text = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингридиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(
                MIN_COOKING_TIME,
                message='Минимальное время приготовления 1 минута'
            ),
            validators.MaxValueValidator(
                MAX_COOKING_TIME,
                message='Максимальное время приготовления 24 часа'
            ),
        ],
        verbose_name='Время приготовления')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(
                MIN_INGREDIENT_AMOUNT,
                message='Минимальное количество ингридиентов 1'
            ),
            validators.MaxValueValidator(
                MAX_INGREDIENT_AMOUNT,
                message='Максимальное количество ингридиентов 30000'
            ),
        ],

        verbose_name='Количество',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_ingredients_recipe')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite_recipe_for_user')
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_cart_user')
        ]

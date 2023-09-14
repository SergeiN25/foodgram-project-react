from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Follow, User


class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 'first_name', 'last_name',
        'is_staff', 'recipe_count', 'follower_count')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    def recipe_count(self, obj):
        return obj.recipes.count()

    def follower_count(self, obj):
        return obj.follower.count()


admin.site.register(User, UserAdmin)
admin.site.register(Follow)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import User, SlimRole


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "nickname",
        "role_label",
        "is_active",
        "date_joined",
    ]

    list_display_links = ["username", "email"]

    list_filter = [
        "role",
        "is_active",
        "sex",
        "date_of_birth",
        "date_joined",
    ]

    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "nickname",
        "phone",
    ]

    ordering = ["-date_joined"]
    readonly_fields = [
        "last_login",
        "date_joined",
    ]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Персональная информация"), {
            "fields": (
                "avatar",
                "banner_image",
                "first_name",
                "last_name",
                "patronymic",
                "nickname",
                "email",
                "phone",
                "sex",
                "date_of_birth",
                "about_me",
            )
        }),
        (_("Права доступа"), {
            "fields": (
                "role",
                "role_expired",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        (_("Важные даты"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "password1",
                "password2",
                "role",
                "is_staff",
                "is_active",
            ),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")


    @display(description="Роль", label={
        User.Role.STANDARD: "info",
        User.Role.BLOCKED: "danger",
        User.Role.JUNIOR_ADMIN: "warning",
        User.Role.SENIOR_ADMIN: "success",
    })
    def role_label(self, obj):
        return obj.get_role_display()

    def has_module_permission(self, request):
        """Проверяет, есть ли доступ к модулю"""
        if request.user.is_superuser:
            return True
        return request.user.role in [User.Role.JUNIOR_ADMIN, User.Role.SENIOR_ADMIN]

    def has_change_permission(self, request, obj = ...):
        if request.user.is_superuser:
            return True
        return request.user.role in [User.Role.JUNIOR_ADMIN, User.Role.SENIOR_ADMIN]

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.role in [User.Role.JUNIOR_ADMIN, User.Role.SENIOR_ADMIN]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            if request.user.role == User.Role.JUNIOR_ADMIN:
                modified_fieldsets = []
                for name, data in fieldsets:
                    if name == _("Права доступа"):
                        fields = list(data["fields"])
                        if "is_superuser" in fields:
                            fields.remove("is_superuser")
                        if "is_staff" in fields:
                            fields.remove("is_staff")
                        if "groups" in fields:
                            fields.remove("groups")
                        if "user_permissions" in fields:
                            fields.remove("user_permissions")
                        data["fields"] = tuple(fields)
                    modified_fieldsets.append((name, data))
                return tuple(modified_fieldsets)

            elif request.user.role == User.Role.SENIOR_ADMIN:
                modified_fieldsets = []
                for name, data in fieldsets:
                    if name == _("Права доступа"):
                        fields = list(data["fields"])
                        if "is_superuser" in fields:
                            fields.remove("is_superuser")
                        data["fields"] = tuple(fields)
                    modified_fieldsets.append((name, data))
                return tuple(modified_fieldsets)

        return fieldsets

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if request.user.role == User.Role.JUNIOR_ADMIN:
            return qs.exclude(
                Q(role=User.Role.SENIOR_ADMIN) |
                Q(is_superuser=True)
            )

        elif request.user.role == User.Role.SENIOR_ADMIN:
            return qs.exclude(is_superuser=True)

        return qs.none()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            if request.user.role == User.Role.JUNIOR_ADMIN:
                form.base_fields.get("role").choices = SlimRole

        return form

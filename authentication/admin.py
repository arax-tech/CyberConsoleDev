from django.contrib import admin

# Register your models here.

from authentication.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


class UserModelAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'email', 'role', 'created_at')
    list_filter = ('is_admin',)
    fieldsets = (
        ('Users Cridentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'company_name', 'address_first_line', 'address_second_line',
         'address_town_city', 'address_country_code', 'address_country', 'role', 'permissions', 'image')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'role', 'is_admin', 'is_active', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('name', 'email', 'role', 'created_at')
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)

# Remove Groups
admin.site.unregister(Group)

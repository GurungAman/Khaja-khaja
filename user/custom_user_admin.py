from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from user.forms import RegistrationForm

User = get_user_model()


class CustomUserAdmin(UserAdmin):

    add_form = RegistrationForm

    list_display = ('email', 'first_name', 'last_name',
                    'admin', 'staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'middle_name', 'last_name')
    readonly_fields = ['date_joined', 'last_login',]
    filter_horizontal = ()
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'middle_name', 'last_name',)}),
        (('Permissions'), {
            'fields': ('is_active', 'staff', 'admin',),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password', 'password_2')}),
        (('Personal info'), {
         'fields': ('first_name', 'middle_name', 'last_name',)}),
        (('Permissions'), {
            'fields': ('is_active', 'staff', 'admin',),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_admin
        if not is_superuser:
            self.readonly_fields += ['admin']
        return form

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from user.forms import RegistrationAdminForm

User = get_user_model()

class CustomUserAdmin(UserAdmin):

    add_form = RegistrationAdminForm

    list_display = ('email', 'admin', )
    ordering = ('email',)
    search_fields = ('email', 'primary_phone_number')
    readonly_fields = ['date_joined', 'last_login',]
    filter_horizontal = ()
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('email', 'primary_phone_number', 'password',)}),
        (('Permissions'), {
            'fields': ('is_active', 'staff', 'admin', 'is_customer', 'is_restaurant',),
        }),
        (('Dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password', 'password_2')}),
        # (('Permissions'), {
        #     'fields': ('is_active', 'staff', 'admin', 'is_customer', 'is_restaurant',),
        # }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_admin
        if not is_superuser:
            self.readonly_fields += ['admin']
        return form

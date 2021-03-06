from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from customuser.models import Usuario
from customuser.forms import CustomUserChangeForm, CustomUserCreationForm



class UserAdmin(BaseUserAdmin):
    list_display = ('email','es_staff')
    list_filter = ('es_staff',)
    fieldsets = ((None, 
                  {'fields':('email','password')}), 
                  ('Información Personal',{'fields':('primerNombre', 'segundoNombre', 'primerApellido','fechaNacimiento'
                  ,'fechaCreacion')}),
                  ('Permissions',{'fields':('es_staff','es_active', 'es_superuser', 'groups', 'user_permissions')})
                  ,)
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),)
    #form = CustomUserChangeForm
    #add_form = CustomUserCreationForm
    search_fields =('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Usuario, UserAdmin)
admin.site.unregister(Group)
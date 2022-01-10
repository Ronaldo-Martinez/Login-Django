from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_user(self, nombres,email, password = None):
        if not email:
            raise ValueError('El Usuario debe tener un correo')
        
        usuario=self.model(
            email=self.normalize_email(email),
            nombres=nombres,
            password=password
        )

        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_superuser(self, nombres,email, password = None):

        usuario=self.create_user(
            email=self.normalize_email(email),
            nombres=nombres,
            password=password
        )

        usuario.es_staff = True
        usuario.es_superuser=True
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    idUsuario = models.AutoField(primary_key=True, unique=True)
    nombres = models.CharField(db_column='NOMBRES', max_length=60)
    apellidos = models.CharField(db_column='APELLIDOS', max_length=60)
    email = models.EmailField(db_column='EMAIL', max_length=100, blank=True, null=True, unique=True)
    es_active = models.BooleanField(db_column='IS_ACTIVE', default=True)
    es_staff = models.BooleanField(db_column='IS_STAFF', default=False)
    last_login = models.DateField(db_column='LAST_LOGIN', null=True)
    es_superuser = models.BooleanField(db_column='IS_SUPERUSER', default=False)
    fechaNacimiento = models.DateField(db_column='FECHA_NACMIENTO', null=True)
    objects = UsuarioManager()

    USERNAME_FIELD="email"
    NAME_FIELD = "nombres"
    REQUIRED_FIELDS = ['nombres']

    def __str__(self):
        return f'{self.email}'
    
    def has_perm(self,perm,obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.es_staff  
    @property
    def is_active(self):
        return self.es_active
    @property
    def is_superuser(self):
        return self.es_superuser

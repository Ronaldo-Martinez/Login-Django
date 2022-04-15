from cgitb import text
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import datetime

# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_user(self, primerNombre,segundoNombre,email,primerApellido, segundoApellido,password = None):
        if not email:
            raise ValueError('El Usuario debe tener un correo')
        
        #Codigo Usuario
        anio=datetime.datetime.now().date().strftime("%Y")[2:]
        texto=primerApellido[0]+segundoApellido[0]
        texto=texto.lower()
        tamaño=len(Usuario.objects.filter(idUsuario__startswith=texto))
        numeros=tamaño+1
        if numeros < 10:
            numeros="00"+str(numeros)
        elif numeros < 100:
            numeros = "0"+str(numeros)
        codigo=texto+anio+numeros
        print(codigo)
        #Crear usuario
        usuario=self.model(
            idUsuario=codigo,
            email=self.normalize_email(email),
            primerNombre=primerNombre,
            segundoNombre=segundoNombre,
            primerApellido=primerApellido,
            segundoApellido=segundoApellido,
            password=password
        )

        usuario.set_password(password)
        usuario.save()
        return usuario
    
    def create_superuser(self, primerNombre,segundoNombre,primerApellido, segundoApellido,email, password = None):
        usuario=self.create_user(
            email=self.normalize_email(email),
            primerNombre=primerNombre,
            segundoNombre=segundoNombre,
            primerApellido=primerApellido,
            segundoApellido=segundoApellido,
            password=password
        )

        usuario.es_staff = True
        usuario.es_superuser=True
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    idUsuario = models.CharField(primary_key=True,max_length=7,unique=True)
    primerNombre = models.CharField(db_column='PRIMER_NOMBRE', max_length=30, null=True)
    segundoNombre=models.CharField(db_column='SEGUNDO_NOMBRE', max_length=30, null=True)
    primerApellido = models.CharField(db_column='PRIMER_APELLIDO', max_length=30, null=True)
    segundoApellido = models.CharField(db_column='SEGUNDO_APELLIDO', max_length=30, null=True)
    sexo = models.CharField(db_column='SEXO', max_length=1, default='-')
    direccion=models.CharField(db_column='DIRECCION', max_length=120, null=True)
    email = models.EmailField(db_column='EMAIL', max_length=100, blank=True, null=True, unique=True)
    es_active = models.BooleanField(db_column='IS_ACTIVE', default=True)
    es_staff = models.BooleanField(db_column='IS_STAFF', default=False)
    last_login = models.DateField(db_column='LAST_LOGIN', null=True)
    es_superuser = models.BooleanField(db_column='IS_SUPERUSER', default=False)
    fechaCreacion = models.DateTimeField(db_column='FECHA_CREACION', default=timezone.now)
    fechaNacimiento = models.DateField(db_column='FECHA_NACMIENTO', null=True)
    objects = UsuarioManager()

    USERNAME_FIELD="email"
    NAME_FIELD = "primerNombre"
    REQUIRED_FIELDS = ['primerNombre', 'segundoNombre', 'primerApellido','segundoApellido']

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

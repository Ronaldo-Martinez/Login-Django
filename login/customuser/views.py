from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from customuser.models import Usuario

def base(request):

    
    return render(request,"register.html")

def vista_iniciarsesion(request):
    return render(request,"login.html")

@csrf_exempt
def logearse(request):
    data={}
    mensaje=""
    titulo=""
    if request.method =="POST":
        email = request.POST.get("usuario")
        password = request.POST.get("password")
        aux=str(email).find('@') #Si encuentra una @ significa que ha recibido un correo
        data={'titulo':'Estoy en post', 'algo':aux}
        #Si aux
        if aux != -1:
            data={'titulo':'Estoy en correo'}
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                data={'titulo': 'Estas logeado'}
            else:
                data
                data={'titulo': "Contraseña incorrecta"}
        else:
            data={'titulo':'Es no es correo'}
            try:
                correo=Usuario.objects.filter(idUsuario=email).first().email
                user = authenticate(request, email=correo, password=password)
                if user is not None:
                    login(request, user)
                    mensaje="logeado"
                else:
                    data
                    mensaje="contraseña incorrecta"
            except:
                mensaje="Usuario o correo incorrectos"

        data={'titulo': titulo, 'mensaje':mensaje}

        return JsonResponse(data)
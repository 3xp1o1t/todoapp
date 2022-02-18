from rest_framework import generics, permissions 
from .serializers import TodoSerializer,TodoToggleCompleteSerializer 
from todo.models import Todo
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth import authenticate

class TodoListCreate(generics.ListCreateAPIView):
    # Heredar de ListAPIView requiere 2 atributos obligatorios. 
    # El primero: SerializerClass 
    # El segundo: QuerySet.

    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user 

        return Todo.objects.filter(user=user).order_by('-created')

    # Para poder agregar un usuario automaticamente al crear una tarea. 
    # Funciona como un Hook, el cual es llamado antes de que se cree el registro en la DB.
    # Esto debido a que se requiere al momento de crear una tarea por el ForeignKey. 
    def perform_create(self, serializer):
        # serializer mantiene el modelo
        serializer.save(user=self.request.user) 

# Rest_framework provee de una metodo interno (build-in) que permite obtener, editar y eliminar un objeto en una sola funcion.

class TodoRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # El usuario puede editar y eliminar solo sus propios todos.
        return Todo.objects.filter(user=user)
     

class TodoToggleComplete(generics.UpdateAPIView):
    
    serializer_class = TodoToggleCompleteSerializer 
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.completed = not(serializer.instance.completed)
        serializer.save() 

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request) # Datos vienen como dict.
            user = User.objects.create_user(
                username = data['username'],
                password = data['password']
            )
            user.save() 

            token = Token.objects.create(user=user)

            return JsonResponse({'token':str(token)}, status=201)
         
        except IntegrityError:
            return JsonResponse(
                {'error':'username taken. choose another username'}, status=400
            )    

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(
            request,
            username = data['username'],
            password = data['password']
        )
        
        if user is None:
            return JsonResponse(
                {'error':'Unable to login. check username and password'}, status = 400
            )
        else: # Retornar el token de sesion.
            try:
                token = Token.objects.get(user=user)
            except: # Si no esta el token en la DB, crea uno nuevo.
                token = Token.objects.create(user=user)

            return JsonResponse({'token':str(token)}, status = 201)


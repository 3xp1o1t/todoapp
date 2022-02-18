from rest_framework import generics
from .serializers import TodoSerializer
from todo.models import Todo

class TodoListCreate(generics.ListCreateAPIView):
    # Heredar de ListAPIView requiere 2 atributos obligatorios. 
    # El primero: SerializerClass 
    # El segundo: QuerySet.

    serializer_class = TodoSerializer

    def get_queryset(self):
        user = self.request.user 

        return Todo.objects.filter(user=user).order_by('-created')

    # Para poder agregar un usuario automaticamente al crear una tarea. 
    # Funciona como un Hook, el cual es llamado antes de que se cree el registro en la DB.
    # Esto debido a que se requiere al momento de crear una tarea por el ForeignKey. 
    def perform_create(self, serializer):
        # serializer mantiene el modelo
        serializer.save(user=self.request.user) 

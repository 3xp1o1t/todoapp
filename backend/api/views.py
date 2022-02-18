from rest_framework import generics, permissions 
from .serializers import TodoSerializer,TodoToggleCompleteSerializer 
from todo.models import Todo

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

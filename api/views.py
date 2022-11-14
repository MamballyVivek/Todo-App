from argparse import Action
from pickle import TRUE
from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.models import Todos, models
from api.serializers import TodoSerializer,RegistrarionSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
class TodoView(ViewSet):
    def list(self,request,*arg,**kw):
       qs=Todos.objects.all()
       Serializer=TodoSerializer(qs,many=True)
       return Response(data=Serializer.data)
    def create(self,request,*arg,**kw):
        Serializer=TodoSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response (data=Serializer.data)
        else:
            return Response(data=Serializer.errors)
    def retrieve(self,request,*arg,**kw):
        
        id=kw.get("pk")
        qs=Todos.objects.get(id=id)
        Serializer=TodoSerializer(qs,many=False)
        return Response(data=Serializer.data)
    def distroy(self,request,*arg,**kw):
        id=kw.get("pk")
        qs=Todos.objects.get(id=id).delete()
        return Response(data="deleted")
    def update(self,request,*arg,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        Serializer=TodoSerializer(data=request.data,instance=object)
        if Serializer.is_valid():
            Serializer.save()
            return Response(data=Serializer.data)
        else:
            return Response(data=Serializer.errors)

class TodosModelView(ModelViewSet):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)
    def create(self, request, *args, **kwargs):
        Serializer = TodoSerializer(data=request.data,context={"user":request.user})
        if Serializer.is_valid():
            Serializer.save()
            return Response (data=Serializer.data)
        else:
            return Response(Serializer.errors)
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
        
    # def create(self, request, *args, **kwargs):
    #     Serialaizer=TodoSerializer(data=request.data)
    #     if Serialaizer.is_valid():
    #        Todos.objects.create(**Serialaizer.validated_data,user=request.user)
    #        return Response(data=Serialaizer.data)
    #     else:
    #         return Response(data=Serialaizer.errors)


       

    serializer_class = TodoSerializer
    queryset=Todos.objects.all()
    @action(methods=["GET"],detail=False)
    def pendingTodos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False)
        Serializer=TodoSerializer(qs,many=True)
        return Response(data=Serializer.data)
    @action(methods=["GET"],detail=False)    
    def completedTodos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=True)
        Serializer=TodoSerializer(qs,many=True)
        return Response(data=Serializer.data)
    @action(methods=["POST"],detail=True)
    def mark_as_done(self,request,*arg,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        object.status=True
        object.save()
        Serializer=TodoSerializer(object,many=False)
        return Response(data=Serializer.data)
class UserView(ModelViewSet):
    serializer_class = RegistrarionSerializer
    queryset=User.objects.all()

    # def create(self,request,*arg,**kw):
    #     Serializer=RegistrarionSerializer(data=request.data)
        
    #     if Serializer.is_valid():
    #         usr=User.objects.create_user(**Serializer.validated_data)
    #         return Response(data=Serializer.data)
    #     else:
    #         return Response(Serializer.errors)



  
     
from django.shortcuts import render
from rest_framework import generics ,permissions
from .serializers import *
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.views import APIView
from django.http import JsonResponse

class register(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = Response({
        "user": user_serializer(user, context=self.get_serializer_context()).data,
        })
        return response

class logine(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        response = super(logine, self).post(request, format=None)
        response.set_cookie("login_token",response.data["token"],path="/",max_age=3600*24*365,samesite='Lax')
        response.data['id'] = user.id
        return response


class machine_AddDelete(APIView):
    # Get info about all machine & their maintenance
    def get(self , request): 
        all_machines = machine.objects.all()
        machines_data=[]
        for i in all_machines:
            machineMaint = maintenance.objects.filter(machine_id=i.id)
            machineMaint_Sr = MaintenanceSerializer(machineMaint , many=True).data
            machine_Sr = machineSerializer(i).data
            machines_data.append({
                "machine" :machine_Sr,
                "maintenance_info":machineMaint_Sr
            })

        return Response(machines_data, status=200)

    # Create a new machine 
    def post(self , request):
        machineSr = machineSerializer(data = request.data )
        if machineSr.is_valid() : 
            machineSr.save()
            return Response(status=201)
        else : 
            return Response(machineSr.errors , status = 400)


class machine_managment(APIView):
    # Get info about specific machine & its maintenance
    def get(self , request , id):
        try : 
            machine_ = machine.objects.get(id=id)
            machineMaint = maintenance.objects.filter(machine_id=id)
            machineMaint_Sr = MaintenanceSerializer(machineMaint , many=True).data
            machine_Sr = machineSerializer(machine_).data
            machines_data = {
                "machine" :machine_Sr,
                "maintenance_info":machineMaint_Sr
            }

            return Response(machines_data, status=200)
        except machine.DoesNotExist : 
            return Response({"Detials":"Machine Does Not Exist"}, status=200)
        
    # update the infos of a specific machine by its ID ( we hould do it to analyse history when problems happend)
    def put(self , request, id):
        try : 
            machine_ = machine.objects.get(id=id)
            serializer = machineSerializer(machine_ , data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status = 200)
        except machine.DoesNotExist : 
            return Response({"Detials":"Machine Does Not Exist"}, status=400)
    # we won't delete the machine from the DB but it will be archived 
    def delete(self , request , id ):
        pass
from django.shortcuts import render
from rest_framework import generics ,permissions
from .serializers import *
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


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


@csrf_exempt 
def callback_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data_to_modify = data.copy()
        robot_type = data["machine_id"].split("_")
        print(data)
        if "welding" in robot_type:
            print(data["timestamp"])
            keys_to_delete = ["timestamp", "vibration_level", "weld_temperature", "power_consumption"]
            for key in keys_to_delete:
                if key in data_to_modify:
                    del data_to_modify[key]
            machine.objects.filter(machine_name=data["machine_id"]).update(timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")),
                                                                            machine_type="WeldingRobot", 
                                                                            vibration_level=data["vibration_level"],
                                                                            temperature=data["weld_temperature"] ,
                                                                            power_consumation=data["power_consumption"] ,
                                                                            sensor_data=str(data_to_modify))  
        elif "cnc" in robot_type:
            print(data["timestamp"])
            keys_to_delete = ["timestamp", "vibration_level", "temperature", "power_consumption"]
            for key in keys_to_delete:
                if key in data_to_modify:
                    del data_to_modify[key]
            machine.objects.filter(machine_name=data["machine_id"]).update(timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")),
                                                                            machine_type="CNC_Machine", 
                                                                            vibration_level=data["vibration_level"],
                                                                            temperature=data["temperature"] ,
                                                                            power_consumation=data["power_consumption"] ,
                                                                            sensor_data=str(data_to_modify)) 
        
        elif "leak" in robot_type:
            print(data["timestamp"])
            keys_to_delete = ["timestamp", "test_pressure", "temperature", "leak_rate"]
            for key in keys_to_delete:
                if key in data_to_modify:
                    del data_to_modify[key]
            machine.objects.filter(machine_name=data["machine_id"]).update(timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")),
                                                                            machine_type="LeakTestMachine", 
                                                                            vibration_level=data["test_pressure"],
                                                                            temperature=data["temperature"] ,
                                                                            power_consumation=data["leak_rate"] ,
                                                                            sensor_data=str(data_to_modify)) 
            
        elif "agv" in robot_type:
            print(data["timestamp"])
            keys_to_delete = ["timestamp", "vibration_level", "temperature", "speed"]
            for key in keys_to_delete:
                if key in data_to_modify:
                    del data_to_modify[key]
            machine.objects.filter(machine_name=data["machine_id"]).update(timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")),
                                                                            machine_type="AGV", 
                                                                            vibration_level=data["vibration_level"],
                                                                            temperature=data["temperature"] ,
                                                                            power_consumation=data["speed"] ,
                                                                            sensor_data=str(data_to_modify)) 
        return JsonResponse({'status': 'success', 'data': data})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



class Task_managment(APIView):
    def get(self , request):
        all_tasks = task.objects.all()
        serializer = taskSerializer(all_tasks, many=True)
        return Response(serializer.data, status=200)
    def post(self , request):
        serializer = taskSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=201)
        else :
            return Response(serializer.errors, status=400)

class task_affection(APIView):
    def post(self , request , id ): #user_id
            task_ = request.data["task"]
            print(task_)
            task_ = task.objects.get(id=task_)
            worker_task = task_user.objects.create(User_id=User.objects.get(id=id) , task_id=task_ , state="pending")
            worker_task.save()
            serializer = taskUserSerializer(worker_task)
            return Response(serializer.data , status = 201)
        
class Task_managment_user(APIView):
    def get(self , request , id): #user id 
        tasks_ = task_user.objects.filter(User_id=id)
        serializer = taskUserSerializer(tasks_,many=True)
        return Response(serializer.data , status=200)
    def put(self , request , id):# task id 
        try : 
            task_ = task_user.objects.get(task_id=id)
            serializer = taskUserSerializerSimple(task_, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status = 200)
            else : 
                return Response(serializer.errors , status = 400)
        except task_user.DoesNotExist : 
            return Response({"Details":"Task Does Not Exist"}, status=400)
        
class Notifications(APIView):
    def post(self, request):
        # Create a new device to recieve notification
        pass
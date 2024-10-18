from django.db import models
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()
class user_data(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20)
    role = models.CharField(max_length=20 , choices=(
        ("Manager" , "Manager"),
        ("Worker" , "Worker")
    ))
    def __str__(self):
        return self.user_data
class task(models.Model):
    task_name=models.CharField(max_length=100)
    task_description = models.TextField()
    task_deadline = models.DateTimeField()
    task_type = models.CharField(max_length=20 , choices=(('routine','routine'),('urgent' , 'urgent'),('simple' , 'simple')))
    def __str__(self):
        return self.task_name
class task_user(models.Model):
    task_id = models.ForeignKey(task , on_delete=models.CASCADE)
    User_id = models.ForeignKey(User , on_delete=models.CASCADE)
    state = models.CharField(max_length=20 , choices=(('pending','pending'),('in progress' , 'in progress') , ('done' , 'done')))

class machine(models.Model):
    machine_types = (('WeldingRobot', 'Welding Robot'),
                     ('StampingPress', 'Stamping Press'),
                     ('PaintingRobot', 'Painting Robot'),
                     ('AGV', 'Automated Guided Vehicle'),
                     ('CNC_Machine', 'CNC Machine'),
                     ('LeakTestMachine', 'Leak Test Machine')
                    )
    machine_name = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    machine_type = models.CharField(max_length=30,choices=machine_types)
    vibration_level = models.FloatField(default=0.0)
    temperature = models.IntegerField()
    power_consumation = models.FloatField()
    #we store the addtionnal json data as text and than parse it in the response (to make db scalable & structured)
    sensor_data = models.TextField(blank=True) 
    def __str__(self):
        return self.machine_type 

class maintenance(models.Model):
    machine_id = models.ForeignKey(machine , on_delete=models.CASCADE)
    description = models.TextField()
    cost = models.FloatField()
    maintenance_date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return self.machine_id.machine_type
from rest_framework import serializers
from .models import  Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields =['name',
                  't_description' ,
                  'asignedto',
                  'start_time',
                  'expected_end',
                  'status',
                  'status2',
                  'project'] 
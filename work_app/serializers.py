from rest_framework import serializers

from work_app.models import jobs
# from work_app.models import jobs

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = jobs
        fields = ['position','company', 'level' , 'salary', 'contact_email', 'description']


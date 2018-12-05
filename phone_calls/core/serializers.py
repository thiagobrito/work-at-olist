from phone_calls.core.models import *

from rest_framework import serializers

'''
    id = models.IntegerField(primary_key=True)
    type = models.CharField('type', max_length=12)
    time_stamp = models.DateTimeField()
    call_id = models.IntegerField()
    source = models.CharField()
    destination = models.TextField()
'''


class PhoneRecordSerializer(serializers.Serializer):
    class Meta:
        model = PhoneRecord
        fields = ('id', 'type', 'time_stamp', 'call_id', 'source', 'destination')

    def create(self, validated_data):
        return PhoneRecord.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.type = validated_data.get('type', instance.type)
        instance.time_stamp = validated_data.get('time_stamp', instance.time_stamp)
        instance.call_id = validated_data.get('call_id', instance.call_id)
        instance.source = validated_data.get('source', instance.source)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.save()
        return instance

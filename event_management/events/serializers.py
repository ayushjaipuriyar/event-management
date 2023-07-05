from rest_framework import serializers
from .models import Event, Registration, Category
from venues.models import Venue
from django.utils import timezone
from datetime import datetime
from django import forms


class EventSerializer(serializers.ModelSerializer):
    venue = serializers.SlugRelatedField(
        slug_field='name', queryset=Venue.objects.all())
    categories = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        current_time = timezone.now()

        if end_time and start_time and end_time <= start_time:
            raise serializers.ValidationError(
                "The end time must be after the start time.")
        if start_time and start_time <= current_time:
            raise serializers.ValidationError(
                "The start time must be greater than the current time.")
        if end_time and end_time <= current_time:
            raise serializers.ValidationError(
                "The end time must be greater than the current time.")
        venue_name = attrs.get('venue')
        capacity = attrs.get('capacity')

        try:
            venue = Venue.objects.get(name=venue_name)
        except Venue.DoesNotExist:
            raise serializers.ValidationError("Invalid venue specified.")

        if capacity is not None and capacity > venue.capacity:
            raise serializers.ValidationError(
                "The event capacity exceeds the venue's capacity.")
        if start_time and end_time:
            conflicting_events = Event.objects.filter(
                venue=venue,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if self.instance:
                conflicting_events = conflicting_events.exclude(
                    pk=self.instance.pk)

            if conflicting_events.exists():
                raise serializers.ValidationError(
                    "Conflicting events found at the same venue.")
        return attrs

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        event = Event.objects.create(**validated_data)
        event.categories.set(categories_data)
        return event


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ['event', 'user']

    def __init__(self, *args, **kwargs):
        is_admin = kwargs['context'].get('is_admin', False)
        super().__init__(*args, **kwargs)

        if is_admin:
            self.fields['status'].read_only = False

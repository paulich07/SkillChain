from rest_framework import serializers
from .models import User, Event, BadgeNFT, AwardNFT
from rest_framework.serializers import ModelSerializer

class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email",  'first_name', 'last_name', 'address', 'imgURI', 'creationDate']
        extra_kwargs = {"password": {"write_only": True}}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'address' 'imgURI', 'creationDate']

class BadgeNFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeNFT
        fields = '__all__'

class AwardNFTSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Mostra i dati dell'utente associato

    class Meta:
        model = AwardNFT
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    awards = AwardNFTSerializer(many=True, read_only=True)
    badges = BadgeNFTSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        # Prüfe, ob beide Passwörter identisch sind
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Die Passwörter stimmen nicht überein."})
        return attrs

    def create(self, validated_data):
        # Entferne das zweite Passwort-Feld, da es nicht für die Erstellung benötigt wird
        validated_data.pop('password2')
        # Erstelle einen neuen Benutzer mit den validierten Daten
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

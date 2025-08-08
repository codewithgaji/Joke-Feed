from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token



class SignupSerializer(serializers.ModelSerializer):
  email = serializers.CharField(max_length=20)
  password = serializers.CharField(min_length=6)
  username = serializers.CharField(max_length=15)
    
  class Meta:
    model = User
    fields = [
       'email', 'username', 'password'
    ]

  def validate(self, attrs):
    email_exist = User.objects.filter(email = attrs['email']).exists()

    if email_exist:
      raise ValidationError("Email has already being used!")
    
    return super().validate(attrs)
  
  def create(self, validated_data):

    user = super().create(validated_data)
    password = validated_data.pop('password')

    user.set_password(password)
    user.save()

    Token.objects.create(user=user)


    return user
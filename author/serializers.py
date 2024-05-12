from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name' ,'email' , 'password', 'confirm_password']
    
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']

        if password != password2:
            raise serializers.ValidationError({'error': "Password Doesn't Matched"})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email already exists"})
        account = User(username = username, first_name = first_name ,last_name = last_name, email = email)
        print(account)
        account.set_password(password)
        account.is_active = False
        account.save()
        return account
        
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)



class UserTokenSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = Token
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = User
        fields = '__all__'


class UserAccountSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.UserAccount
        fields = '__all__'


class UpdateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name' ,'email']
    
    def save(self, author):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        user_auth=None
        profile_user = User.objects.all()
        for auth in profile_user:
            if auth.username == author:
                user_auth = auth

        # usernameLen = len(User.objects.filter(username=username))
        # emailLen = len(User.objects.filter(email=email))
        user_auth.username = username
        user_auth.first_name = first_name
        user_auth.last_name = last_name
        user_auth.email = email
        user_auth.save()
        
       
        return user_auth
    

from django.contrib.auth.hashers import check_password
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['old_password', 'new_password']
    
    def save(self, author):
        old_password = self.validated_data['old_password']
        new_password = self.validated_data['new_password']

        user_auth=None
        profile_user = User.objects.all()
        for auth in profile_user:
            if auth.username == author:
                user_auth = auth
        # print('>>>>>>>>>>>>>>>>>>>>>>',user_auth.password)
        if check_password(old_password, user_auth.password):
            user_auth.set_password(new_password)
            user_auth.save()
        else:
            print('Invalid password')

        return user_auth
    



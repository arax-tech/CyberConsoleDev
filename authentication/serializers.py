from rest_framework import serializers
from authentication.models import User

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from authentication.utils import Util

import os

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    # We are writing this because we need confirm password field in our Registratin Request
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)


    class Meta:
        model = User
        fields=['email', 'name', 'password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
        

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password confirmation does not match...")
        return attrs
  

    # Create user
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'company_name', 'email', 'role','address_first_line', 'address_second_line', 'address_town_city', 'address_country_code', 'address_country', 'image','last_login', 'permissions', 'created_at']


class UserUpdateProfileSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=255,style={'input_type': 'text'}, write_only=True)
    email = serializers.CharField(max_length=255,style={'input_type': 'text'}, write_only=True)
    company_name = serializers.CharField(max_length=255,style={'input_type': 'text'}, write_only=True)
    address_first_line = serializers.CharField(max_length=255,style={'input_type': 'text'}, write_only=True)
    address_second_line = serializers.CharField(max_length=255,style={'input_type': 'text'}, write_only=True)
    address_town_city = serializers.CharField(max_length=255,style={'input_type': 'text'}, write_only=True)
    address_country_code = serializers.CharField(max_length=255,style={'input_type': 'text'}, write_only=True)
    address_country = serializers.CharField(max_length=255,style={'input_type': 'text'}, write_only=True)
    image = serializers.ImageField(max_length=255,style={'input_type': 'file'}, write_only=True)

    class Meta:
        fields = ['name', 'email', 'company_name']

    def validate(self, attrs):

        user = self.context.get('user')

        user.name = attrs.get('name')
        user.email = attrs.get('email')
        user.company_name = attrs.get('company_name')
        user.address_first_line = attrs.get('address_first_line')
        user.address_second_line = attrs.get('address_second_line')
        user.address_town_city = attrs.get('address_town_city')
        user.address_country_code = attrs.get('address_country_code')
        user.address_country = attrs.get('address_country')
        user.image = attrs.get('image')
        user.save()
        return attrs
    

class UserUpdatePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=255,style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type': 'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password confirmation does not match...')
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            # print ('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            # print ('Password Reset Token', token)
            link = 'http://localhost:3000/password/reset/' + uid + '/' + token 
            # print ('Password Reset Link', link)

      # Send EMail

            body = 'Your password reset token  is 👇 \n\n' + link + '\n\n\nIf you have not requested this email then, please ignore this email... \n\n\nRegard BroadBand9'
            data = {'subject': 'Reset Your Password', 'body': body, 'to_email': user.email}

            Util.send_email(data)

            return attrs
        else:
            raise serializers.ValidationError('User not found with this email...')
            

class SendPasswordUpdateEmailSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            # print ('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            # print ('Password Reset Token', token)
            link = 'http://localhost:3000/password/update/' + uid + '/' + token
            # print ('Password Reset Link', link)

      # Send EMail

            body = 'Update Your password client then link below 👇 \n\n' + link + \
                '\n\n\nYou are register in CyberConsole... \n\n\nRegard BroadBand9'
            data = {'subject': 'Update Your password',
                    'body': body, 'to_email': user.email}

            Util.send_email(data)

            return attrs
        else:
            raise serializers.ValidationError(
                'User not found with this email...')




class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password confirmation does not match...")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('Token is not Valid or Expired...')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired...')
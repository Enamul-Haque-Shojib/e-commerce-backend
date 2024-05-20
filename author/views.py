from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, filters, pagination


class UploadProfileView(APIView):

    # def get(self, request, *args, **kwargs):
    #     posts = models.UserAccount.objects.all()
    #     serializer = serializers.UserAccountSerializer(posts, many=True)
    #     return Response(serializer.data)

    def post(self, request):

        author = request.data.get('author')
        profile_image = request.data.get('profile_image')

        user_auth=None
        profile_user = User.objects.all()
        for auth in profile_user:
            if auth.username == author:
                user_auth = auth

        user_profile, created = models.UserAccount.objects.get_or_create(user=user_auth)
        print('>>>>>>>>>>>>>>>>>>>>>',user_profile, created)
        print('>>>>>>>>>>>>>>>>>>>>>',user_profile, created)

        user_profile.user = user_auth  # Update username if provided
        if profile_image:
            user_profile.profile_image = profile_image
        user_profile.save()

        serializer = serializers.UserAccountSerializer(user_profile)
        return Response(serializer.data)
    

from django.core.mail import send_mail
from django.utils.crypto import get_random_string


class ResetPasswordEmailView(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        
        auth = User.objects.filter(email=email).first()
        # print('>>>>>>>>>>>>>>>>>>>>>',auth.pk)
        if auth:
            uidb64 = urlsafe_base64_encode(force_bytes(auth.pk))
            # token = get_random_string(length=32)
            token = default_token_generator.make_token(auth)
            send_mail(
                'Password Reset',
                f'Click the link to reset your password: http://localhost:5173/resetpassnew/{uidb64}/{token}/',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset email sent.'})
        


        return Response('email not found')
    
class ResetPasswordNewView(APIView):
    def post(self, request, uidb64, token):
        new_password = request.data.get('confirm_password')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>',new_password)
        # print("****************",uidb64, '****************',token)
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
        auth = default_token_generator.check_token(user, token)
        if auth:
            user.set_password(new_password)
            user.save()

        print('>>>>>>>>>>>>>>>>>>>>',auth)


        return Response('Password reset successful')    





class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializers = self.serializer_class(data = request.data)
        # print('>>>signup>>>>', serializers.is_valid())
        if serializers.is_valid():
            user = serializers.save()
            token = default_token_generator.make_token(user)
            # print("token: ",token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # print('uid: ', uid)
            confirm_link = f"http://127.0.0.1:8000/author/active/{uid}/{token}"
            email_subject = 'Confirm Your Email'
            email_body = render_to_string("confirm_email.html", {'confirm_link':confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response("Check your email for confirmation")
        return Response(serializers.errors)
        

    
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('http://localhost:5173/login')
    else:
        return redirect('http://localhost:5173/signup')
    


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data = self.request.data)
        print('>>>login>>>>', serializer.is_valid())
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username = username, password = password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                # print(token.key)
                # print(_)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id, 'user':user.username})
            else:
                return Response({'error' : "invalid Credential"})
        return Response(serializer.errors)



# class UserLogoutView(APIView):
#     def get(self, request):
#         request.user.auth_token.delete()
#         logout(request)
#         # return redirect('login')
#         return Response("success")



class UserLogoutView(APIView):

    def get(self, request):
        # print('>>>>>>>>>>>>>>>>>>',request.headers.get("Authorization"))
        # print(request)
        for user in User.objects.all():
            if(user.username != 'admin'):
                key_to_check = 'auth_token'
                if hasattr(user, key_to_check):
                    strToken= str(user.auth_token)
                    if(strToken == request.headers.get("Authorization")):
                        # print('>>>>>>>>>---user---->>>>>>>>',user.auth_token)
                        user.auth_token.delete()
                        logout(request)

        # print(request)
        # request.user.auth_token.delete()
        # logout(request)
        # return redirect('login')
        return Response("Logout success")


class ProfileImageViewSet(viewsets.ModelViewSet):
    queryset = models.UserAccount.objects.all()
    serializer_class = serializers.UserAccountSerializer

class UserView(APIView):
    def get(self, request):
        # print('>>>>>>>>>>>>>>>>>>',request.headers.get("Authorization"))
        if request.headers.get("Authorization") != 'null':
            # token = Token.objects.get(key=request.headers.get("Authorization"))
            token = Token.objects.filter(key=request.headers.get("Authorization"))
            if(token):
                # userAuth = token.user
                userAuth = token[0].user
                # profile_image = models.UserAccount.objects.get(user=userAuth)
                profile_image, created = models.UserAccount.objects.get_or_create(user=userAuth)
                serializerToken = serializers.UserTokenSerializer(token[0])
                serializerUserAuth = serializers.UserSerializer(userAuth)
                serializerProfileImage = serializers.UserAccountSerializer(profile_image)
                return Response({'token':serializerToken.data, 'profile':serializerUserAuth.data, 'profile_image':serializerProfileImage.data})
        return Response({'data': 'null'})
    



    



class UpdateProfileView(APIView):
    def post(self, request):
        author = request.data.get('author')
        serializer = serializers.UpdateProfileSerializer(data = self.request.data)
        # print('>>>update profile>>>>', serializer)

        if serializer.is_valid():
            updateProfile = serializer.save(author)
            # print(updateProfile)
            serializerUserAuth = serializers.UpdateProfileSerializer(updateProfile).data
            # print(serializerUserAuth)
            return Response(serializerUserAuth)
        return Response(serializer.errors)
    



class ChangePasswordView(APIView):
    def post(self, request):
        author = request.data.get('author')
        serializer = serializers.ChangePasswordSerializer(data = self.request.data)

        if serializer.is_valid():
            # print('>>>update profile>>>>', serializer)
            passwordChange = serializer.save(author)
        #     # print(updateProfile)
        #     # serializerUserAuth = serializers.ChangePasswordSerializer(updateProfile).data
        #     # print(serializerUserAuth)
            return Response('changePassword')
        return Response(serializer.errors)
    


        
    



    


    


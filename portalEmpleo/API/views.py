from lib2to3.pgen2 import token
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from .models import Candidate,Offers, State ,Postulation
from .serializers import CandidateListSerializer,CandidateRegisterSerializer,OffersListSerializer,PostulationCreateSerializer,OffersSerializer
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail,send_mass_mail, EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework.decorators import permission_classes







# Create your views here.


class Login (ObtainAuthToken):
    def post(self, request):
        print('PASO')
        parameterLogin = {
            "user":request.data['username'],
            "password":request.data['password']
        }
        userValidate = get_object_or_404(User, username=request.data['username'])
        if userValidate:
            user = authenticate(
                username=request.data['username'],
                password=request.data['password']
            )
            print ("user ::",user)
            if user:
                token2 = Token.objects.get_or_create(user=user)
                print("token2", token2[0])
                return Response(
                    {
                        'token': str(token2[0]),
                        'error': '',
                        'id': user.id,
                        # 'update': user.userGraduated.updateDate,
                        'nombre': user.first_name,
                        'apellido': user.last_name,
                        'username': user.username,
                        'is_active': user.is_active
                    }
                )

            else:
                content = {'error': 'Usuario o Password incorrectos'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuario no registrado en la base de datos'})


class Logout(APIView):
    def get(self,request,format = None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status =status.HTTP_200_OK)


class UserAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class CandidateList(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class= CandidateListSerializer
    authentication_class = (TokenAuthentication,)



class RegisterCandidateAPI(APIView):
    """
        User Profile Form Register API
    """
    serializer_class = CandidateRegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = CandidateRegisterSerializer(data=request.data)
        # If serializer is correct
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            print("request.data", request.data['user.first_name'])
            email_body = "<p>Hola " + request.data['user.first_name']+ " " + request.data['user.last_name'] + "! </p>"
            email_body += "<p></p>"
            email_body += "<p>Te damos la bienvenida a la plataforma de empleo TuEmpleoDes</p>"
            email_body += "<p>Recuerda tus credenciales para acceder a la plataforma y encontrar tu empleo soñado</p>"
            email_body += "<p></p>"
            email_body += "<p></p>"
            email_body += "<p></p>"
            email_body += "<p></p>"
            email_body += "<p>Cordialmente,</p>"
            email_body += "<p>Equipo de TuEmpleoDes</p>"
            # email_body += "<p>Coordinador de Proyectos</p>"
            # email_body += "<p>premio@colombialider.org</p>"
            # email_body += "<p>(57) 317 643 8653</p>"
            #print(email_body)
            subject, from_email, to = 'Bienvenido a la plataforma - TuEmpleoDes' , 'leonardo.novoa@grupohousemedia.com', str(request.data['user.email'])
            # subject, from_email, to = ' Registro exitoso - BidVox' , 'leonardo.novoa@grupohousemedia.com', 'pedro.rrg.96@gmail.com'
            text_content = 'Registro Exitoso'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(email_body, "text/html")
            msg.send()
            print("email enviado")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)


class OffersList(generics.ListCreateAPIView):
    queryset = Offers.objects.filter(state_id = 1 ).order_by('-created_at')
    serializer_class= OffersListSerializer
    authentication_class = (TokenAuthentication,)

   # permission_classes = (IsAuthenticated,)
   # authentication_class = (TokenAuthentication,)

class PostulationCreate(generics.CreateAPIView):
    serializer_class = PostulationCreateSerializer
    authentication_class = (TokenAuthentication,)
    
    def create(self, request, *args, **kwargs):
        tokenKey = request.META.get('HTTP_AUTHORIZATION').split()
        tokenKey = tokenKey[1]
        print("Header token ::", tokenKey)
        try:
            tokenModel = Token.objects.get(key=tokenKey)
        except ObjectDoesNotExist:
            content = {
                'details':
                'El token no es valido'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        userId = tokenModel.user.id
        candidate = Candidate.objects.get(user_id = userId)
        quotes = Postulation.objects.filter(Q(offers_id = request.data['offers'] )& Q(candidate_id=candidate.id)).count()
        if quotes :
            content = {
                'Error':
                'No puedes postularte dos veces a la misma oferta'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        newData = request.data
        newDataR = request.data.update({'candidate': candidate.id})
        print("newData : ", newData)
        print("request.data : ", request.data['offers'])
        serializer = self.get_serializer(data=request.data)
        print("serializer : ", serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



#@permission_classes((AllowAny, ))
class OffersCreate(generics.CreateAPIView):
    serializer_class = OffersSerializer
    authentication_class = (TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        tokenKey = request.META.get('HTTP_AUTHORIZATION').split()
        tokenKey = tokenKey[1]
        print("Header token ::", tokenKey)
        try:
            tokenModel = Token.objects.get(key=tokenKey)
        except ObjectDoesNotExist:
            content = {
                'details':
                'El token no es valido'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        userId = tokenModel.user.id
        user= User.objects.get(id=userId)
        state= State.objects.get(id=1)
        newData = request.data
        newDataS = request.data.update({'state': state.id})
        newDataR = request.data.update({'creatorUser': user.id})
        print("newData : ", newData)
        print("request.data : ", request.data)
        serializer = self.get_serializer(data=request.data)
        print("serializer : ", serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@permission_classes((AllowAny,))
class OffersUpdate(generics.UpdateAPIView):
 
    serializer_class = OffersSerializer
    authentication_class = (TokenAuthentication,)

    def get_queryset(self):  
        # Get certification instance
        offer = Offers.objects.get(id = self.kwargs['pk'])
        return self.get_serializer().Meta.model.objects.filter(id = self.kwargs['pk'])
    def patch(self,request,pk=None):
        offers =self.get_queryset().filter(id=pk).first()
        # If offer exists
        if offers:
            offer_serializer = self.serializer_class(offers)
            return Response(offer_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe una oferta con estos datos!'},status = status.HTTP_400_BAD_REQUEST)
    def put(self, request, *args, **kwargs):
        tokenKey = request.META.get('HTTP_AUTHORIZATION').split()
        tokenKey = tokenKey[1]
        print("Header token ::", tokenKey)
        try:
            tokenModel = Token.objects.get(key=tokenKey)
        except ObjectDoesNotExist:
            content = {
                'details':
                'El token no es valido'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        userId = tokenModel.user.id
        user= User.objects.get(id=userId)
        newDataR = request.data.update({'updaterUser': user.id})
        return self.update(request, *args, **kwargs)







# class Login(FormView):
#     template_name ="login.html"
#     form_class = AuthenticationForm
#     success_url = reverse_lazy('API:candidate_list')
#     @method_decorator(csrf_protect)
#     @method_decorator(never_cache)
#     def dispatch(self,request,*args,**kwargs):
#         if request.user.is_authenticated:
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return super(Login,self).dispatch(request,*args,*kwargs)
#     def form_valid(self, request):
#             user = authenticate(
#                 username=request.data['username'],
#                 password=request.data['password']
#             )
#             print ("user ::",user)
#             if user:
#                 token2 = Token.objects.get_or_create(user=user)
#                 print("token2", token2[0])
#                 return Response(
#                     {
#                         'token': str(token2[0]),
#                         'error': '',
#                         'id': user.id,
#                         # 'update': user.userGraduated.updateDate,
#                         'nombre': user.first_name,
#                         'apellido': user.last_name,
#                         'username': user.username,
#                         'is_active': user.is_active
#                     }
#                 )

#             else:
#                 content = {'error': 'Usuario o Password incorrectos'}
#                 return Response(content, status=status.HTTP_400_BAD_REQUEST)

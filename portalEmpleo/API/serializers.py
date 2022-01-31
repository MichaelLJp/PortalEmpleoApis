from dataclasses import field
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Candidate, Offers , Postulation

class UserSerializer(serializers.Serializer):
    id =  serializers.ReadOnlyField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def create(self, validated_data):
        instance = User()
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance
    def validate_username(self, data):
        users= User.objects.filter(username = data)
        if len(users) != 0:
            raise serializers.ValidationError("Este nombre de usuario ya exite, Ingrese uno nuevo")
        else:
            return data

class CandidateListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Candidate 
        fields =  ('__all__')

class CandidateRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = Candidate
        fields= (
            'user',
            'othersName',
            'othersLastName',
            'kindId',
            'numberId', 
            'profession', 
            'description'
        )
    def create(self, validated_data):
        # user_data = validated_data.pop('user')
        user = User.objects.create(username =  validated_data.get('user.username'),email = validated_data.get('user.email'),password = validated_data.get('user.password'),last_name = validated_data.get('user.last_name'),first_name = validated_data.get('user.first_name'))
        # user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.set_password(user.password)       
        users= User.objects.filter(username = validated_data.get('username'))
        candidate = Candidate.objects.filter(numberId = validated_data.get('numberId'))

        if len(users) != 0:
            raise serializers.ValidationError("Este nombre de usuario ya esta registrado, Ingrese uno nuevo")
        elif len(candidate) != 0:
            raise serializers.ValidationError("Este numero de identificaciòn ya esta registrado, Ingrese uno nuevo")
        user.save() 
        candidate= Candidate.objects.get_or_create(
            user=user,
            othersName= validated_data.get('othersName'),
            othersLastName= validated_data.get('othersLastName'),
            kindId_id= validated_data.get('kindId'),
            numberId= validated_data.get('numberId'),
            profession= validated_data.get('profession'),
            description= validated_data.get('description')
            # address= validated_data.get('address'),
        )
        return candidate

class OffersListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Offers 
        fields =  ('__all__')


class PostulationCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Postulation
		#fields = ('name', 'pk')
		fields = ('__all__')


class OffersSerializer(serializers.ModelSerializer):
  #  studies = studiesSerializer(many = True)
    class Meta:
        model = Offers
        fields = ('__all__')
        #fields = ('name', 'pk', 'icon')
	    
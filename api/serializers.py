from rest_framework import serializers
from .models import Users, Securityquestions, Caretaker, Healthcareprofessional, Advertise


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['userID', 'firstName', 'lastName', 'phoneNumber', 'postalAddress', 'email', 'roleID', 'username']


class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['securityQuestionOneID', 'securityQuestionTwoID', 'securityQuestionThreeID',
                  'securityQuestionOneAnswer', 'securityQuestionTwoAnswer', 'securityQuestionThreeAnswer'
                  ]


class SecurityQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Securityquestions
        fields = ['securityQuestionID', 'question']


class CareTakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caretaker
        fields = "__all__"


class HcpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Healthcareprofessional
        fields = "__all__"


class AdvertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertise
        fields = "__all__"

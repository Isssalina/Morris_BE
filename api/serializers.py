from rest_framework import serializers
from .models import Users, Securityquestions, Caretaker


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

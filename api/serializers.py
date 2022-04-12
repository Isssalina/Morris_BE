from rest_framework import serializers
from .models import Users, Securityquestions, Caretaker, Healthcareprofessional, Advertise, ServiceRequest, Requests, \
    WorkRecord


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        if obj.roleID.roleName == "hcp":
            relateID = Healthcareprofessional.objects.get(userID__userID=obj.userID).pID
            return {
                "type": obj.roleID.roleName,
                "pID": relateID
            }
        if obj.roleID.roleName == "ct":
            relateID = Caretaker.objects.get(userID__userID=obj.userID).takerID
            return {
                "type": obj.roleID.roleName,
                "takerID": relateID
            }
        return obj.roleID.roleName

    class Meta:
        model = Users
        fields = ['userID', 'username', 'firstName', 'lastName', 'phoneNumber', 'postalAddress', 'email', 'role',
                  'securityQuestionOneID', 'securityQuestionTwoID', 'securityQuestionThreeID',
                  'securityQuestionOneAnswer', 'securityQuestionTwoAnswer', 'securityQuestionThreeAnswer'
                  ]


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


class RequestListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requests
        fields = "__all__"


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = "__all__"


class WorkSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    def get_amount(self, obj):
        return obj.cal_amount(obj.request.hourlyRate)

    class Meta:
        model = WorkRecord
        fields = ['id', 'workDate', 'startTime', 'endTime', 'amount']


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = "__all__"

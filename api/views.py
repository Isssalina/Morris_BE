import hashlib
from rest_framework.views import APIView
from rest_framework.views import Response
from .models import Users, Securityquestions, Caretaker, Healthcareprofessional, Advertise
from .serializers import UserSerializer, SecurityQuestionsSerializer, CareTakerSerializer, HcpSerializer, \
    AdvertiseSerializer


class AuthView(APIView):
    def post(self, req):
        username = req.data.get("username", None)
        pwd = req.data.get('pwd', None)
        pwd = hashlib.md5(pwd.encode(encoding='utf-8')).hexdigest()
        user = Users.objects.filter(username=username, pwd=pwd, deleted=False).first()
        if user:
            return Response(UserSerializer(user).data, status=200)
        return Response(data={'error': "User does not exist"}, status=404)


class UserListView(APIView):
    def get(self, req):
        user = Users.objects.filter(deleted=False)
        return Response(UserSerializer(user, many=True).data, status=200)

    def post(self, req):
        user = Users()
        results = user.create_user(**req.data)
        return Response(data=results, status=200)


class UserView(APIView):
    def get(self, req, pk):
        user = Users.objects.filter(userID=int(pk), deleted=False).first()
        if user:
            return Response(UserSerializer(user).data, status=200)
        return Response(data={'error': "User does not exist"}, status=404)

    def put(self, req, pk):
        user = Users.objects.filter(userID=int(pk), deleted=False).first()
        if user:
            for k, v in req.data.items():
                if k in ['securityQuestionOneID', 'securityQuestionTwoID', 'securityQuestionThreeID']:
                    v = Securityquestions.objects.get(securityQuestionID=int(v))
                if k == "pwd":
                    v = hashlib.md5(v.encode(encoding='utf-8')).hexdigest()
                    setattr(user, k, v)
                setattr(user, k, v)
            user.save()
            return Response({}, status=200)
        return Response(data={'error': "User does not exist"}, status=404)

    def delete(self, req, pk):
        user = Users.objects.filter(userID=int(pk), deleted=False).first()
        if user:
            user.remove()
            return Response({})
        return Response(data={'error': "User does not exist"}, status=404)


class QuestionListView(APIView):
    def get(self, req):
        qs = Securityquestions.objects.filter(deleted=False)
        return Response(SecurityQuestionsSerializer(qs, many=True).data, status=200)


class QuestionView(APIView):
    def get(self, req, userID):
        user = Users.objects.filter(userID=int(userID), deleted=False).first()
        if user:
            data = {
                'securityQuestionOneID': user.securityQuestionOneID.securityQuestionID if user.securityQuestionOneID else None,
                'securityQuestionOne': user.securityQuestionOneID.question if user.securityQuestionOneID else None,
                'questionOneAnswer': user.securityQuestionOneAnswer,
                'securityQuestionTwoID': user.securityQuestionTwoID.securityQuestionID if user.securityQuestionTwoID else None,
                'securityQuestionTwo': user.securityQuestionTwoID.question if user.securityQuestionTwoID else None,
                'questionTwoAnswer': user.securityQuestionTwoAnswer,
                'securityQuestionThreeID': user.securityQuestionThreeID.securityQuestionID if user.securityQuestionThreeID else None,
                'securityQuestionThree': user.securityQuestionThreeID.question if user.securityQuestionThreeID else None,
                'questionThreeAnswer': user.securityQuestionThreeAnswer,
            }
            return Response(data=data, status=200)
        return Response(data={'error': "User does not exist"}, status=404)


class CareTakersView(APIView):
    def get(self, req):
        caretakers = Caretaker.objects.filter(deleted=False)
        return Response(data=CareTakerSerializer(caretakers, many=True).data, status=200)

    def post(self, req):
        caretaker = Caretaker()
        for k, v in req.data.items():
            setattr(caretaker, k, v)
        caretaker.enroll = False
        caretaker.save()
        return Response(data={"takerID": caretaker.takerID}, status=200)


class CareTakerView(APIView):
    def get(self, req, pk):
        caretaker = Caretaker.objects.filter(takerID=int(pk), deleted=False).first()
        if caretaker:
            return Response(CareTakerSerializer(caretaker).data, status=200)
        return Response(data={'error': "Caretaker does not exist"}, status=404)


class CareTakerEnRollView(APIView):
    def post(self, req, takerID):
        taker = Caretaker.objects.filter(takerID=int(takerID), deleted=False).first()
        if taker:
            if not taker.enroll:
                taker.enroll = True
                user = Users()
                results = user.create_user(taker.firstName, taker.lastName, taker.email, taker.postalAddress,
                                           taker.phoneNumber,
                                           'ct')
                taker.userID = Users.objects.get(userID=results['userID'])
                taker.save()
                return Response(data=results, status=200)
            return Response(data={'error': "The current caretaker has been enlisted"}, status=400)
        return Response(data={'error': "Caretaker does not exist"}, status=404)


class HealthCareProfessionalsView(APIView):
    def get(self, req, appID=None):
        if appID:
            hcp = Healthcareprofessional.objects.filter(advertiseID__adID=int(appID), enroll=False, deleted=False)
        else:
            hcp = Healthcareprofessional.objects.filter(deleted=False)
        return Response(data=HcpSerializer(hcp, many=True).data, status=200)

    def post(self, req, appID=None):
        ad = Advertise.objects.get(adID=int(appID))
        if Healthcareprofessional.objects.filter(email=req.data.get('email', None), advertiseID=ad, deleted=False):
            return Response({"error": "You have applied for this position. You can't apply for it again"}, status=400)
        hcp = Healthcareprofessional()
        for k, v in req.data.items():
            setattr(hcp, k, v)
        hcp.advertiseID = ad
        hcp.enroll = False
        hcp.save()
        return Response({}, status=200)


class HealthCareProfessionalView(APIView):
    def get(self, req, pk):
        hcp = Healthcareprofessional.objects.filter(pID=int(pk), deleted=False).first()
        if hcp:
            return Response(HcpSerializer(hcp).data, status=200)
        return Response(data={'error': "Applicant does not exist"}, status=404)

    def delete(self, req, pk):
        hcp = Healthcareprofessional.objects.filter(pID=int(pk), deleted=False).first()
        if hcp:
            hcp.remove()
            return Response({})
        return Response(data={'error': "Applicant does not exist"}, status=404)


class ApplicationsView(APIView):
    def get(self, req):
        typeHS = req.query_params.get("type", None)
        applications = Advertise.objects.filter(deleted=False)
        if typeHS:
            applications = applications.filter(typeHS=typeHS, deleted=False)
        return Response(AdvertiseSerializer(applications, many=True).data, status=200)

    def post(self, req):
        application = Advertise()
        for k, v in req.data.items():
            setattr(application, k, v)
        application.save()
        return Response({"adID": application.adID}, status=200)


class ApplicationView(APIView):
    def get(self, req, pk):
        application = Advertise.objects.filter(adID=int(pk), deleted=False).first()
        if application:
            return Response(AdvertiseSerializer(application).data, status=200)
        return Response(data={'error': "Application does not exist"}, status=404)

    def delete(self, req, pk):
        application = Advertise.objects.filter(adID=int(pk), deleted=False).first()
        if application:
            application.remove()
            return Response({})
        return Response(data={'error': "User does not exist"}, status=404)


class HcpApproveView(APIView):
    # approve
    def get(self, req, pID):
        hcp = Healthcareprofessional.objects.filter(pID=int(pID), deleted=False).first()
        ad = hcp.advertiseID
        if hcp:
            if not hcp.enroll:
                hcp.enroll = True
                user = Users()
                results = user.create_user(hcp.firstName, hcp.lastName, hcp.email, hcp.postalAddress,
                                           hcp.phoneNumber,
                                           'hcp')
                hcp.userID = Users.objects.get(userID=results['userID'])
                hcp.save()
                ad.remove()
                for hcp in Healthcareprofessional.objects.filter(advertiseID=ad, deleted=False):
                    if int(hcp.pID) != int(pID):
                        hcp.remove()
                return Response(data=results, status=200)
            return Response(data={'error': "The current hcp has been enlisted"}, status=400)
        return Response(data={'error': "Application or applicant  does not exist"}, status=404)


class HcpDenyView(APIView):
    # deny
    def get(self, req, pID):
        hcp = Healthcareprofessional.objects.filter(pID=int(pID), deleted=False).first()
        if hcp:
            hcp.remove()
            return Response(data={}, status=200)
        else:
            return Response(data={'Applicant does not exist'}, status=400)

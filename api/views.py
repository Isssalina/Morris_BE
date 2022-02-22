from rest_framework.views import APIView
from rest_framework.views import Response
from .models import Users, Securityquestions, Caretaker
from .serializers import UserSerializer, SecurityQuestionsSerializer, CareTakerSerializer


class AuthView(APIView):
    def post(self, req):
        username = req.data.get("username", None)
        pwd = req.data.get('pwd', None)
        user = Users.objects.filter(username=username, pwd=pwd).first()
        if user:
            return Response(UserSerializer(user).data, status=200)
        return Response(data={'error': "User does not exist"}, status=404)


class UserListView(APIView):
    def get(self, req):
        user = Users.objects.all()
        return Response(UserSerializer(user, many=True).data, status=200)

    def post(self, req):
        user = Users()
        results = user.create_user(**req.data)
        return Response(data=results, status=200)


class UserView(APIView):
    def get(self, req, pk):
        user = Users.objects.filter(userID=int(pk)).first()
        if user:
            return Response(UserSerializer(user).data, status=200)
        return Response(data={'error': "User does not exist"}, status=404)

    def put(self, req, pk):
        user = Users.objects.filter(userID=int(pk)).first()
        if user:
            for k, v in req.data.items():
                if k in ['securityQuestionOneID', 'securityQuestionTwoID', 'securityQuestionThreeID']:
                    v = Securityquestions.objects.get(securityQuestionID=int(v))
                setattr(user, k, v)
            user.save()
            return Response({}, status=200)
        return Response(data={'error': "User does not exist"}, status=404)

    def delete(self, req, pk):
        user = Users.objects.filter(userID=int(pk)).first()
        if user:
            user.delete()
            return Response({})
        return Response(data={'error': "User does not exist"}, status=404)


class QuestionListView(APIView):
    def get(self, req):
        qs = Securityquestions.objects.all()
        return Response(SecurityQuestionsSerializer(qs, many=True).data, status=200)


class QuestionView(APIView):
    def get(self, req, userID):
        user = Users.objects.filter(userID=int(userID)).first()
        if user:
            data = {
                'questionOne': SecurityQuestionsSerializer(user.securityQuestionOneID).data,
                'questionTwo': SecurityQuestionsSerializer(user.securityQuestionTwoID).data,
                'questionThree': SecurityQuestionsSerializer(user.securityQuestionThreeID).data,
            }
            return Response(data=data, status=200)
        return Response(data={'error': "User does not exist"}, status=404)


class CareTakersView(APIView):
    def get(self, req):
        caretakers = Caretaker.objects.all()
        return Response(data=CareTakerSerializer(caretakers, many=True).data, status=200)

    def post(self, req):
        caretaker = Caretaker()
        for k, v in req.data.items():
            setattr(caretaker, k, v)
        caretaker.enroll = 0
        caretaker.save()
        return Response(data={"takerID": caretaker.takerID}, status=200)


class CareTakerView(APIView):
    def get(self, req, pk):
        caretaker = Caretaker.objects.filter(takerID=int(pk)).first()
        if caretaker:
            return Response(CareTakerSerializer(caretaker).data, status=200)
        return Response(data={'error': "Caretaker does not exist"}, status=404)


class CareTakerEnRollView(APIView):
    def post(self, req, takerID):
        taker = Caretaker.objects.filter(takerID=int(takerID)).first()
        if taker:
            if int(taker.enroll) != 1:
                taker.enroll = 1
                user = Users()
                results = user.create_user(taker.firstName, taker.lastName, taker.email, taker.postalAddress,
                                           taker.phoneNumber,
                                           'caretaker')
                taker.userID = Users.objects.get(userID=results['userID'])
                taker.save()
                return Response(data=results, status=200)
            return Response(data={'error': "The current caretaker has been enlisted"}, status=400)
        return Response(data={'error': "Caretaker does not exist"}, status=404)

import datetime
import hashlib
from rest_framework.views import APIView
from rest_framework.views import Response
from .models import Users, Securityquestions, Caretaker, Healthcareprofessional, Advertise, Requests, WorkRecord, \
    ServiceRequest
from .serializers import UserSerializer, SecurityQuestionsSerializer, CareTakerSerializer, HcpSerializer, \
    AdvertiseSerializer, RequestListSerializer, RequestSerializer, WorkSerializer, ServiceRequestSerializer
from rest_framework.authentication import SessionAuthentication
from .utils import is_conflict, get_time_schedule


class UnsafeSessionAuthentication(SessionAuthentication):
    def authenticate(self, request):
        http_request = request._request
        user = getattr(http_request, 'user', None)
        if not user or not user.is_active:
            return None
        return user, None


class AuthView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

    def post(self, req):
        username = req.data.get("username", None)
        pwd = req.data.get('pwd', None)
        pwd = hashlib.md5(pwd.encode(encoding='utf-8')).hexdigest()
        user = Users.objects.filter(username=username, pwd=pwd, deleted=False).first()
        if user:
            return Response(UserSerializer(user).data, status=200)
        return Response(data={'error': "User does not exist"}, status=404)


class UserListView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

    def get(self, req):
        user = Users.objects.filter(deleted=False)
        return Response(UserSerializer(user, many=True).data, status=200)

    def post(self, req):
        user = Users()
        results = user.create_user(**req.data)
        return Response(data=results, status=200)


class UserView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

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
    authentication_classes = (UnsafeSessionAuthentication,)

    def get(self, req):
        qs = Securityquestions.objects.filter(deleted=False)
        return Response(SecurityQuestionsSerializer(qs, many=True).data, status=200)


class QuestionView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

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
    authentication_classes = (UnsafeSessionAuthentication,)

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
    authentication_classes = (UnsafeSessionAuthentication,)

    def get(self, req, pk):
        caretaker = Caretaker.objects.filter(takerID=int(pk), deleted=False).first()
        if caretaker:
            return Response(CareTakerSerializer(caretaker).data, status=200)
        return Response(data={'error': "Caretaker does not exist"}, status=404)


class CareTakerEnRollView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

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
    authentication_classes = (UnsafeSessionAuthentication,)

    def get(self, req, appID=None):
        enroll = req.GET.get("enroll", False)
        enroll = True if enroll == "1" else False
        if appID:
            hcp = Healthcareprofessional.objects.filter(advertiseID__adID=int(appID), enroll=False, deleted=False)
        else:
            hcp = Healthcareprofessional.objects.filter(deleted=False, enroll=enroll)
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
    authentication_classes = (UnsafeSessionAuthentication,)

    def get(self, req, pk):
        hcp = Healthcareprofessional.objects.filter(pID=int(pk), deleted=False).first()
        if hcp:
            return Response(HcpSerializer(hcp).data, status=200)
        return Response(data={'error': "Applicant does not exist"}, status=404)

    def delete(self, req, pk):
        hcp = Healthcareprofessional.objects.filter(pID=int(pk), deleted=False).first()
        if hcp:
            if WorkRecord.objects.filter(hcp=hcp, hcpPayed=False).count() > 0:
                return Response({"error": "Current Applicant has unpaid bills"})
            hcp.userID.remove()
            hcp.remove()
            return Response({})
        return Response(data={'error': "Applicant does not exist"}, status=404)

    def put(self, req, pk):
        """
        todo:add salary
        """
        hcp = Healthcareprofessional.objects.filter(pID=int(pk), deleted=False).first()
        if hcp:
            for k, v in req.data.items():
                setattr(hcp, k, v)
            hcp.save()
            return Response({})
        return Response(data={'error': "Applicant does not exist"}, status=404)


class ApplicationsView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

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
    authentication_classes = (UnsafeSessionAuthentication,)

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
    authentication_classes = (UnsafeSessionAuthentication,)

    # approve
    def get(self, req, pID):
        hcp = Healthcareprofessional.objects.filter(pID=int(pID), deleted=False).first()
        ad = hcp.advertiseID
        if hcp and ad:
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
        return Response(data={'error': "Application or applicant does not exist"}, status=404)


class HcpDenyView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

    # deny
    def get(self, req, pID):
        hcp = Healthcareprofessional.objects.filter(pID=int(pID), deleted=False).first()
        if hcp:
            hcp.remove()
            return Response(data={}, status=200)
        else:
            return Response(data={'error': 'Applicant does not exist'}, status=404)


class RequestsView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

    def get(self, req):
        userID = req.query_params.get("userID", None)
        requests = Requests.objects.filter(deleted=False)
        if userID:
            requests = requests.filter(userID__userID=int(userID))
        return Response(RequestListSerializer(requests, many=True).data, status=200)

    def post(self, req):
        h_request = Requests()
        # 1.检查是否发布过serviceType相同的request
        patientFirstName = req.data.get("patientFirstName", None)
        patientLastName = req.data.get("patientLastName", None)
        dateOfBirth = req.data.get("dateOfBirth", None)
        r = req.data.get("requirements")
        serviceType = r['serviceType']
        exist = Requests.objects.filter(patientFirstName=patientFirstName, patientLastName=patientLastName,
                                        dateOfBirth=dateOfBirth, requirements__serviceType=serviceType,
                                        deleted=False).first()
        startDate = r['startDate']
        numDaysRequested = r['numDaysRequested']
        daysRequested = r['daysRequested']
        startTime = r['startTime'] if 'startTime' in r else False
        endTime = r['endTime'] if 'endTime' in r else False
        flexibleTime = r['flexibleTime'] if 'flexibleTime' in r else False
        if exist:
            # 2.检查时间是否重合
            exist_schedule = exist.get_schedule()
            current_schedule = get_time_schedule(startDate, numDaysRequested, daysRequested, startTime, endTime,
                                                 flexibleTime)
            if is_conflict(exist_schedule, current_schedule):
                return Response({"error": "The current patient has posted the same request during this time period"})
        for k, v in req.data.items():
            if k == "userID":
                v = Users.objects.filter(userID=int(v), deleted=False).first()
                if not v:
                    return Response({"error": "User does not exist"}, status=200)
            setattr(h_request, k, v)
        h_request.distribution = {
            "assigned": [],
            "unassigned": h_request.requirements['daysRequested']
        }
        h_request.save()
        return Response({"requestID": Requests.objects.last().requestID}, status=200)


class RequestView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

    def get(self, req, pk):
        _requests = Requests.objects.filter(requestID=int(pk), deleted=False).first()
        if _requests:
            return Response(RequestListSerializer(_requests).data, status=200)
        else:
            return Response({'error': 'Requests does not exist'}, status=404)

    def put(self, req, pk):
        _requests = Requests.objects.filter(requestID=int(pk), deleted=False).first()
        if _requests:
            for k, v in req.data.items():
                setattr(_requests, k, v)
            _requests.save()
            return Response({})
        return Response(data={'error': "Request does not exist"}, status=404)

    def delete(self, req, pk):
        _requests = Requests.objects.filter(requestID=int(pk), deleted=False).first()
        if _requests:
            _requests.remove()
            return Response({}, status=200)
        else:
            return Response({'error': 'Requests does not exist'}, status=404)


class AssignRequestView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

    def post(self, req):
        requestID = req.data.get("requestID")
        pID = req.data.get('pID')
        _requests = Requests.objects.filter(requestID=int(requestID), deleted=False).first()
        hcp = Healthcareprofessional.objects.filter(pID=int(pID), deleted=False).first()
        if not _requests:
            return Response({'error': 'Requests does not exist'}, status=404)
        if not hcp:
            return Response({'error': 'Hcp does not exist'}, status=404)
        if not hcp.enroll:
            return Response({'error': 'The current hcp is not enrolled'}, status=400)
        daysRequested = req.data.get("daysRequested")
        r = _requests.requirements
        flexibleTime = r['flexibleTime'] if 'flexibleTime' in r else False
        if flexibleTime:
            startTime = req.data.get("startTime")
            endTime = req.data.get("endTime")
            if not (startTime and endTime):
                return Response({'error': 'FlexibleTime request requires start time and end time'}, status=400)
        else:
            startTime = r['startTime']
            endTime = r['endTime']
        status, results = _requests.assign(hcp, daysRequested, startTime, endTime)
        return Response(results, status=status)


class UnAssignRequestView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

    def post(self, req):
        requestID = req.data.get("requestID")
        pID = req.data.get('pID')
        scheduleID = req.data.get('scheduleID')
        _requests = Requests.objects.filter(requestID=int(requestID), deleted=False).first()
        hcp = Healthcareprofessional.objects.filter(pID=int(pID), deleted=False).first()
        if not _requests:
            return Response({'error': 'Requests does not exist'}, status=404)
        if not hcp:
            return Response({'error': 'Hcp does not exist'}, status=404)
        if not hcp.enroll:
            return Response({'error': 'The current hcp is not enrolled'}, status=400)

        status, results = _requests.un_assign(hcp, scheduleID)
        return Response(results, status=status)


class AvailableHcpView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

    def post(self, req, requestID):
        _request = Requests.objects.filter(requestID=int(requestID)).first()
        startTime = req.data.get("startTime", None)
        endTime = req.data.get("endTime", None)
        daysRequested = req.data.get("daysRequested", None)
        if _request:
            return Response(
                data=HcpSerializer(_request.get_available_hcp(startTime, endTime, daysRequested), many=True).data)
        return Response({"error": "requests does not exist"}, 404)


class ScheduleView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

    def get(self, req, pID):
        hcp = Healthcareprofessional.objects.filter(pID=int(pID)).first()
        if hcp:
            ret = []
            schedules = hcp.schedule
            for k, v in schedules.items():
                _request = Requests.objects.get(requestID=int(k))
                _request = RequestSerializer(_request).data
                _request['schedule'] = v
                ret.append(_request)
            return Response(ret, 200)
        else:
            return Response({"error": "Hcp does not exist"}, 404)


class WorkView(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

    def post(self, req):
        requestID = req.data.get("requestID", -1)
        pID = req.data.get('pID', -1)
        scheduleID = req.data.get('scheduleID', -1)
        workDate = req.data.get("workDate")
        startTime = req.data.get('startTime')
        endTime = req.data.get('endTime')
        _requests = Requests.objects.filter(requestID=int(requestID), deleted=False).first()
        hcp = Healthcareprofessional.objects.filter(pID=int(pID), deleted=False).first()
        if not _requests:
            return Response({'error': 'Requests does not exist'}, status=404)
        if not hcp:
            return Response({'error': 'Hcp does not exist'}, status=404)
        if not hcp.enroll:
            return Response({'error': 'The current hcp is not enrolled'}, status=400)
        if not hcp.has_schedule(requestID, scheduleID):
            return Response({'error': 'The scheduleID is invalid'}, status=400)
        if WorkRecord.objects.filter(hcp=hcp, request=_requests, scheduleID=int(scheduleID), workDate=workDate).first():
            return Response({'error': 'Work record already exists'}, status=400)
        hourlyRate = _requests.hourlyRate
        work = WorkRecord()
        work.hcp = hcp
        work.request = _requests
        work.scheduleID = scheduleID
        work.amount = work.cal_amount(startTime, endTime, hourlyRate)
        work.startTime = startTime
        work.endTime = endTime
        work.workDate = workDate
        work.salary = work.cal_amount(startTime, endTime, hcp.salary)
        work.save()
        return Response(WorkSerializer(work).data, 200)


class BillingAccountListView(APIView):
    def get(self, req):
        ret = []
        _requestsList = Requests.objects.filter(deleted=False)
        for _requests in _requestsList:
            ret.append(_requests.get_billing_account())
        return Response(ret, 200)


class BillingAccountView(APIView):
    def get(self, req, requestID):
        _requests = Requests.objects.filter(requestID=int(requestID), deleted=False).first()
        if not _requests:
            return Response({'error': 'Requests does not exist'}, status=404)
        ret = _requests.get_billing_account()
        return Response(ret, 200)


class HcpBillingListView(APIView):
    def get(self, req):
        ret = []
        hcpList = Healthcareprofessional.objects.filter(enroll=True, deleted=False)
        for hcp in hcpList:
            ret.append(hcp.get_salary_info())
        return Response(ret, 200)


class HcpBillingView(APIView):
    def get(self, req, pID):
        hcp = Healthcareprofessional.objects.filter(pID=int(pID), deleted=False).first()
        if not hcp:
            return Response({'error': 'Hcp does not exist'}, status=404)
        if not hcp.enroll:
            return Response({'error': 'The current hcp is not enrolled'}, status=400)
        ret = hcp.get_salary_info()
        return Response(ret, 200)


class BillingPayView(APIView):
    def get(self, req, recordID):
        record = WorkRecord.objects.filter(id=int(recordID)).first()
        if not record:
            return Response({'error': 'Record does not exist'}, status=404)
        record.hasPayed = True
        record.payedTime = datetime.datetime.now()
        record.save()
        return Response({}, 200)


class HcpPayView(APIView):
    def get(self, req, recordID):
        record = WorkRecord.objects.filter(id=int(recordID)).first()
        if not record:
            return Response({'error': 'Record does not exist'}, status=404)
        record.hcpPayed = True
        record.hcpPayedTime = datetime.datetime.now()
        record.save()
        return Response({}, 200)


class ServiceRequestView(APIView):
    def get(self, req):
        servicesInfo = ServiceRequest.objects.filter(deleted=False)
        userTo = req.query_params.get("userTo", None)
        if userTo:
            servicesInfo = servicesInfo.filter(userTo__userID=int(userTo))
        userFrom = req.query_params.get("userFrom", None)
        if userFrom:
            servicesInfo = servicesInfo.filter(userFrom__userID=int(userFrom))
        return Response(ServiceRequestSerializer(servicesInfo, many=True).data, 200)

    def post(self, req):
        userFrom = req.data.get('userFrom', None)
        userTo = req.data.get('userTo', None)
        requestID = req.data.get("requestID", None)
        status = req.data.get("status", 0)
        _request = Requests.objects.filter(requestID=int(requestID), deleted=False).first()
        userFrom = Users.objects.filter(userID=int(userFrom), deleted=False).first()
        userTo = Users.objects.filter(userID=int(userTo), deleted=False).first()
        if not _request:
            return Response({'error': 'Request does not exist'}, status=404)
        if not userFrom:
            return Response({'error': 'userFrom does not exist'}, status=404)
        if not userTo:
            return Response({'error': 'userTo does not exist'}, status=404)
        s = ServiceRequest()
        s.userFrom = userFrom
        s.userTo = userTo
        s.request = _request
        s.status = int(status)
        s.save()
        return Response({"id": s.id}, 200)

    def put(self, req):
        serviceID = req.data.get("serviceID", -1)
        status = req.data.get("status", 0)
        service = ServiceRequest.objects.filter(pk=int(serviceID), deleted=False).first()
        if not service:
            return Response({'error': 'Service request does not exist'}, status=404)
        service.status = status
        if int(status) == 2:  # success
            if service.request.get_billing_count() == 0:
                service.request.end_request()
        service.save()


class EndRequestView(APIView):
    def get(self, req, requestID):
        _requests = Requests.objects.filter(requestID=int(requestID), deleted=False).first()
        if not _requests:
            return Response({'error': 'Requests does not exist'}, status=404)
        if _requests.get_billing_count() > 0:
            return Response({'error': 'The current Request has unpaid bills'}, status=400)
        _requests.end_request()
        return Response({}, 200)

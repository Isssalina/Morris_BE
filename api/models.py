from django.db import models
import datetime
import random
import hashlib
from .utils import sent_email, is_conflict, get_time_schedule, popItem, timeFormat


class Roles(models.Model):
    roleID = models.AutoField(db_column='roleID', primary_key=True)  # Field name made lowercase.
    roleName = models.CharField(db_column='roleName', max_length=30)  # Field name made lowercase.
    updateTime = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def remove(self):
        self.deleted = True
        self.save()

    class Meta:
        db_table = 'Roles'


class Securityquestions(models.Model):
    securityQuestionID = models.AutoField(db_column='securityQuestionID',
                                          primary_key=True)  # Field name made lowercase.
    question = models.CharField(max_length=255)
    updateTime = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def remove(self):
        self.deleted = True
        self.save()

    class Meta:
        db_table = 'SecurityQuestions'


class Users(models.Model):
    userID = models.AutoField(db_column='userID', primary_key=True)  # Field name made lowercase.
    firstName = models.CharField(db_column='firstName', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    lastName = models.CharField(db_column='lastName', max_length=50, blank=True,
                                null=True)  # Field name made lowercase.
    phoneNumber = models.DecimalField(db_column='phoneNumber', max_digits=10, decimal_places=0, blank=True,
                                      null=True)  # Field name made lowercase.
    postalAddress = models.CharField(db_column='postalAddress', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    email = models.CharField(max_length=100, blank=True, null=True)
    roleID = models.ForeignKey(Roles, models.CASCADE, db_column='roleID')  # Field name made lowercase.
    username = models.CharField(db_column='username', max_length=100)  # Field name made lowercase.
    pwd = models.CharField(max_length=32)
    securityQuestionOneID = models.ForeignKey(Securityquestions, models.CASCADE,
                                              related_name="q1", blank=True, null=True,
                                              db_column='securityQuestionOneID')  # Field name made lowercase.
    securityQuestionOneAnswer = models.CharField(db_column='securityQuestionOneAnswer', blank=True, null=True,
                                                 max_length=30)  # Field name made lowercase.
    securityQuestionTwoID = models.ForeignKey(Securityquestions, models.CASCADE,
                                              related_name="q2", blank=True, null=True,
                                              db_column='securityQuestionTwoID')  # Field name made lowercase.
    securityQuestionTwoAnswer = models.CharField(db_column='securityQuestionTwoAnswer', blank=True, null=True,
                                                 max_length=30)  # Field name made lowercase.
    securityQuestionThreeID = models.ForeignKey(Securityquestions, models.CASCADE,
                                                related_name="q3", blank=True, null=True,
                                                db_column='securityQuestionThreeID')  # Field name made lowercase.
    securityQuestionThreeAnswer = models.CharField(db_column='securityQuestionThreeAnswer', blank=True, null=True,
                                                   max_length=30)  # Field name made lowercase.
    updateTime = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def gen_password(self):
        ch1 = "~!@#$%ˆ&*+"
        ch2 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        ch3 = '1234567890'
        pwd_list = []
        for i in range(random.randint(1, 3)):
            pwd_list.append(ch1[random.randint(0, len(ch1) - 1)])
        for i in range(random.randint(4, 6)):
            pwd_list.append(ch2[random.randint(0, len(ch2) - 1)])
        for i in range(random.randint(2, 6)):
            pwd_list.append(ch3[random.randint(0, len(ch3) - 1)])
        random.shuffle(pwd_list)
        return "".join(pwd_list)

    def gen_username(self, last_name):
        last = Users.objects.last()
        _id = 0
        if last:
            _id = int(last.userID)
        return f"{last_name}{'0' if _id < 10 else ''}{_id}"

    def create_user(self, firstName, lastName, email, postalAddress, phoneNumber, role):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.postalAddress = postalAddress
        self.phoneNumber = phoneNumber
        self.roleID = Roles.objects.get(roleName=role)
        self.username = self.gen_username(lastName)
        raw_pwd = self.gen_password()
        self.pwd = hashlib.md5(raw_pwd.encode(encoding='utf-8')).hexdigest()
        self.save()
        sent_email(self.email, self.username, raw_pwd)
        return {'userID': self.userID}

    def remove(self):
        self.deleted = True
        if self.roleID.roleName == "hcp":
            hcp = Healthcareprofessional.objects.get(userID__userID=self.userID)
            hcp.remove()
        self.save()

    class Meta:
        db_table = 'Users'


class Caretaker(models.Model):
    takerID = models.AutoField(db_column='takerID', primary_key=True)  # Field name made lowercase.
    firstName = models.CharField(db_column='firstName', max_length=50)  # Field name made lowercase.
    lastName = models.CharField(db_column='lastName', max_length=50)  # Field name made lowercase.
    phoneNumber = models.DecimalField(db_column='phoneNumber', max_digits=10, decimal_places=0, blank=True,
                                      null=True)  # Field name made lowercase.
    postalAddress = models.CharField(db_column='postalAddress', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    email = models.CharField(max_length=100, blank=True, null=True)
    enroll = models.BooleanField(blank=True, null=True, default=False)
    userID = models.ForeignKey('Users', models.CASCADE, db_column='userID', blank=True,
                               null=True)
    updateTime = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def remove(self):
        self.deleted = True
        self.save()

    class Meta:
        db_table = 'CareTaker'


class Healthcareprofessional(models.Model):
    pID = models.IntegerField(db_column='PID', primary_key=True)  # Field name made lowercase.
    firstName = models.CharField(db_column='firstName', max_length=50)  # Field name made lowercase.
    lastName = models.CharField(db_column='lastName', max_length=50)  # Field name made lowercase.
    sex = models.CharField(max_length=1)
    ssn = models.DecimalField(db_column='SSN', max_digits=9, decimal_places=0)  # Field name made lowercase.
    salary = models.FloatField(default=0)
    typeHS = models.CharField(db_column='Type_H_S', max_length=15)  # Field name made lowercase.
    qualification = models.CharField(db_column='Qualification', max_length=10)  # Field name made lowercase.
    qualificationDate = models.DateField(db_column='Qualification_Date',
                                         default=datetime.datetime.now)  # Field name made lowercase.
    yearOExp = models.IntegerField(db_column='Year_O_Exp')  # Field name made lowercase.
    phoneNumber = models.DecimalField(db_column='phoneNumber', max_digits=10, decimal_places=0, blank=True,
                                      null=True)  # Field name made lowercase.
    postalAddress = models.CharField(db_column='postalAddress', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    dateOfBirth = models.DateField(default=datetime.datetime.now)
    email = models.CharField(max_length=100, blank=True, null=True)
    enroll = models.BooleanField(blank=True, null=True, default=False)
    advertiseID = models.ForeignKey('Advertise', models.CASCADE, db_column='advertiseID', blank=True,
                                    null=True)  # Field name made lowercase.
    userID = models.ForeignKey('Users', models.CASCADE, db_column='userID', blank=True,
                               null=True)  # Field name made lowercase.
    schedule = models.JSONField(default={})
    updateTime = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def age(self):
        return datetime.datetime.now().year - self.dateOfBirth.year

    def remove(self):
        self.deleted = True
        self.save()

    def get_name(self):
        return f"{self.firstName} {self.lastName}"

    def get_all_schedule(self):
        schedules = []
        if self.schedule:
            for k, v in self.schedule.items():
                for item in v:
                    schedules.extend(
                        get_time_schedule(item['startDate'], item['numDaysRequested'], item['daysRequested'],
                                          item['startTime'], item['endTime'], False))
        return schedules

    def has_schedule(self, requestID):
        requestID = str(requestID)
        if not self.schedule:
            return False
        if requestID not in self.schedule:
            return False
        return True

    def add_schedule(self, startDate, startTime, endTime, requestID, numDaysRequested, daysRequested):
        requestID = str(requestID)
        if not self.schedule:
            self.schedule = {}
        item = {
            "scheduleID": 0,
            "startDate": startDate,
            "startTime": startTime,
            'endTime': endTime,
            "numDaysRequested": numDaysRequested,
            "daysRequested": daysRequested
        }

        if requestID in self.schedule:
            schedule_id = self.schedule[requestID][-1]['scheduleID'] + 1
            item['scheduleID'] = schedule_id
            for s in self.schedule[requestID]:
                if s['startDate'] == startDate and s['numDaysRequested'] == numDaysRequested and \
                        (s['startTime'] == startTime and s['endTime'] == endTime):
                    s['daysRequested'].extend(daysRequested)
                    self.save()
                    return s
            self.schedule[requestID].append(item)
        else:
            self.schedule[requestID] = [item]
        self.save()
        return item

    def remove_schedule(self, requestID, scheduleID):
        requestID = str(requestID)
        if requestID in self.schedule:
            pop, new_array = popItem(self.schedule[requestID], lambda x: int(x['scheduleID'] == int(scheduleID)))
            if pop:
                if new_array:
                    self.schedule[requestID] = new_array
                else:
                    del self.schedule[requestID]
                self.save()
                return 200, pop
            return 404, {"error": "schedule does not exist"}
        else:
            return 404, {"error": "schedule does not exist"}

    def get_salary_info(self):
        salaryRecord = BillingAccount.objects.get(hcp=self)
        ret = {
            "billingAccountID": salaryRecord.pk + 1000,
            "total": salaryRecord.total,
            "payedTotal": salaryRecord.paid,
            "unPayedTotal": salaryRecord.unpaid,
            "hcp": {
                "pID": self.pID,
                "hcpName": self.get_name()
            },
            "detail": []
        }
        records = PayRecord.objects.filter(billingAccount=salaryRecord)
        for record in records:
            ret['detail'].append({
                "amount": record.amount,
                "paidTime": record.paidTime
            })
        return ret

    class Meta:
        db_table = 'HealthcareProfessional'


class Requests(models.Model):
    requestID = models.IntegerField(db_column='requestID', primary_key=True)  # Field name made lowercase.
    userID = models.ForeignKey(Users, models.CASCADE, null=True,
                               blank=True)  # Field name made lowercase.
    patientFirstName = models.CharField(db_column='patientFirstName', max_length=50)  # Field name made lowercase.
    patientLastName = models.CharField(db_column='patientLastName', max_length=50)  # Field name made lowercase.
    sex = models.CharField(max_length=1)
    dateOfBirth = models.DateField(db_column='dateOfBirth')  # Field name made lowercase.

    locationOfService = models.CharField(db_column='locationOfService', max_length=30)  # Field name made lowercase.
    patientPhoneNumber = models.DecimalField(db_column='patientPhoneNumber', max_digits=10,
                                             decimal_places=0)  # Field name made lowercase.
    patientEmail = models.CharField(db_column='patientEmail', max_length=100)  # Field name made lowercase.
    hourlyRate = models.FloatField(default=100.0, null=True, blank=True)
    requirements = models.JSONField(default={})
    distribution = models.JSONField(default={})
    deleted = models.BooleanField(default=False)
    updateTime = models.DateTimeField(default=datetime.datetime.now)
    end = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Requests({self.requestID})"

    def assign(self, hcp: Healthcareprofessional, daysRequested, startTime, endTime):
        unassigned_list = self.distribution['unassigned']
        r = self.requirements
        for i in daysRequested:
            if i in unassigned_list:
                del self.distribution['unassigned'][unassigned_list.index(i)]
            else:
                return 400, {"error": f"daysRequested {i} can not be assigned"}
        schedule = hcp.add_schedule(r['startDate'], startTime, endTime, self.requestID, r['numDaysRequested'],
                                    daysRequested)
        for item in self.distribution['assigned']:
            s = item['schedule']
            if s['startDate'] == r['startDate'] and s['numDaysRequested'] == r['numDaysRequested'] and \
                    (s['startTime'] == startTime and s['endTime'] == endTime):
                s['daysRequested'].extend(daysRequested)
                self.save()
                return 200, item
        ret = {
            "schedule": schedule,
            "hcp": hcp.pID,
            "hcpName": hcp.get_name()
        }
        self.distribution['assigned'].append(ret)
        self.save()
        return 200, ret

    def end_request(self):
        self.end = True
        self.save()

    def is_end(self):
        if self.end:
            return True
        wcs_count = self.get_billing_count()
        startDate = datetime.datetime.strptime(self.requirements['startDate'], "%Y-%m-%d")
        endDate = startDate + datetime.timedelta(days=int(self.requirements['numDaysRequested']))
        return wcs_count == 0 and datetime.datetime.now() > endDate

    def get_status(self):
        """
        0:not start
        1:start
        2:end
        """
        startDate = datetime.datetime.strptime(self.requirements['startDate'], "%Y-%m-%d")
        if startDate > datetime.datetime.now():
            return 0
        elif self.is_end():
            return 2
        else:
            return 1

    def get_billing_count(self):
        return WorkRecord.objects.filter(request=self, hasPayed=False).count()

    def un_assign(self, hcp: Healthcareprofessional, scheduleID):
        status, results = hcp.remove_schedule(self.requestID, scheduleID)
        if status != 404:
            self.distribution['unassigned'].extend(results['daysRequested'])
            pop, new_array = popItem(self.distribution['assigned'],
                                     lambda x: int(x['schedule']['scheduleID']) == int(scheduleID))
            if pop:
                self.distribution['assigned'] = new_array
                self.save()
        return status, results

    def delete_hcp_schedule(self):
        assigned = self.distribution['assigned']
        for item in assigned:
            hcp = Healthcareprofessional.objects.filter(pID=int(item['hcp'])).first()
            if hcp:
                hcp.remove_all_schedule(self.requestID)

    def check_requirements(self, hcp, requirements):
        available = True
        if "age_min" in requirements:
            available = available and hcp.age() >= requirements['age_min']
        if "age_max" in requirements:
            available = available and hcp.age() <= requirements['age_max']
        if "gender" in requirements:
            available = available and hcp.sex == requirements['gender']
        if 'serviceType' in requirements:
            available = available and hcp.typeHS == requirements['serviceType']
        return available

    def get_schedule(self):
        startDate = self.requirements['startDate']
        numDaysRequested = self.requirements['numDaysRequested']
        daysRequested = self.distribution['unassigned']
        if "flexibleTime" in self.requirements:
            flexibleTime = self.requirements['flexibleTime']
            startTime = None
            endTime = None
        else:
            startTime = self.requirements['startTime']
            endTime = self.requirements['endTime']
            flexibleTime = False
        current_schedule = get_time_schedule(startDate, numDaysRequested, daysRequested, startTime, endTime,
                                             flexibleTime)
        return current_schedule

    def get_available_hcp(self, startTime=None, endTime=None, daysRequested=None, flexibleTime=False):
        distribution = self.distribution
        requirements = self.requirements
        hcp_list = Healthcareprofessional.objects.filter(enroll=True, deleted=False)
        required_hcp_list = []
        if not daysRequested:
            daysRequested = distribution['unassigned']
            if len(daysRequested) == 0:
                return []
        startDate = requirements['startDate']
        numDaysRequested = requirements['numDaysRequested']
        if not startTime:
            startTime = requirements['startTime']
        if not endTime:
            endTime = requirements['endTime']

        current_schedule = get_time_schedule(startDate, numDaysRequested, daysRequested, startTime, endTime,
                                             flexibleTime)
        for hcp in hcp_list:
            hcp_schedule = hcp.get_all_schedule()
            available = not is_conflict(hcp_schedule, current_schedule)
            hcp.schedule['available'] = available and self.check_requirements(hcp, requirements)
            required_hcp_list.append(hcp)

        return required_hcp_list

    def remove_hcp_schedule(self):
        for item in self.distribution['assigned']:
            hcp = Healthcareprofessional.objects.get(pID=item['hcp'])
            if str(self.requestID) in hcp.schedule:
                del hcp.schedule[str(self.requestID)]
                hcp.save()

    def remove(self):
        self.deleted = True
        self.remove_hcp_schedule()
        self.save()

    def get_billing_account(self):
        billing = BillingAccount.objects.get(request=self)
        ret = {
            "billingAccountID": 1000 + billing.pk,
            "requestID": self.pk,
            "detail": [],
            'patientName': f"{self.patientFirstName} {self.patientLastName}"}
        for assign in self.distribution['assigned']:
            item = {
                'hcpName': assign['hcpName'],
                'pID': int(assign['hcp']),
                'records': [],
                "total": billing.total,
                'payedTotal': billing.paid,
                'unPayedTotal': billing.total - billing.paid
            }
            wcs = WorkRecord.objects.filter(hcp__pID=int(assign['hcp']), request_id=int(self.requestID))
            for wc in wcs:
                item['records'].append({
                    "workDate": wc.workDate,
                    "startTime": wc.startTime.strftime("%H:%M"),
                    "endTime": wc.endTime.strftime("%H:%M"),
                    "amount": wc.cal_amount(self.hourlyRate)
                })
            ret['detail'].append(item)
        return ret

    class Meta:
        db_table = 'Requests'


class Advertise(models.Model):
    adID = models.AutoField(db_column='adID', primary_key=True)
    typeHS = models.CharField(db_column='typeHS', max_length=15)
    qualification = models.CharField(db_column='qualification', max_length=10)
    education = models.CharField(db_column='education', max_length=100, default="")
    yearOExp = models.IntegerField(db_column='yearOExp')
    updateTime = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def remove(self):
        self.deleted = True
        self.save()

    class Meta:
        db_table = 'Advertise'


class WorkRecord(models.Model):
    request = models.ForeignKey(Requests, on_delete=models.CASCADE)
    hcp = models.ForeignKey(Healthcareprofessional, on_delete=models.CASCADE)
    workDate = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    updateTime = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def cal_amount(self, hourlyRate=100.0):
        endTime = timeFormat(self.endTime)
        startTime = timeFormat(self.startTime)
        duration = datetime.datetime.combine(datetime.date.today(), endTime) - datetime.datetime.combine(
            datetime.date.today(), startTime)
        hours = round(duration.seconds / 60 / 60, 2)
        return round(float(hourlyRate) * hours, 2)

    def remove(self):
        self.deleted = True
        self.save()

    def add_billing_account(self):
        billing = BillingAccount.objects.filter(request=self.request).first()
        total = self.cal_amount(self.request.hourlyRate)
        if billing:
            billing.total += total
            billing.unpaid += total
        else:
            billing = BillingAccount.objects.create(request=self.request, total=total, unpaid=total)
        billing.save()

    def add_hcp_salary(self):
        salaryRecord = BillingAccount.objects.filter(hcp=self.hcp).first()
        total = self.cal_amount(self.hcp.salary)
        if salaryRecord:
            salaryRecord.total += total
            salaryRecord.unpaid += total
        else:
            salaryRecord = BillingAccount.objects.create(hcp=self.hcp, total=total, unpaid=total)
        salaryRecord.save()

    class Meta:
        db_table = 'WorkRecord'


class ServiceRequest(models.Model):
    userTo = models.ForeignKey(Users, related_name="user_to", on_delete=models.CASCADE)
    userFrom = models.ForeignKey(Users, related_name="user_from", on_delete=models.CASCADE)
    request = models.ForeignKey(Requests, on_delete=models.CASCADE)
    status = models.IntegerField(null=True, blank=True, help_text="0:申请,1:驳回,2:成功")
    updateTime = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def remove(self):
        self.deleted = True
        self.save()

    class Meta:
        db_table = 'ServiceRequest'


class BillingAccount(models.Model):
    hcp = models.ForeignKey(Healthcareprofessional, on_delete=models.CASCADE, null=True, blank=True)
    request = models.ForeignKey(Requests, on_delete=models.CASCADE, null=True, blank=True)
    total = models.FloatField()
    paid = models.FloatField(default=0)
    unpaid = models.FloatField(default=0)
    updateTime = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        if self.hcp:
            return f"Hcp Billing Record- {self.pk}"
        else:
            return f"Patient Billing Record- {self.pk}"

    def remove(self):
        self.deleted = True
        self.save()

    class Meta:
        db_table = 'BillingAccount'


class PayRecord(models.Model):
    billingAccount = models.ForeignKey(BillingAccount, on_delete=models.CASCADE)
    amount = models.FloatField()
    paidTime = models.DateTimeField(default=datetime.datetime.now)
    updateTime = models.DateTimeField(default=datetime.datetime.now)
    deleted = models.BooleanField(default=False)

    def remove(self):
        self.deleted = True
        self.save()

    class Meta:
        db_table = 'PayRecord'

from django.db import models
from datetime import datetime
import random
import hashlib
from .utils import sent_email


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

    class Meta:
        db_table = 'CareTaker'


class Healthcareprofessional(models.Model):
    pID = models.IntegerField(db_column='PID', primary_key=True)  # Field name made lowercase.
    firstName = models.CharField(db_column='firstName', max_length=50)  # Field name made lowercase.
    lastName = models.CharField(db_column='lastName', max_length=50)  # Field name made lowercase.
    sex = models.CharField(max_length=1)
    ssn = models.DecimalField(db_column='SSN', max_digits=9, decimal_places=0)  # Field name made lowercase.
    typeHS = models.CharField(db_column='Type_H_S', max_length=15)  # Field name made lowercase.
    qualification = models.CharField(db_column='Qualification', max_length=10)  # Field name made lowercase.
    qualificationDate = models.DateField(db_column='Qualification_Date',
                                         default=datetime.now)  # Field name made lowercase.
    yearOExp = models.IntegerField(db_column='Year_O_Exp')  # Field name made lowercase.
    phoneNumber = models.DecimalField(db_column='phoneNumber', max_digits=10, decimal_places=0, blank=True,
                                      null=True)  # Field name made lowercase.
    postalAddress = models.CharField(db_column='postalAddress', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    email = models.CharField(max_length=100, blank=True, null=True)
    enroll = models.BooleanField(blank=True, null=True, default=False)
    advertiseID = models.ForeignKey('Advertise', models.CASCADE, db_column='advertiseID', blank=True,
                                    null=True)  # Field name made lowercase.
    userID = models.ForeignKey('Users', models.CASCADE, db_column='userID', blank=True,
                               null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'HealthcareProfessional'


class Requests(models.Model):
    requestID = models.IntegerField(db_column='requestID', primary_key=True)  # Field name made lowercase.
    userID = models.ForeignKey('Users', models.CASCADE, db_column='userID')  # Field name made lowercase.
    patientFirstName = models.CharField(db_column='patientFirstName', max_length=50)  # Field name made lowercase.
    patientLastName = models.CharField(db_column='patientLastName', max_length=50)  # Field name made lowercase.
    sex = models.CharField(max_length=1)
    dateOfBirth = models.DateField(db_column='dateOfBirth')  # Field name made lowercase.
    locationOfService = models.CharField(db_column='locationOfService', max_length=30)  # Field name made lowercase.
    patientPhoneNumber = models.DecimalField(db_column='patientPhoneNumber', max_digits=10,
                                             decimal_places=0)  # Field name made lowercase.
    patientEmail = models.CharField(db_column='patientEmail', max_length=100)  # Field name made lowercase.
    serviceType = models.CharField(db_column='serviceType', max_length=10)  # Field name made lowercase.
    daysRequested = models.CharField(db_column='daysRequested', max_length=10, blank=True,
                                     null=True)  # Field name made lowercase.
    startTime = models.TimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
    endTime = models.TimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    numDaysRequested = models.IntegerField(db_column='numDaysRequested', blank=True,
                                           null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Requests'


class Roles(models.Model):
    roleID = models.AutoField(db_column='roleID', primary_key=True)  # Field name made lowercase.
    roleName = models.CharField(db_column='roleName', max_length=30)  # Field name made lowercase.

    class Meta:
        db_table = 'Roles'


class Securityquestions(models.Model):
    securityQuestionID = models.AutoField(db_column='securityQuestionID',
                                          primary_key=True)  # Field name made lowercase.
    question = models.CharField(max_length=255)

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
    username = models.CharField(db_column='userName', max_length=100)  # Field name made lowercase.
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

    class Meta:
        db_table = 'Users'


class Advertise(models.Model):
    adID = models.AutoField(db_column='AdID', primary_key=True)
    typeHS = models.CharField(db_column='Type_H_S', max_length=15)
    qualification = models.CharField(db_column='Qualification', max_length=10)
    education = models.CharField(db_column='education', max_length=100, default="")
    yearOExp = models.IntegerField(db_column='Year_O_Exp')

    class Meta:
        db_table = 'Advertise'

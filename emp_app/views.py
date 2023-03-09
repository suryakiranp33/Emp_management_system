# from django.http import HttpResponse
from .serializer import EmployeeLeaveCreateSerializer, Userserializer
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist

from .serializer import UserSerializer


import logging
from .models import Employee, LeaveStatus, LeaveSystem
# from rest_framework.response import Response
from .serializer import EmployeeCreateSerializer
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, 
                                     RetrieveUpdateAPIView)
logger = logging.getLogger(__name__)


                                
class EmployeDetail(RetrieveUpdateAPIView):
    queryset = Employee.objects.order_by('id').all()
    serializer_class = EmployeeCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    lookup_field = "pk"

    def perform_update(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                
                object_id = self.kwargs.get("pk")
                emp_obj = Employee.objects.get(id=object_id)
                data["message"] = "Employee detail"
                data["status"] = "success"
                data["code"] = 200

            else:
                data["message"] = "Failed"
                data["status"] = "failed"
                data['code'] = 422

        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "failed"
            data["message"] ='something_went_wrong'
            data['code'] = 500
        return data

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        data={}
        data["message"] ="enter_valid_inputs"
        data["status"] = "failed"
        return Response(data=data,status=406)          




class EmployeeUpdateView(RetrieveUpdateAPIView):
    queryset = Employee.objects.order_by('id').all()
    serializer_class = EmployeeCreateSerializer
    
    lookup_field = "pk"
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_update(self, serializer):
        try:
            data = {}
            
            if serializer.is_valid():
                serializer.save()
                data['message'] = 'Employee updated'
                data['status'] = 'Success'
                return data
            else:
                data['message'] = 'update_failed'
                data['details'] = serializer.errors
                data['status'] = 'Failed'
            return data
        except Exception as exception:
            logger.exception(
                "Exception occuring while updating Employee %s", exception
            )
            return {
                'status': 'Failed',
                'message': 'something_went_wrong'
            }

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
       
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
       
        data = self.perform_update(serializer)
        
        if data['status'] == 'Success':
            return Response(data=data, status=200)
        elif data['status'] == 'Failed':
            return Response(data=data, status=400)
        else:
            return Response(data=data, status=500)

class EmployeeDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Employee.objects.order_by('id').all()
    serializer_class = EmployeeCreateSerializer
    lookup_field = "pk"

    def perform_destroy(self, instance):
        try:
            data = {}
            instance.delete()
            data['status'] = "success"
            data['message'] = 'employee_deleted'
            return data
        except Exception as exception:
            logger.exception(
                "Exception occuring while deleting Employee %s", exception
            )
            data['message'] = 'something_went_wrong'
            data['status'] = 'failed'
            return data

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        if data['status'] == 'success':
            return Response(data=data, status=200)
        elif data['status'] == 'failed':
            return Response(data=data, status=400)
        else:
            return Response(data=data, status=500)

class EmployeeListView(ListAPIView):
    serializer_class = EmployeeCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get_queryset(self, *args, **kwargs):

        try:
           
            obj = Employee.objects.all()

            return obj
        except Exception as exception:
            logger.exception(
                "Exception occuring while fetching Employee %s", exception
            )
            


class LeaveCreateView(CreateAPIView):

   

    queryset = LeaveSystem.objects.order_by('id').all()
    serializer_class = EmployeeLeaveCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


    def perform_create(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                
                  status=LeaveStatus.objects.get(status="Pending")
                  if status:
                      action_plan = serializer.save(status=status)
                  data['status'] = 'success'
                  data['message'] = 'created'
                  data["code"]=200
                
                
            else:
                data['message'] = 'create_failed'
                data['details'] = serializer.errors
                data['status'] = 'failed'
                data["code"]=422
            return data

        except Exception as exception:
            logger.exception(
                "Exception occuring while fetching  %s", exception
            )
            data["status"] = "failed"
            data["message"] = 'something_went_wrong'
            data['code'] = 500

        print(data)
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = self.perform_create(serializer)
        if data['status'] == True:
            return Response(data=data, status=201)
        elif data['status'] == False:
            return Response(data=data, status=400)
        else:
            return Response(data=data, status=500)
        

class LeaveListView(ListAPIView):
    serializer_class = EmployeeLeaveCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self, *args, **kwargs):
        try:
            obj = LeaveSystem.objects.all()
            return obj
        except Exception as exception:
            logger.exception(
                "Exception occuring while fetching  %s", exception
            )

class LeaveRejectView(RetrieveUpdateAPIView):
    queryset = LeaveSystem.objects.all()
    serializer_class = EmployeeLeaveCreateSerializer
    lookup_field = "pk"
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_update(self, serializer):
        data = {}
        user=[]
        try:
            if serializer.is_valid():
              if self.request.user.is_superuser==True:
                  object_id = self.kwargs.get("pk")
                  obj = LeaveSystem.objects.get(id=object_id)
                  status = self.request.data.get("status")
                  status=LeaveStatus.objects.get(id=status)
                  policy_obj = serializer.save(
                      status=status
                  )   
                  if policy_obj.status.status=="Reject":
                      data["message"] ="rejected"
                      data["status"] = "success"
                      data["code"] = 200
                  elif policy_obj.status.status=="Approve":
                      data["message"] ="Approved"
                      data["status"] = "success"
                      data["code"] = 200
                  elif policy_obj.status.status=="Pending":
                      data["message"] ="Pending"
                      data["status"] = "success"
                      data["code"] = 200
              else:
                  data['status'] = 'failed'
                  data['message'] = 'Not an admin'
                  data["code"]=400
            else:
                data["message"] = "update_failed"
                data["details"] = serializer.errors
                data["status"] = "failed"
                data['code'] = 422

        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "failed"
            data["message"] = 'something_went_wrong'
            data['code'] = 500
        return data

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        data = self.perform_update(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)
    
class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            Employee.objects.create(user=user,email=user.email,employee_name=user.username)
            token = Token.objects.create(user=user)
            data = {
                'token': token.key,
                'user': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserLogoutView(APIView):
#     def post(self, request):
#         logout(request)
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

class LogoutUser(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Logout successfull"}, status=status.HTTP_200_OK)



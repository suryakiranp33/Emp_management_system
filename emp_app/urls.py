from . import views
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegistrationView,LogoutUser

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_login'),
    # path('logout/', UserLogoutView.as_view(), name='api_logout'),
    path('logoutuser/', LogoutUser.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='api_register'),
    path(
        "employee/<int:pk>/edit/",
        views.EmployeeUpdateView.as_view(),
    ),
    path(
        "employee/<int:pk>/delete/",
        views.EmployeeDeleteView.as_view(),
    ),
 
    path("employeelist/",views.EmployeeListView.as_view(),),
    

    path(
        "employeedetail/<int:pk>/",
        views.EmployeDetail.as_view()
        ),

    path(
        "employee/leavecreate",
        views.LeaveCreateView.as_view(),
        
    ),
    path(
        "employee/leave/list/",
        views.LeaveListView.as_view(),
    ),
    path(
        "leave/status/<int:pk>/change",
        views.LeaveRejectView.as_view(),
    ),

]

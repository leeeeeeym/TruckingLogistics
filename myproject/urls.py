"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

#User Authentication
from django.urls import path, include
from django.contrib.auth import views as auth_views

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    
    #Dashboard URLS
    path('driver_dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('container/start/<int:container_id>/', views.start_container, name='start_container'),
    path('container/complete/<int:container_id>/', views.complete_container, name='complete_container'),
    path('container/cancel/<int:container_id>/', views.cancel_container, name='cancel_container'),


    # Customer URLs
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/update/<int:pk>/', views.customer_update, name='customer_update'),
    path('customers/delete/<int:pk>/', views.customer_delete, name='customer_delete'),
    path('bookings/cancel/<int:pk>/', views.booking_cancel, name='booking_cancel'),


    # User URLs
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/update/<int:pk>/', views.user_update, name='user_update'),
    path('users/delete/<int:pk>/', views.user_delete, name='user_delete'),

    # Booking URLs
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/create/', views.booking_create, name='booking_create'),
    path('bookings/update/<int:pk>/', views.booking_update, name='booking_update'),
    path('bookings/delete/<int:pk>/', views.booking_delete, name='booking_delete'),
    path('bookings/confirm/<int:pk>/', views.booking_confirm, name='booking_confirm'),  # Add this line
    path('bookings/cancel/<int:pk>/', views.booking_cancel, name='booking_cancel'),  # Ensure cancel is also consistent

    # Container URLs
    path('containers/', views.container_list, name='container_list'),
    path('containers/create/', views.container_create, name='container_create'),
    path('containers/update/<int:pk>/', views.container_update, name='container_update'),
    path('containers/delete/<int:pk>/', views.container_delete, name='container_delete'),

    # Container Status URLs
    path('container_statuses/', views.container_status_list, name='container_status_list'),
    path('container_statuses/create/', views.container_status_create, name='container_status_create'),
    path('container_statuses/update/<int:pk>/', views.container_status_update, name='container_status_update'),
    path('container_statuses/delete/<int:pk>/', views.container_status_delete, name='container_status_delete'),

    # Role URLs
    path('roles/', views.role_list, name='role_list'),
    path('roles/create/', views.role_create, name='role_create'),
    path('roles/update/<int:pk>/', views.role_update, name='role_update'),
    path('roles/delete/<int:pk>/', views.role_delete, name='role_delete'),

    path('drivers/', views.driver_list, name='driver_list'),  # List of drivers
    path('drivers/create/', views.driver_create, name='driver_create'),  # Create a new driver
    path('drivers/update/<int:pk>/', views.driver_update, name='driver_update'),  # Update an existing driver
    path('drivers/delete/<int:pk>/', views.driver_delete, name='driver_delete'),  # Delete a driver
    path('drivers/form/<int:pk>/', views.driver_form, name='driver_form'),  # Form for creating or updating a driver

    #User Authentication
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('validate-username/', views.validate_username, name='validate_username'),
    path('validate-email/', views.validate_email, name='validate_email'),

    path('customers/assign/<int:pk>/', views.assign_user_to_customer, name='assign_user_to_customer'),
    path('containers/assign/<int:container_id>/', views.assign_driver, name='assign_driver'),


    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('validate-username/', views.validate_username, name='validate_username'),
    path('validate-email/', views.validate_email, name='validate_email'),

    path('customers/assign/<int:pk>/', views.assign_user_to_customer, name='assign_user_to_customer'),
    path('containers/assign/<int:container_id>/', views.assign_driver, name='assign_driver'),
]

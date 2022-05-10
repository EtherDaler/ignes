from django.urls import path, include
from .views import *

urlpatterns = [
	path('', main, name='main'),
	path('logout/', logout_page, name='logout'),
	path('login/', login_page, name='login'),
	path('create_analys/', create_analys, name='create_analys'),
	path('analys_info/<str:slug>-<int:id>/', analys_info, name='analys_info'),
	path('analys_not_ready_list', analys_not_ready_list, name='analys_not_ready_list'),
	path('analys_ready_list', analys_ready_list, name='analys_ready_list'),
	path('update_analys/<str:slug>-<int:id>/', update_analys, name='update_analys'),
	path('appointment/', appointment, name='appointment'),
	path('request_appointments/', request_appointments, name='request_appointments'),
	path('appointments_list/', appointments_list, name='appointments_list'),
	path('delete_appointment/<int:id>/', delete_appointment, name='delete_appointment'),
	path('change_appointment/<int:id>/', change_appointment, name='change_appointment'),
	path('questions/', questions, name='questions'),

	path('about_us/', about_us, name='about_us'),
	path('services/', services, name='services'),
	path('price_list/', price_list, name='price_list'),
	path('blogs_list/', blogs_list, name='blogs_list'),
	path('blog/<str:slug>/', blog, name='blog'),
	path('crew_list', crew_list, name='crew_list'),
	path('crew_info/<int:id>/', crew_info, name='crew_info'),
	path('contacts/', contacts, name='contacts'),
	path('get_analys_from_code/', get_analys_from_code, name='get_analys_from_code'),
]
from django.shortcuts import render, redirect
from .models import *
import qrcode
from django.contrib import messages
from .decorators import unauthenticated, authenticated, isstaff
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import choice
from string import digits
from django.http import HttpResponse
import json
from django.utils.translation import gettext as _
from dateutil import tz

def convert_date_from_str(date):
    #convert only date in format 'yyyy.mm.dd' or 'yyyy-mm-dd' or 'yyyy/mm/dd'
    day = 0
    year = 0
    month = 0 
    dot_count = 0
    year = int(date[0] + date[1] + date[2] + date[3])
    if date[5] == '0':
        month = int(date[6])
    else:
        month = int(date[5] + date[6])
    if date[8] == '0':
        day = int( date[9])
    else:
        day = int(date[8] + date[9])
    return datetime.date(year, month, day)

def convert_time_from_str(time):
	hour = time[:2]
	minute = time[3:]
	second = 0
	TJ = tz.gettz('Asia / Tashkent') 
	return datetime.time(int(hour), int(minute), second, tzinfo=TJ)

def convert_datetime_from_str(date, time):
	year = int(date[0] + date[1] + date[2] + date[3])
	if date[5] == '0':
		month = int(date[6])
	else:
		month = int(date[5] + date[6])
	if date[8] == '0':
		day = int( date[9])
	else:
		day = int(date[8] + date[9])
	
	hour = time[:2]
	minute = time[3:]
	second = 0
	TJ = tz.gettz('Asia / Tashkent') 

	return datetime.datetime(year, month, day, int(hour), int(minute), second, tzinfo=TJ)

@authenticated
def login_page(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username = username, password = password)
		if user is not None:
			login(request, user)
			return redirect('main')
		else:
			messages.error(request, 'Указан неверный логин или пароль')
	return render(request, 'mainApp/login.html')

@unauthenticated
def logout_page(request):
	logout(request)
	return redirect('main')

def main(request):

	context = {
		'info': MyInfo.objects.all().first(),
		'reviews': Reviews.objects.all(),
		'price_list': Services.objects.filter(show_price=True),
		'services': Services.objects.filter(show=True),
		'all_services': Services.objects.all(),
		'carusel': Carusel.objects.filter(show=True).order_by('deque'),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_main': 'active',
	}

	return render(request, 'mainApp/main.html', context)

@isstaff
def create_analys(request, *args, **kwargs):
	if request.method == 'POST':
		type = request.POST.get('type')
		person_full_name = request.POST.get('full_name')
		person_citizenship = request.POST.get('citizenship')
		person_date_of_birth = request.POST.get('date_of_birth')
		category = AnalysType.objects.get(id = int(type))
		analys = Analys.objects.create(
			type = category,
			person_full_name = person_full_name,
			person_citizenship = person_citizenship,
			person_date_of_birth = person_date_of_birth
		)
		qr_code = qrcode.make('http://127.0.0.1:8000/analys_info/' + str(analys.slug) + '-' + str(analys.id))
		url = 'media/qr_codes/qr_' + str(analys.id) + '_' + person_full_name + '_' + str(analys.analys_datetime.year) + '_' + str(analys.analys_datetime.month) + "_" + str(analys.analys_datetime.day) + "_" + str(analys.analys_datetime.hour) + "_" + str(analys.analys_datetime.minute) + '.png'
		file = qr_code.save('./media/qr_codes/qr_' + str(analys.id) + '_' + person_full_name + '_' + str(analys.analys_datetime.year) + '_' + str(analys.analys_datetime.month) + "_" + str(analys.analys_datetime.day) + "_" + str(analys.analys_datetime.hour) + "_" + str(analys.analys_datetime.minute) + '.png')
		print(str(url[6:]))
		analys.qr_code = str(url[6:])
		str_nums = '123456789'
		generate_code = list()
		for i in range(16 - len(str(analys.id))):
			generate_code.append(choice(str_nums))
		code = ''.join(generate_code) + str(analys.id)
		analys.code = int(code)
		analys.save()
		messages.info(request, 'Анализы добавлены в базу данных.')
		return redirect('create_analys')
	context = {
		'types': AnalysType.objects.all(),
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_create': 'active',
	}
	return render(request, 'mainApp/create_analys.html', context)

@isstaff
def analys_not_ready_list(request, *args, **kwargs):
	dataset = Analys.objects.filter(ready = False).order_by('analys_datetime')
	kwargs['dataset'] = dataset
	analys_list = dataset
	paginator = Paginator(analys_list, 10)
	page = request.GET.get('page', 1)
	try:
		analys_list = paginator.page(page)
	except PageNotAnInteger:
		analys_list = paginator.page(1)
	except EmptyPage:
		analys_list = paginator.page(paginator.num_pages)
	context = {
		'analys_list': analys_list,
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_wait': 'active',
	}
	return render(request, 'mainApp/analys_not_ready_list.html', context)

@isstaff
def analys_ready_list(request, *args, **kwargs):
	dataset = Analys.objects.filter(ready = True)
	kwargs['dataset'] = dataset
	analys_list = dataset
	paginator = Paginator(analys_list, 10)
	page = request.GET.get('page', 1)
	try:
		analys_list = paginator.page(page)
	except PageNotAnInteger:
		analys_list = paginator.page(1)
	except EmptyPage:
		analys_list = paginator.page(paginator.num_pages)
	context = {
		'analys_list': analys_list,
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_ready': 'active',
	}
	return render(request, 'mainApp/analys_ready_list.html', context)

@isstaff
def update_analys(request, slug, id):
	now = datetime.datetime.now()
	analys = Analys.objects.get(slug = slug, id = id)
	spec_fields = []
	for field in analys.type.extra_fields.all():
		spec_fields.append(field.name)
	if request.method == 'POST':
		comments = request.POST.get('comments')
		method = request.POST.get('method')
		datas = {}
		for data in spec_fields:
			datas[data] = request.POST.get(data)
		for data in datas.keys():
			field = ExtraFields.objects.get(type = analys.type, name = data)
			analys.values.create(
				type = analys.type,
				field = field,
				name = datas[data]
			)
		analys.comments = comments
		analys.method = method
		analys.analys_finish_datetime = now
		analys.ready = True
		analys.save()
		messages.info(request, 'Анализы обновлены')
		return redirect('analys_ready_list')
	context = {
		'fields': spec_fields,
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_ready': 'active',
	}
	return render(request, 'mainApp/update_analys.html', context)

def analys_info(request, slug, id):
	analys = Analys.objects.get(slug = slug, id = id)
	res = []
	for field in analys.type.extra_fields.all():
		try:
			val = analys.values.get(field = field)
			res.append({'field': field.name, 'value': val.name})
		except ExtraFieldsValue.DoesNotExist:
			val = ''
			res.append({'field': field.name, 'value': val})
	context = {
		'analys': analys,
		'info': MyInfo.objects.all().first(),
		'results': res,
		'last_services': Services.objects.all()[:5]
	}
	return render(request, 'mainApp/analys_info.html', context)

def appointment(request):
	response = {}
	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		second_name = request.POST.get('second_name')
		phone = request.POST.get('phone')
		service = request.POST.get('service')
		adress = request.POST.get('adress')


		Appointment.objects.create(
			full_name = first_name + ' ' + second_name,
			phone = phone,
			service = Services.objects.get(name = service),
			felial = Felials.objects.get(adress = adress)
		)

		response['result'] = 'Вы успешно зарегистрировались на прием, ожидайте нашего звонка.'

		return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)
	else:
		response['result'] = 'Произошла ошибка, повторите попытку позже.'
		return HttpResponse(
			json.dumps(response),
			content_type="application/json"
		)

def request_appointments(request, *args, **kwargs):
	dataset = Appointment.objects.filter(appointment_datetime = None, show = True)
	kwargs['dataset'] = dataset
	appointments_list = dataset
	paginator = Paginator(appointments_list, 10)
	page = request.GET.get('page', 1)
	try:
		appointments_list = paginator.page(page)
	except PageNotAnInteger:
		appointments_list = paginator.page(1)
	except EmptyPage:
		appointments_list = paginator.page(paginator.num_pages)
	context = {
		'appointments_list': appointments_list,
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_requests': 'active',
	}
	return render(request, 'mainApp/request_appointments.html', context)

def appointments_list(request, *args, **kwargs):
	dataset = Appointment.objects.filter(appointment_datetime__gte = datetime.datetime.now(), show = True)
	for i in Appointment.objects.all():
		print(i.appointment_datetime)
	kwargs['dataset'] = dataset
	appointments_list = dataset
	paginator = Paginator(appointments_list, 10)
	page = request.GET.get('page', 1)
	try:
		appointments_list = paginator.page(page)
	except PageNotAnInteger:
		appointments_list = paginator.page(1)
	except EmptyPage:
		appointments_list = paginator.page(paginator.num_pages)
	context = {
		'appointments_list': appointments_list,
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5]
		,
		'link_writes': 'active',
	}
	return render(request, 'mainApp/appointments_list.html', context)

def delete_appointment(request, id):
	appointment = Appointment.objects.get(id = id)
	appointment.delete()
	return redirect('appointments_list')

def change_appointment(request, id):
	if request.method == 'POST':
		date = request.POST.get('date')
		time = request.POST.get('time')
		appointment = Appointment.objects.get(id=id)
		appointment.appointment_datetime = convert_datetime_from_str(date, time)
		appointment.save()
		messages.info(request, 'Запись назначена')
		return redirect('request_appointments')
	context = {
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_requests': 'active',
	}
	return render(request, 'mainApp/change_appointment.html', context)

def get_analys_from_code(request):
	if request.method == 'POST':
		full_name = request.POST.get('full_name')
		date_of_birth = request.POST.get('date_of_birth')
		code = request.POST.get('code')
		try:
			analys = Analys.objects.get(person_full_name = full_name, person_date_of_birth = date_of_birth, code = code)
			return redirect('analys_info', slug=analys.slug, id=analys.id)
		except Analys.DoesNotExist:
			messages.info(request, 'Указаны неверные данные')
	context = {
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_results': 'active',
	}
	return render(request, 'mainApp/get_analys_from_code.html', context)

def blogs_list(request, *args, **kwargs):
	dataset = Blogs.objects.all().order_by('date')
	kwargs['dataset'] = dataset
	blogs_list = dataset
	paginator = Paginator(blogs_list, 6)
	page = request.GET.get('page', 1)
	try:
		blogs_list = paginator.page(page)
	except PageNotAnInteger:
		blogs_list = paginator.page(1)
	except EmptyPage:
		blogs_list = paginator.page(paginator.num_pages)
	context = {
		'blogs_list': blogs_list,
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_blogs': 'active',
	}
	return render(request, 'mainApp/blogs_list.html', context)

def blog(request, slug):
	blog = Blogs.objects.get(slug=slug)
	blog.watch_up()
	blog.save()
	context = {
		'blog': blog,
		'popular_blogs': Blogs.objects.all().order_by('-watch')[:5],
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_blogs': 'active',
	}
	return render(request, 'mainApp/blog.html', context)

def about_us(request):
	context = {
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_about': 'active',
	}

	return render(request, 'mainApp/about_us.html', context)

def crew_list(request):
	context = {
		'crew': Crew.objects.all(),
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_crew': 'active',
	}
	return render(request, 'mainApp/crew_list.html', context)

def crew_info(request, id):
	member = Crew.objects.get(id=id)
	context = {
		'member': member,
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_crew': 'active',
	}
	return render(request, 'mainApp/crew_info.html', context)

def price_list(request):
	services = Services.objects.all()
	context = {
		'price_list': services,
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_prices': 'active',
	}
	return render(request, 'mainApp/price_list.html', context)

def services(request):
	services = Services.objects.all()
	context = {
		'services': services,
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_services': 'active',
	}
	return render(request, 'mainApp/services.html', context)

def contacts(request):
	if request.method == 'POST':
		Questions.objects.create(
			name = request.POST.get('name'),
			email = request.POST.get('email'),
			subject = request.POST.get('subject'),
			message = request.POST.get('message')
		)
		messages.info(request, 'Ваше письмо успешно отправлено, дождитесь ответа, который придет на указанный вами email.')
	context ={
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_contacts': 'active',
	}
	return render(request, 'mainApp/contacts.html', context)

def questions(request, *args, **kwargs):
	dataset = Questions.objects.all().order_by('-date')
	kwargs['dataset'] = dataset
	questions = dataset
	paginator = Paginator(questions, 6)
	page = request.GET.get('page', 1)
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		questions = paginator.page(1)
	except EmptyPage:
		questions = paginator.page(paginator.num_pages)
	context = {
		'questions': questions,
		'info': MyInfo.objects.all().first(),
		'recent_blogs': Blogs.objects.all().order_by('-date')[:3],
		'last_services': Services.objects.all()[:5],
		'link_questions': 'active',
	}
	return render(request, 'mainApp/questions.html', context)


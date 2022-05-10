from django.db import models
import datetime
import pytz
from django.utils import timezone
from pytils.translit import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

def default_datetime():
	now = timezone.now()
	return datetime.datetime.now()

def default_date():
	return datetime.date.today()

class MyInfo(models.Model):
	name = models.CharField(max_length=255, verbose_name="Название")
	description = models.TextField(verbose_name="Описание", blank=True)
	inn = models.BigIntegerField(default=0, verbose_name="ИНН")
	license = models.CharField(max_length=255, verbose_name="Лицензия")
	min_of_just = models.CharField(max_length=255, verbose_name="Министрерство юстиций")
	adress = models.CharField(max_length=255, verbose_name="Адресс")
	email = models.CharField(max_length=255, verbose_name="Email")
	phone = models.CharField(max_length=255, verbose_name="Телефон")
	cheff_name = models.CharField(max_length=255, verbose_name='Имя владельца', null=True)
	cheff_photo = models.ImageField(upload_to='cheff', default='no_user.png', verbose_name='Фото владельца')
	photo = models.ImageField(upload_to='felials/', default='net_photo.png')
	favicon = models.ImageField(upload_to='favicon', default='net_photo.png', verbose_name='Фавикон')
	opened_from = models.TimeField(verbose_name='Открыто с ', blank = True, null = True)
	opened_until = models.TimeField(verbose_name='Открыто до ', blank = True, null=True)
	week_days_opened = models.CharField(max_length=255, verbose_name='Дни недели, в которые заведение открыто (Пон. - Суб.)', blank=True, null=True)
	week_days_off = models.CharField(max_length=255, verbose_name='Дни недели, в которые заведение закрыто (Воск.)', blank=True, null=True)
	instagram = models.CharField(max_length=255, verbose_name='Ссылка на instagram', blank=True, null=True)
	facebook = models.CharField(max_length=255, verbose_name='Ссылка на facebook',  blank=True, null=True)
	show_price_list = models.BooleanField(default=True, verbose_name='Отображать price list')

	class Meta:
		verbose_name="Информация о лаборатории"
		verbose_name_plural = "Информация о лаборатории"

class Felials(models.Model):
	info = models.ForeignKey(MyInfo, on_delete=models.CASCADE, related_name='felials')
	city = models.CharField(max_length=255, verbose_name='Город', default='')
	adress = models.CharField(max_length=255, verbose_name="Адресс")
	photo = models.ImageField(upload_to='felials/', default='net_photo.png')
	phone = models.CharField(max_length=255, verbose_name='Телефон', blank=True, null=True)

	class Meta:
		verbose_name="Филиаллы"
		verbose_name_plural = "Филиаллы"

class ExtraContacts(models.Model):
	info = models.ForeignKey(MyInfo, on_delete=models.CASCADE, related_name='extra_contacts')
	email = models.CharField(max_length=255, verbose_name="Email", blank=True)
	phone = models.CharField(max_length=255, verbose_name="Телефон", blank=True)

	class Meta:
		verbose_name="Дополнительные контакты"
		verbose_name_plural = "Дополнительные контакты"

class Category(models.Model):
	name = models.CharField(max_length=255, verbose_name='Название')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name="Категория анализов"
		verbose_name_plural = "Категория анализов"


class AnalysType(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', null=True)
	logo = models.ImageField(upload_to='analys_types', verbose_name='Лого', default='probirka.png')
	name = models.CharField(max_length=255, verbose_name='Название')
	description = models.TextField(verbose_name="Описание")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name="Виды анализов"
		verbose_name_plural = "Виды анализов"

class Analys(models.Model):
	type = models.ForeignKey(AnalysType, on_delete=models.CASCADE, verbose_name="Вид анализов")
	person_full_name = models.CharField(max_length=255, verbose_name="ФИО")
	person_citizenship = models.CharField(max_length=255, verbose_name="Гражданство")
	person_date_of_birth = models.DateField(default=default_date, verbose_name="Дата рождения")
	analys_datetime = models.DateTimeField(default=default_datetime, verbose_name='Дата и время сдачи анализов')
	analys_finish_datetime = models.DateTimeField(verbose_name='Дата и время подготовки анализов', blank=True, null = True)
	method = models.CharField(max_length=512, verbose_name='Метод исследования', blank=True, null=True)
	comments = models.CharField(max_length=512, verbose_name='Примечания', blank=True, null=True)
	slug = models.SlugField(max_length=255, verbose_name='Слаг код', default='')
	qr_code = models.ImageField(upload_to='qr_codes', verbose_name='QR код', blank=True)
	code = models.BigIntegerField(verbose_name = 'Номер анализов', blank=True, null=True)
	ready = models.BooleanField(default=False, verbose_name='Готовность', blank=True)

	def get_url(self):
		return 'http://10.154.25.91:8080/' + str(self.slug) + '-' + str(self.id)

	def __str__(self):
		return self.type.name

	def save(self, *args, **kwargs):
		self.slug = slugify(str(self.type.name) + '-' + str(self.person_full_name) + '-' + str(self.analys_datetime))
		super(Analys, self).save(*args, **kwargs)

	class Meta:
		verbose_name="Анализы"
		verbose_name_plural = "Анализы"

class ExtraFields(models.Model):
	type = models.ForeignKey(AnalysType, on_delete=models.CASCADE, verbose_name="Вид анализов", related_name='extra_fields')
	name = models.CharField(max_length=255, verbose_name="Название поля")

	def __str__(self):
		return '{} -> {}'.format(self.type, self.name)

	class Meta:
		verbose_name="Уникальные поля"
		verbose_name_plural = "Уникальные поля"

class ExtraFieldsValue(models.Model):
	type = models.ForeignKey(AnalysType, on_delete=models.CASCADE, verbose_name="Вид анализов")
	field = models.ForeignKey(ExtraFields, on_delete=models.CASCADE, verbose_name="Поле", related_name='values')
	analys = models.ForeignKey(Analys, on_delete=models.CASCADE, verbose_name="Анализ", default='', related_name = 'values')
	name = models.CharField(max_length=255, verbose_name="Значение поля")

	class Meta:
		verbose_name="Значения уникальных полей"
		verbose_name_plural = "Значения уникальных полей"

class Services(models.Model):
	mini_logo = models.ImageField(upload_to='services/mini_logo', default='net-photo.png', verbose_name='Мини изображение')
	logo = models.ImageField(upload_to='services/logo', default='net-photo.png', verbose_name='Изображение')
	name = models.CharField(max_length=255, verbose_name='Название')
	description = models.TextField(verbose_name='Описание')
	price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, blank=True)
	show = models.BooleanField(verbose_name='Отображение на главной', default=False)
	show_price = models.BooleanField(verbose_name='Отображать на прайс листе', default=False)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name="Услуги"
		verbose_name_plural = "Услуги"

class Questions(models.Model):
	name = models.CharField(max_length=255, verbose_name='Имя')
	email = models.EmailField(verbose_name='Email')
	subject = models.CharField(verbose_name='Тема сообщения', max_length=255, null=True)
	message = models.TextField(verbose_name='Письмо')
	date = models.DateTimeField(default=default_datetime())

	def __str__(self):
		return self.name

	class Meta:
		verbose_name="Вопросы"
		verbose_name_plural = "Вопросы"

class Answers(models.Model):
	question = models.ForeignKey(Questions, on_delete=models.CASCADE, verbose_name='Вопрос')
	answer = models.TextField(verbose_name='Ответ')
	date = models.DateTimeField(default=default_datetime())

	def __str__(self):
		return self.question

	class Meta:
		verbose_name="Ответы"
		verbose_name_plural = "Ответы"

class Carusel(models.Model):
	image = models.ImageField(upload_to='carusel', verbose_name='Изображение')
	title = models.CharField(max_length=255, verbose_name='Заголовок', blank=True)
	text = models.TextField(verbose_name='Текст', blank=True)
	button = models.BooleanField(verbose_name='Отображать кнопку')
	button_title = models.CharField(verbose_name='Надпись на кнопке', blank=True, max_length=255)
	href = models.CharField(verbose_name='Ссылка', max_length=255)
	show = models.BooleanField(default=True, verbose_name='Отображать на главной')
	deque = models.PositiveIntegerField(verbose_name='Порядок при отображении', default=1)

	def __str__(self):
		return 'Карусель: {}. Название: {}'.format(self.id, self.title)

	class Meta:
		verbose_name="Карусель"
		verbose_name_plural = "Карусель"

class Blogs(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор статьи', related_name='blogs')
	title = models.CharField(max_length=255, verbose_name='Заголовок')
	logo = models.ImageField(verbose_name='Обложка статьи', upload_to='blogs')
	mini_description = models.TextField(verbose_name='Мини описание (20 слов макс.)', blank=True, null=True)
	body = RichTextField(verbose_name='Блог')
	date = models.DateTimeField(verbose_name='Дата и время публикации', default=default_datetime())
	watch = models.PositiveIntegerField(default=0, verbose_name='Просмотров')
	slug = models.SlugField(max_length=255, verbose_name='Slug код', unique = True)

	def watch_up(self):
		self.watch += 1
		return self.watch

	def __str__(self):
		return self.title

	class Meta:
		verbose_name="Блоги"
		verbose_name_plural = "Блоги"

class Appointment(models.Model):
	full_name = models.CharField(max_length=255, verbose_name='Полное имя')
	phone = models.CharField(max_length=255, verbose_name='Номер телефона')
	service = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name='Процедура/услуга', related_name='appontments', blank=True, null=True)
	felial = models.ForeignKey(Felials, on_delete=models.CASCADE, verbose_name='Адрес', related_name='appintments', blank=True, null=True)
	appointment_datetime = models.DateTimeField(verbose_name='Дата и время записи', blank=True, null=True)
	date = models.DateTimeField(default=default_datetime(), verbose_name='Дата и время запроса')
	show = models.BooleanField(verbose_name='Показывать в списке записей', default=True)

	def __str__(self):
		return self.full_name

	class Meta:
		verbose_name="Записи на прием"
		verbose_name_plural = "Записи на прием"

class AboutUs(models.Model):
	text = RichTextField(verbose_name='Текст')

	class Meta:
		verbose_name="О нас"
		verbose_name_plural = "О нас"

class Crew(models.Model):
	full_name = models.CharField(verbose_name='ФИО', max_length=512)
	photo = models.ImageField(upload_to='crew', verbose_name='Фотография')
	instagram = models.CharField(max_length=255, verbose_name='Ссылка на Instagram', blank=True)
	facebook = models.CharField(max_length=255, verbose_name='Ссылка на facebook', blank=True)
	about = models.TextField(verbose_name='О сотруднике')
	position = models.CharField(verbose_name='Должность', max_length=255)
	education = models.CharField(verbose_name='Образование', max_length=512)

	def __str__(self):
		return self.full_name

	class Meta:
		verbose_name="Персонал"
		verbose_name_plural = "Персонал"

class Jobs(models.Model):
	crew = models.ForeignKey(Crew, on_delete=models.CASCADE, verbose_name='Сотрудник', related_name='jobs')
	place = models.CharField(max_length=255, verbose_name='Место работы')
	period = models.CharField(max_length=255, verbose_name='Период работы')

	class Meta:
		verbose_name="Опыт работы"
		verbose_name_plural = "Опыт работы"

class Reviews(models.Model):
	name = models.CharField(max_length=255, verbose_name='Имя')
	status = models.CharField(max_length=255, verbose_name='Социальный статус/должность (поле не обязателно для ввода)', blank=True)
	photo = models.ImageField(upload_to='reviews', default='no_user.png', verbose_name='Фотография')
	review = models.TextField(verbose_name='Отзыв')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name="Отзывы"
		verbose_name_plural = "Отзывы"
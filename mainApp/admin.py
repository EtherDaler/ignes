from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm
from mainApp.models import *


class FelialsFieldInline(admin.StackedInline):
	model = Felials

class ExtraContactssFieldInline(admin.StackedInline):
	model = ExtraContacts

class MyInfoAdmin(admin.ModelAdmin):
	inlines = [FelialsFieldInline, ExtraContactssFieldInline]

admin.site.register(MyInfo, MyInfoAdmin)


class ExtraFieldsFieldInline(admin.StackedInline):
	model = ExtraFields

class AnalysTypeAdmin(admin.ModelAdmin):
	inlines = [ExtraFieldsFieldInline]

admin.site.register(AnalysType, AnalysTypeAdmin)

class ExtraFieldsValueFieldInline(admin.StackedInline):
	model = ExtraFieldsValue

class AnalysAdmin(admin.ModelAdmin):
	list_display = ['type', 'person_full_name', 'person_date_of_birth', 'analys_datetime', 'analys_finish_datetime']
	search_fields = search_fields = ['type', 'person_full_name']
	list_filter = ['type', 'analys_datetime', 'analys_finish_datetime']
	prepopulated_fields = {'slug': ('type', 'person_full_name', 'analys_datetime')}
	inlines = [ExtraFieldsValueFieldInline]

admin.site.register(Analys, AnalysAdmin)

class CategoryAdmin(admin.ModelAdmin):
	search_fields = search_fields = ['name']

admin.site.register(Category, CategoryAdmin)

class ServicesAdmin(admin.ModelAdmin):
	list_display = ['name', 'price', 'show', 'show_price']
	list_filter = ['show', 'show_price']
	search_fields = ['name']

admin.site.register(Services, ServicesAdmin)

admin.site.register(Questions)

admin.site.register(Answers)

admin.site.register(Carusel)

class BlogsAdmin(admin.ModelAdmin):
	search_fields = ['title']
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Blogs, BlogsAdmin)

class AppointmentAdmin(admin.ModelAdmin):
	search_fields = ['full_name', 'phone']
	list_display = ['full_name', 'phone', 'service', 'felial', 'show']
	list_filter = ['service', 'felial', 'show']

admin.site.register(Appointment, AppointmentAdmin)

#admin.site.register(AboutUs)

class JobsInline(admin.StackedInline):
	model = Jobs

class CrewAdmin(admin.ModelAdmin):
	search_fields = ['full_name']
	inlines = [JobsInline]

admin.site.register(Crew, CrewAdmin)

class ReviewsAdmin(admin.ModelAdmin):
	search_fields = ['name', 'status', 'review']

admin.site.register(Reviews, ReviewsAdmin)
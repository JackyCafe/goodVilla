from django.contrib import admin

from chamberlain.models import MajorItem, DetailItem, Attendance


# Register your models here.

@admin.register(MajorItem)
class MajorItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MajorItem._meta.fields]


@admin.register(DetailItem)
class DetailItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DetailItem._meta.fields]


@admin.register(Attendance)
class DetailItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Attendance._meta.fields]

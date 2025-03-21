from django.contrib import admin

from .models import Wilaya, Daira, Commune


class WilayaAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["code", "name_fr", "name_ar"]
    search_fields = ["name_fr","name_ar"]

    list_filter = []


class DairaAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_select_related = ['wilaya']
    list_display = ["name_fr", "name_ar", "wilaya"]
    list_filter = ["wilaya"]
    search_fields = ["name_fr","name_ar"]


class CommuneAdmin(admin.ModelAdmin):
    list_select_related = ['daira', 'daira__wilaya']
    list_display = ["name_fr", "name_ar", "daira", "get_wilaya"]
    list_filter = ["daira__wilaya"]
    search_fields = ["name_fr","name_ar"]

    def get_wilaya(self, obj):
        return obj.daira.wilaya

admin.site.register(Wilaya, WilayaAdmin)
admin.site.register(Daira, DairaAdmin)
admin.site.register(Commune, CommuneAdmin)

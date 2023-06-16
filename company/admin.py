from django.contrib import admin

from .models import *

# Register your models here.


class AdminGroups(admin.ModelAdmin):
    list_display = ('company', 'group_name', 'group_type',
                    'group_color', 'group_description', 'created_at')
    search_fields = ('group_name',)
    ordering = ('group_name', 'group_type', 'created_at')


class AdminDomains(admin.ModelAdmin):
    list_display = ('company', 'client', 'group', 'domain_name', 'created_at')
    search_fields = ('domain_name',)
    ordering = ('domain_name', 'company', 'client', 'group', 'created_at')


class AdminDns(admin.ModelAdmin):
    list_display = ('company', 'domain', 'type', 'value', 'pri', 'created_at')
    search_fields = ('domain',)
    ordering = ('company', 'domain', 'type', 'value', 'pri', 'created_at')


class AdminWhois(admin.ModelAdmin):
    list_display = ('company', 'client', 'domain', 'updated_date',
                    'status', 'registrar', 'expiration_date', 'creation_date')
    search_fields = ('domain',)
    ordering = ('company', 'client', 'domain', 'updated_date',
                'status', 'registrar', 'expiration_date', 'creation_date')


class AdminGeoip(admin.ModelAdmin):
    list_display = ('company', 'domain', 'dns', 'city',
                    'country', 'region', 'status', 'created_at')
    search_fields = ('domain',)
    ordering = ('company', 'domain', 'dns', 'city',
                'country', 'region', 'status', 'created_at')

class AdminLog(admin.ModelAdmin):
    list_display = ('user', 'description', 'created_at')
    search_fields = ('user',)
    ordering = ('user', 'description', 'created_at')


admin.site.register(Group, AdminGroups)
admin.site.register(Domain, AdminDomains)
admin.site.register(Dns, AdminDns)

admin.site.register(Whois, AdminWhois)
admin.site.register(Log, AdminLog)
admin.site.register(Geoip, AdminGeoip)

admin.site.register(SslLookup)
admin.site.register(CmsLookup)

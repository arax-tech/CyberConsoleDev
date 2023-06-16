from rest_framework import serializers
from authentication.models import User

from .models import Group, Domain, Dns, Whois, Geoip, SslLookup, Log


class CompanyClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_active', 'is_admin']


class CompanyTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['created_at', 'updated_at']


class CompanyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ['created_at', 'updated_at']


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        exclude = ['created_at', 'updated_at']
        depth = 1


class CompanyDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        exclude = ['created_at', 'updated_at']
        depth = 1


class CompanyDNSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dns
        exclude = ['created_at', 'updated_at']
        depth = 1


class CompanyWhoisSerializer(serializers.ModelSerializer):
    # client = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='client'
    # )
    class Meta:
        model = Whois
        fields = '__all__'
        depth = 1


class CompanyGeoIpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geoip
        fields = ('id', 'company', 'domain', 'status', 'dns_type', 'country', 'countryCode', 'region',
                  'regionName', 'city', 'zip', 'lat', 'lon', 'timezone', 'isp', 'org', 'asn', 'ip')
        depth = 1


class CompanySSLSerializer(serializers.ModelSerializer):
    class Meta:
        model = SslLookup
        fields = ('id', 'company', 'domain', 'host', 'issued_to', 'issued_o', 'issuer_c', 'issuer_o', 'issuer_ou', 'issuer_cn', 'cert_sn', 'cert_sha1', 'cert_alg',
                  'cert_ver', 'cert_sans', 'cert_exp', 'cert_valid', 'valid_from', 'valid_till', 'validity_days', 'days_left', 'valid_days_to_expire', 'tcp_port')


class CmsLookupSerializer(serializers.Serializer):
    cms_id = serializers.UUIDField()
    cms_name = serializers.CharField()
    cms_url = serializers.URLField()
    detection_param = serializers.CharField()
    last_scanned = serializers.DateTimeField()
    url = serializers.URLField()
    wp_license = serializers.URLField()
    wp_plugins = serializers.CharField()
    wp_readme_file = serializers.URLField()
    wp_theme_version = serializers.CharField()
    wp_themes = serializers.CharField()
    wp_users = serializers.CharField()
    wp_version = serializers.CharField()
    domain = serializers.PrimaryKeyRelatedField(queryset=Domain.objects.all())

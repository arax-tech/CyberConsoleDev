from rest_framework import serializers
from authentication.models import User

from company.models import Group, Domain, Dns, Whois, Geoip, SslLookup, Log




class ClientDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        exclude = ['created_at', 'updated_at']
        depth = 1



from django.db import models
import uuid
# Create your models here.

from authentication.models import User
#
class Group(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_company", db_column='company')
    group_name = models.CharField(max_length=255)
    group_type = models.CharField(max_length=255)
    group_color = models.CharField(max_length=255, null=True)
    group_description = models.CharField(max_length=25, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.group_name
#
class Domain(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="domain_company", db_column='company')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="domain_client", db_column='client')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="domain_group", db_column='group')
    domain_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.domain_name
#
class Dns(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dns_company", db_column='company')
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="dns_domain", db_column='domain')
    type = models.CharField(max_length=255, null=False)
    value = models.CharField(max_length=255, null=False)
    pri = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.domain.domain_name + ' ' + self.type
#


class Whois(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="whois_company", db_column='company')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="whois_client", db_column='client', null=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="whois_domain", db_column='domain')
    updated_date = models.DateTimeField()
    status = models.CharField(max_length=255)
    registrar = models.CharField(max_length=255)
    expiration_date = models.DateTimeField()
    creation_date = models.DateTimeField()

    def __str__(self):
        return self.domain.domain_name

class Geoip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="geoip_company", db_column='company')
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="geoip_domain", db_column='domain')
    dns = models.ForeignKey(Dns, on_delete=models.CASCADE, related_name="geoip_dns", db_column='dns')
    dns_type = models.CharField(max_length=3, choices=(("A", "A"), ("NS", "NS"), ("MX", "MX")))
    status = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    countryCode = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    regionName = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    lon = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)
    isp = models.CharField(max_length=255)
    org = models.CharField(max_length=255)
    asn = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.domain.domain_name + ' ' + self.countryCode + ' ' + self.dns_type


class ServerInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="server_company", db_column='company')
    server_name = models.CharField(max_length=255)
    server_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    SERVER_TYPE_CHOICES = (
        ('WH', 'Webhosting'),
        ('M', 'Mail'),
    )
    server_type = models.CharField(max_length=2, choices=SERVER_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

class SslLookup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ssl_company", db_column='company')
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="ssl_domain", db_column='domain')
    host = models.CharField(max_length=255)
    issued_to = models.CharField(max_length=255)
    issued_o = models.CharField(max_length=255, blank=True, null=True)
    issuer_c = models.CharField(max_length=255)
    issuer_o = models.CharField(max_length=255)
    issuer_ou = models.CharField(max_length=255, blank=True, null=True)
    issuer_cn = models.CharField(max_length=255)
    cert_sn = models.CharField(max_length=255)
    cert_sha1 = models.CharField(max_length=255)
    cert_alg = models.CharField(max_length=255)
    cert_ver = models.IntegerField()
    cert_sans = models.TextField()
    cert_exp = models.BooleanField()
    cert_valid = models.BooleanField()
    valid_from = models.DateField()
    valid_till = models.DateField()
    validity_days = models.IntegerField()
    days_left = models.IntegerField()
    valid_days_to_expire = models.IntegerField()
    tcp_port = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.host

class CmsLookup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cms_company", db_column='company')
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="cms_domain", db_column='domain')
    cms_id = models.CharField(max_length=100, blank=True, null=True)
    cms_name = models.CharField(max_length=100, blank=True, null=True)
    cms_url = models.URLField(blank=True, null=True)
    cms_version = models.IntegerField(blank=True, null=True)
    detection_param = models.CharField(max_length=100, blank=True, null=True)
    last_scanned = models.DateTimeField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    wp_license = models.URLField(blank=True, null=True)
    wp_plugins = models.TextField(blank=True, null=True)
    wp_readme_file = models.URLField(blank=True, null=True)
    wp_theme_version = models.CharField(max_length=100, blank=True, null=True)
    wp_themes = models.CharField(max_length=100, blank=True, null=True)
    wp_users = models.TextField(blank=True, null=True)
    wp_version = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.domain.domain_name + ' ' + self.cms_id 

#
class Log(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="log_user", db_column='user')
    # user = models.CharField(max_length=255,)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

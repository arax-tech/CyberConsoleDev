import sys
from .models import Domain, Geoip, Dns
import uuid


def save_geoip_data(geoip_data, domain, dns_type, dns_id, company):
    status = geoip_data['status']
    country = geoip_data['country']
    countryCode = geoip_data['countryCode']
    region = geoip_data['region']
    regionName = geoip_data['regionName']
    city = geoip_data['city']
    zip = geoip_data['zip']
    lat = geoip_data['lat']
    lon = geoip_data['lon']
    timezone = geoip_data['timezone']
    isp = geoip_data['isp']
    org = geoip_data['org']
    asn = geoip_data['as']
    ip = geoip_data['query']
# Create or update the Whois model
    geoip, created = Geoip.objects.update_or_create(
        company=company,
        domain=domain,
        dns_type=dns_type,
        dns_id=dns_id,
        defaults={
            'status': status,
            'country': country,
            'countryCode': countryCode,
            'region': region,
            'regionName': regionName,
            'city': city,
            'zip': zip,
            'lat': lat,
            'lon': lon,
            'timezone': timezone,
            'isp': isp,
            'org': org,
            'asn': asn,
            'ip': ip
        }
    )
    return geoip

import sys
from .models import Domain, Whois
import uuid
import datetime


def save_whois_data(whois_data, domain, company, client):
    # print(company)
    updated_date = datetime.datetime.fromisoformat(whois_data["updated_date"][0])
    expiration_date = datetime.datetime.fromisoformat(whois_data["expiration_date"][0])
    creation_date = datetime.datetime.fromisoformat(whois_data["creation_date"][0])
    status = whois_data["status"][0].strip("[]")
    nameservers = whois_data["nameservers"][0].strip("[]")
    registrar = whois_data["registrar"][0].strip("[]")
# Create or update the Whois model
    whois, created = Whois.objects.update_or_create(
        company=company,
        client=client,
        domain=domain,
        defaults={
            'updated_date': updated_date,
            'status': status,
            'expiration_date': expiration_date,
            'creation_date': creation_date,
            'registrar': registrar
        }
    )
    return whois

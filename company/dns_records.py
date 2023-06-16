import sys
from .models import Domain, Dns
import dns.resolver
import uuid


def lookup_dns_records(company, domain_id):
    my_resolver = dns.resolver.Resolver()
    my_resolver.timeout = 1
    my_resolver.lifetime = 1
    
    try:
        domain = Domain.objects.get(id=domain_id)
        domain_name = domain.domain_name
    except Domain.DoesNotExist:
        print(f"Error: Domain with ID {domain_id} does not exist.")
        sys.exit(1)
# A
    try:
        
        answers = my_resolver.query(domain_name, "A")
        print(answers)
        for rdata in answers:
            defaults = {'domain': domain, 'company': company}
            dns_record = Dns.objects.filter(
                type='A', value=rdata.address, domain=domain_id)
            if dns_record.exists():
                dns_record.update(**defaults)
                print(
                    f"A record {rdata.address} already exists for: {domain_name}")
            else:
                Dns.objects.create(type='A', value=rdata.address, **defaults)
                print(f"A record {rdata.address} created for: {domain_name}")
    except dns.resolver.NXDOMAIN:
        print(f"Error: {domain_name} does not exist")
    except dns.resolver.NoAnswer:
        print(f"Error: No A record found for {domain_name}")
# MX
    my_resolver = dns.resolver.Resolver()
    try:
        answers = my_resolver.query(domain_name, "MX")
        for rdata in answers:
            defaults = {'domain': domain, 'company': company}
            dns_record, created = Dns.objects.get_or_create(
                type='MX',
                value=rdata.exchange,
                defaults=defaults
            )
            if not created:
                existing_record = Dns.objects.get(
                    type='MX', value=rdata.exchange)
                if existing_record.pri != rdata.preference:
                    Dns.objects.filter(id=existing_record.id).update(
                        pri=rdata.preference)
                    print(
                        f"MX record {rdata.exchange} changed Priority from {existing_record.pri} to {rdata.preference} for: {domain_name}")
    except dns.resolver.NXDOMAIN:
        print(f"Error: {domain_name} does not exist")
    except dns.resolver.NoAnswer:
        print(f"Error: No MX record found for {domain_name}")
# TXT
    my_resolver = dns.resolver.Resolver()
    try:
        answers = my_resolver.query(domain_name, "TXT")
        for rdata in answers:
            defaults = {'domain': domain, 'company': company}
            dns_record = Dns.objects.filter(
                type='TXT', value=rdata.strings, domain=domain_id)
            if dns_record.exists():
                dns_record.update(**defaults)
                print(
                    f"TXT record {rdata.strings} already exists for: {domain_name}")
            else:
                Dns.objects.create(type='TXT', value=rdata.strings, **defaults)
                print(f"TXT record {rdata.strings} created for: {domain_name}")
    except dns.resolver.NXDOMAIN:
        print(f"Error: {domain_name} does not exist")
    except dns.resolver.NoAnswer:
        print(f"Error: No TXT record found for {domain_name}")
# NS
    my_resolver = dns.resolver.Resolver()
    try:
        answers = my_resolver.query(domain_name, "NS")
        for rdata in answers:
            defaults = {'domain': domain, 'company': company}
            dns_record = Dns.objects.filter(
                type='NS', value=rdata.target, domain=domain_id)
            if dns_record.exists():
                dns_record.update(**defaults)
                print(
                    f"NS record {rdata.target} already exists for: {domain_name}")
            else:
                Dns.objects.create(type='NS', value=rdata.target, **defaults)
                print(f"NS record {rdata.target} created for: {domain_name}")
    except dns.resolver.NXDOMAIN:
        print(f"Error: {domain_name} does not exist")
    except dns.resolver.NoAnswer:
        print(f"Error: No NS record found for {domain_name}")

from rest_framework.response import Response
from rest_framework import status

from authentication.models import User
from company.models import Group, Domain, Dns, Whois, Geoip, SslLookup, CmsLookup, Log
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets

from authentication.renderers import UserRenderer
from company.serializers import CompanyClientSerializer, CompanyTeamSerializer, CompanyDomainSerializer, CompanyGroupSerializer, CompanyDNSSerializer, CompanyWhoisSerializer, CompanyGeoIpSerializer, CompanySSLSerializer, LogSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.parsers import MultiPartParser, FormParser
from company.dns_records import lookup_dns_records


from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import uuid
import dns.resolver
import requests
import json
import time
import subprocess
from django.views.decorators.debug import sensitive_variables

from company.whois_records import save_whois_data
from company.geoip_records import save_geoip_data


class CompanyClientView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        clients = User.objects.filter(
            role="Client", company=request.user.company)
        serializer = CompanyClientSerializer(clients, many=True)
        return Response({"status": 200, "clients": serializer.data}, status=status.HTTP_200_OK)




        client = User.objects.filter(id=id)

        if not client.exists():
            return Response({"status": 500, "message": "Client not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # print(client)
        serializer = CompanyClientSerializer(client, many=True)
        return Response({"status": 200, "client": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        data = request.data
        data._mutable = True
        data['company'] = request.user.company
        data['company_name'] = request.user.company_name

        serializer = CompanyClientSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": 201, "message": "Client Create Successfully..."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):

        data = request.data

        client = User.objects.filter(id=data.get('id'))

        if not client.exists():
            return Response({"status": 500, "message": "Client not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = CompanyClientSerializer(
            client[0], data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": 200, "message": "Client Update Successfully..."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        client = User.objects.filter(id=id)

        if not client.exists():
            return Response({"status": 500, "message": "Client not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        client[0].delete()
        return Response({"status": 200, "message": "Client Delete Successfully..."}, status=status.HTTP_200_OK)


class CompanyUserView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = User.objects.filter(id=id)
        if not user.exists():
            return Response({"status": 500, "message": "User not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = CompanyClientSerializer(user, many=True)
        return Response({"status": 200, "user": serializer.data[0]}, status=status.HTTP_200_OK)


class CompanyTeamView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        teams = User.objects.filter(role="Team", company=request.user.company)
        serializer = CompanyTeamSerializer(teams, many=True)
        return Response({"status": 200, "teams": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        data = request.data
        data._mutable = True
        data['company'] = request.user.company

        serializer = CompanyTeamSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": 201, "message": "Team Create Successfully..."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):

        data = request.data

        team = User.objects.filter(id=data.get('id'))

        if not team.exists():
            return Response({"status": 500, "message": "Team not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = CompanyTeamSerializer(team[0], data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": 200, "message": "Team Update Successfully..."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        team = User.objects.filter(id=id)

        if not team.exists():
            return Response({"status": 500, "message": "Team not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        team[0].delete()
        return Response({"status": 200, "message": "Team Delete Successfully..."}, status=status.HTTP_200_OK)


class CompanyGroupView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        groups = Group.objects.filter(company=request.user.company)
        serializer = CompanyGroupSerializer(groups, many=True)
        return Response({"status": 200, "groups": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        data = request.data
        data._mutable = True
        data['company'] = request.user.company

        serializer = CompanyGroupSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": 201, "message": "Group Create Successfully..."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):

        data = request.data

        group = Group.objects.filter(id=id)

        if not group.exists():
            return Response({"status": 500, "message": "Group not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = CompanyGroupSerializer(group[0], data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": 200, "message": "Group Update Successfully..."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        group = Group.objects.filter(id=id)
        if not group.exists():
            return Response({"status": 500, "message": "Group not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = CompanyGroupSerializer(group, many=True)
        return Response({"status": 200, "group": serializer.data}, status=status.HTTP_200_OK)
        
    def delete(self, request, id):

        group = Group.objects.filter(id=id)

        if not group.exists():
            return Response({"status": 500, "message": "Group not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        group[0].delete()
        return Response({"status": 200, "message": "Group Delete Successfully..."}, status=status.HTTP_200_OK)


class LogView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logs = Log.objects.filter(user=request.user.id)
        serializer = LogSerializer(logs, many=True)
        return Response({"status": 200, "logs": serializer.data}, status=status.HTTP_200_OK)



    def post(self, request, format=None):

        data = request.data
        data._mutable = True
        user = User.objects.filter(id=request.user.id)
        data['user'] = request.user.id

        serializer = LogSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": 201, "message": "Log Create Successfully..."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        
    def delete(self, request, id):

        group = Group.objects.filter(id=id)

        if not group.exists():
            return Response({"status": 500, "message": "Group not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        group[0].delete()
        return Response({"status": 200, "message": "Group Delete Successfully..."}, status=status.HTTP_200_OK)


class CompanyDomainView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        domains = Domain.objects.filter(company=request.user.company)
        serializer = CompanyDomainSerializer(domains, many=True)
        return Response({"status": 200, "domains": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        
        data = request.data
        data._mutable = True
        data['company'] = request.user.company

        serializer = CompanyDomainSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": 201, "message": "Domain Create Successfully..."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors.message, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):

        data = request.data

        domain = Domain.objects.filter(id=data.get('id'))

        if not domain.exists():
            return Response({"status": 500, "message": "Domain not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = CompanyDomainSerializer(
            domain[0], data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": 200, "message": "Domain Update Successfully..."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        domain = Domain.objects.filter(id=id)

        if not domain.exists():
            return Response({"status": 500, "message": "Domain not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        domain[0].delete()
        return Response({"status": 200, "message": "Domain Delete Successfully..."}, status=status.HTTP_200_OK)




class CompanyDNSView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        dns = Dns.objects.filter(company=request.user.company)
        serializer = CompanyDNSSerializer(dns, many=True)
        return Response({"status": 200, "dns": serializer.data}, status=status.HTTP_200_OK)

    @sensitive_variables()
    # Single Domain LookUp
    def post(self, request):
        domain = request.data['domain']
        # print(domain)
        records = lookup_dns_records(request.user.company, domain)
        return Response({"status": 200}, status=status.HTTP_200_OK)

    # All Domain LookUp
    @sensitive_variables()
    def put(self, request):
        domains = Domain.objects.filter(company=request.user.company)
        for domain in domains:
            records = lookup_dns_records(request.user, domain.id)
        return Response({"status": 200}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        dns = Dns.objects.filter(id=id)
        if not dns.exists():
            return Response({"status": 500, "message": "Dns not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        dns[0].delete()
        return Response({"status": 200, "message": "Dns Delete Successfully..."}, status=status.HTTP_200_OK)




class CompanyWhoisView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        whoisData = Whois.objects.filter(company=request.user.company)
        serializer = CompanyWhoisSerializer(whoisData, many=True)
        # print(serializer.data)
        return Response({"status": 200, "whoisDatas": serializer.data}, status=status.HTTP_200_OK)
    
 

    # Single LookUp
    def post(self, request):
        
        domain_id = request.data['domain']
        domain = Domain.objects.get(id=domain_id)
        # print(domain_id)
        # print(domain)
        domain_name = domain.domain_name
        client = User.objects.get(id=domain.client_id)
        try:
            headers = {'X-API-Key': 'SyUCnSX24sBjdMYrPxKm6Hcy'}
            url = f"https://api.int.cyberconsole.co.uk:8443/api.php?mode=whois&domain={domain_name}"
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)
            whois_data = data["whoisdata"]
            # print(whois_data)
            whois = save_whois_data(whois_data, domain, request.user, client)
            return Response({"status": 200, 'message': 'Single Domain Lookup Successfully...'}, status=status.HTTP_200_OK)
        except requests.exceptions.Timeout:
            return Response({"status": 200, 'message': 'The request timed out...'}, status=status.HTTP_200_OK)
    
    # All LookUp
    def patch(self, request):
        
        domains = Domain.objects.filter(company=request.user.company)
        
        for domain in domains:
            domain_name = domain.domain_name
            client = domain.client_id
            # print(domain_name)
            try:
                headers = {'X-API-Key': 'SyUCnSX24sBjdMYrPxKm6Hcy'}
                url = f"https://api.int.cyberconsole.co.uk:8443/api.php?mode=whois&domain={domain_name}"
                response = requests.get(url, headers=headers)
                data = json.loads(response.text)
                whois_data = data["whoisdata"]
                whois = save_whois_data(whois_data, domain, request.user, client)
                time.sleep(0.5)
            except requests.exceptions.Timeout:
                return Response({"status": 200, 'message': 'The request timed out...'}, status=status.HTTP_200_OK)
        return Response({"status": 200, 'message': 'All Lookup Successfully...'}, status=status.HTTP_200_OK)

    

    def delete(self, request, id):
        whois = Whois.objects.filter(id=id)
        if not whois.exists():
            return Response({"status": 500, "message": "Whois not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        whois[0].delete()
        return Response({"status": 200, "message": "Whois Delete Successfully..."}, status=status.HTTP_200_OK)


class CompanyGeoIpView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        geoip = Geoip.objects.filter(company=request.user.company)
        serializer = CompanyGeoIpSerializer(geoip, many=True)
        # print(serializer.data)
        return Response({"status": 200, "geoips": serializer.data}, status=status.HTTP_200_OK)
    
    # Single LookUp
    def post(self, request):
        domain = request.data['domain']
        domain = Domain.objects.get(id=domain)
        domain_name = domain.domain_name
        # domain = domain.id
        dns_records = Dns.objects.filter(
            type__in=['A', 'MX', 'NS'], domain=domain)
        for record in dns_records:
            url = f" http://ip-api.com/json/{record.value}"
            response = requests.get(url)
            geoip_data = response.json()
            geoip = save_geoip_data(geoip_data, domain, record.type, record.id, request.user)
        return Response({"status": 200, "message": "Single Domain GeoIp LookUp Successfully..."}, status=status.HTTP_200_OK)
    # All LookUp
    
    
    def patch(self, request):
        
        domains = Domain.objects.filter(company=request.user.company)

        for domain in domains:
            try:
                domain_name = domain.domain_name
                domain = domain.id
                dns_records = Dns.objects.filter(
                    type__in=['A', 'MX', 'NS'], domain=domain)
                for record in dns_records:
                    url = f" http://ip-api.com/json/{record.value}"
                    response = requests.get(url)
                    geoip_data = response.json()
                    geoip = save_geoip_data(geoip_data, domain, record.type, record.id, request.user)
            except requests.exceptions.Timeout:
                return Response({"status": 200, 'message': 'The request timed out...'}, status=status.HTTP_200_OK)
        return Response({"status": 200, "message": "All GeoIp LookUp Successfully..."}, status=status.HTTP_200_OK)
        
   

    

    def delete(self, request, id):
        geo = Geoip.objects.filter(id=id)
        if not geo.exists():
            return Response({"status": 500, "message": "Geoip not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        geo[0].delete()
        return Response({"status": 200, "message": "Geoip Delete Successfully..."}, status=status.HTTP_200_OK)


class CompanySSLView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ssl = SslLookup.objects.filter(company=request.user.company)
        serializer = CompanySSLSerializer(ssl, many=True)
        return Response({"status": 200, "ssls": serializer.data}, status=status.HTTP_200_OK)

    # Single LookUp
    def post(self, request):
        domain = request.data['domain']
        domain = Domain.objects.get(id=domain)
        domain_name = domain.domain_name
        # Run the command and capture the output
        result = run(["/var/www/html/ssl-checker/ssl_checker.py", "-H",domain_name, "-j"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        json_data = json.loads(result.stdout)

        # Extract the data for the specified domain
        domain_data = json_data.get(domain_name)

        # Check if an SslLookup instance with the specified domain already exists
        ssl_lookup, created = SslLookup.objects.update_or_create(
            company=request.user,
            domain=domain,
            defaults={
                'host': domain_data.get('host'),
                'issued_to': domain_data.get('issued_to'),
                'issued_o': domain_data.get('issued_o'),
                'issuer_c': domain_data.get('issuer_c'),
                'issuer_o': domain_data.get('issuer_o'),
                'issuer_ou': domain_data.get('issuer_ou'),
                'issuer_cn': domain_data.get('issuer_cn'),
                'cert_sn': domain_data.get('cert_sn'),
                'cert_sha1': domain_data.get('cert_sha1'),
                'cert_alg': domain_data.get('cert_alg'),
                'cert_ver': domain_data.get('cert_ver'),
                'cert_sans': domain_data.get('cert_sans'),
                'cert_exp': domain_data.get('cert_exp'),
                'cert_valid': domain_data.get('cert_valid'),
                'valid_from': domain_data.get('valid_from'),
                'valid_till': domain_data.get('valid_till'),
                'validity_days': domain_data.get('validity_days'),
                'days_left': domain_data.get('days_left'),
                'valid_days_to_expire': domain_data.get('valid_days_to_expire'),
                'tcp_port': domain_data.get('tcp_port'),
            }
        )
        ssl_lookup.save()
        serializer = CompanySSLSerializer(ssl_lookup)
        return Response({"status": 201, "message": "GEOIP success SINGLE"}, status=status.HTTP_200_OK)
    # All LookUp

    def patch(self, request):

        domains = Domain.objects.filter(company=request.user.company)

        for domain in domains:
            try:
                domain_name = domain.domain_name
                domain = domain.id
                dns_records = Dns.objects.filter(
                    type__in=['A', 'MX', 'NS'], domain=domain)
                for record in dns_records:
                    url = f" http://ip-api.com/json/{record.value}"
                    response = requests.get(url)
                    geoip_data = response.json()
                    geoip = save_geoip_data(
                        geoip_data, domain, record.type, record.id, request.user)
            except requests.exceptions.Timeout:
                return Response({"status": 200, 'message': 'The request timed out...'}, status=status.HTTP_200_OK)
        return Response({"status": 200, "message": "GEOIP success ALL"}, status=status.HTTP_200_OK)

    def delete(self, request):
        data = request.data
        geo = Geoip.objects.filter(id=data.get('id'))
        # print(data.get('id'))
        if not geo.exists():
            return Response({"status": 500, "message": "Geoip not found with this id..."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        geo[0].delete()
        return Response({"status": 200, "message": "Geoip Delete Successfully..."}, status=status.HTTP_200_OK)

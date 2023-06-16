from django.urls import path
from .views import CompanyClientView, CompanyTeamView, CompanyGroupView, CompanyDomainView, CompanyDNSView, CompanyWhoisView, CompanyGeoIpView, CompanySSLView, CompanyUserView


urlpatterns = [
    path("clients/", CompanyClientView.as_view(), name="clients"),
    path("client/store/", CompanyClientView.as_view(), name="client_store"),
    path("client/update/", CompanyClientView.as_view(), name="client_update"),
    path("client/single/<id>/", CompanyClientView.as_view(), name="client_view"),
    path("client/delete/<id>/", CompanyClientView.as_view(), name="client_delete"),
    
    path("user/<id>/", CompanyUserView.as_view(), name="user"),


    path("teams/", CompanyTeamView.as_view(), name="teams"),
    path("team/store/", CompanyTeamView.as_view(), name="team_store"),
    path("team/update/", CompanyTeamView.as_view(), name="team_update"),
    path("team/delete/<id>/", CompanyTeamView.as_view(), name="team_delete"),


    path("groups/", CompanyGroupView.as_view(), name="groups"),
    path("group/single/<id>/", CompanyGroupView.as_view(), name="group_single"),
    path("group/store/", CompanyGroupView.as_view(), name="group_store"),
    path("group/update/<id>/", CompanyGroupView.as_view(), name="group_update"),
    path("group/delete/<id>/", CompanyGroupView.as_view(), name="group_delete"),


    

    path("domains/", CompanyDomainView.as_view(), name="domains"),
    path("domain/store/", CompanyDomainView.as_view(), name="domain_store"),
    path("domain/update/", CompanyDomainView.as_view(), name="domain_update"),
    path("domain/delete/<id>/", CompanyDomainView.as_view(), name="domain_delete"),


    path("domain/dns/", CompanyDNSView.as_view(), name="domains_dns"),
    # Signle Domain LookUp
    path("domain/dns/lookup/", CompanyDNSView.as_view(), name="domain_dns_lookup"),
    # All Domains LookUp
    path("domain/dns/all/lookup/", CompanyDNSView.as_view(),name="domain_dns_lookup_all"),
    path("domain/dns/delete/<id>/", CompanyDNSView.as_view(), name="domain_dns_delete"),



    path("whois/data/all/", CompanyWhoisView.as_view(), name="whois_lookup"),
    path("whois/lookup/single/", CompanyWhoisView.as_view(), name="whois_lookup_single"),
    path("whois/lookup/all/", CompanyWhoisView.as_view(), name="whois_lookup_all"),
    path("whois/lookup/delete/<id>/", CompanyWhoisView.as_view(), name="whois_lookup_delete"),
    
    path("geoip/data/all/", CompanyGeoIpView.as_view(), name="geoip_lookup"),
    path("geoip/lookup/single/", CompanyGeoIpView.as_view(),name="geoip_lookup_single"),
    path("geoip/lookup/all/", CompanyGeoIpView.as_view(), name="geoip_lookup_all"),
    path("geoip/lookup/delete/<id>/", CompanyGeoIpView.as_view(),name="geoip_lookup_delete"),
    
    path("ssl/data/all/", CompanySSLView.as_view(), name="ssl_lookup"),
    path("ssl/lookup/single/", CompanySSLView.as_view(),name="ssl_lookup_single"),
    path("ssl/lookup/all/", CompanySSLView.as_view(), name="ssl_lookup_all"),
    path("ssl/lookup/delete/", CompanySSLView.as_view(),name="ssl_lookup_delete"),

]

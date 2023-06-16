from rest_framework.response import Response
from rest_framework import status

from company.models import Domain

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from authentication.renderers import UserRenderer
from .serializers import ClientDomainSerializer
from rest_framework.permissions import IsAuthenticated



class ClientDomainView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        domains = Domain.objects.filter(client=request.user.id)
        serializer = ClientDomainSerializer(domains, many=True)
        return Response({"status": 200, "domains": serializer.data}, status=status.HTTP_200_OK)


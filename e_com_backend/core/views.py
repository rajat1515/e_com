from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializers import VendorSerializer
from drf_spectacular.utils import extend_schema

class VendorCreation(APIView):
    @extend_schema(
        request=VendorSerializer,
        responses={
            201: {'description': 'domain name'},
            400: {'description': 'Bad request. Duplicate email or invid data'},
            500: {'description': 'Internal server error. Something went wrong'}
        },
        description="create a new VendorUser.(Admin access)")
    def post(self, request):
        try:
            serializer = VendorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                domain = serializer.validated_data['schema_name']+'.localhost:8000'
                return Response({"domain": domain},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

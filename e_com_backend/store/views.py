from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (status,
                            pagination,
                            serializers)

from store.permissions import (IsAdmin,
                               IsSalesperson,
                               IsSupervisor,
                               IsCustomer)

from store.serializers import (VendorUserSerializer,
                               StoreSerializer,
                               ProductSerializer,
                               ProductSoldSerializer,
                               CustomerRegistrationSerializer)

from store.models import VendorUser, Store, Product

from django.db.models import Q
from django.db.utils import ProgrammingError, IntegrityError
from csv import DictReader
from store.utils import CSVValidator
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserManagementView(APIView):
    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        description="Retrieve a list of users filtered by email or role.\
            (Admin Access)",
        parameters=[
            OpenApiParameter(
                name='q',
                required=False,
                description='Search keyword for filtering by email or role.',
                type=str
            ),
            OpenApiParameter(
                name='page',
                required=False,
                description='Page number for paginated results.',
                type=int
            ),
            OpenApiParameter(
                name='page_size',
                required=False,
                description='Number of items per page for pagination.',
                type=int
            )
        ]
    )
    def get(self, request):
        try:
            search_keyword = request.GET.get('q', None)

            filters = Q()

            if search_keyword:
                filters &= Q(user__email__istartswith=search_keyword)
                filters |= Q(role__istartswith=search_keyword)

            users = VendorUser.objects.filter(filters)

            paginator = CustomPagination()
            results = paginator.paginate_queryset(users, request)
            serializer = VendorUserSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)
        except ProgrammingError:
            return Response({"error": "Not Valid for public schema"},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        request=VendorUserSerializer,
        responses={
            201: VendorUserSerializer,
            400: {'description': 'Bad request. Duplicate email or invid data'},
            500: {'description': 'Internal server error. Something went wrong'}
        },
        description="create a new VendorUser.(Admin access)")
    def post(self, request):
        try:
            serializer = VendorUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except ProgrammingError:
            return Response({"error": "Not Valid for public schema"},
                            status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"error": "Duplicate email"},
                            status=status.HTTP_400_BAD_REQUEST)
        except :
            return Response({"error": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StoreManagementView(APIView):
    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        description="Retrieve a list of stores (Admin Access)",
        parameters=[
            OpenApiParameter(
                name='q',
                required=False,
                description='Search keyword for filtering by name or \
                    location or contact details.',
                type=str
            ),
            OpenApiParameter(
                name='page',
                required=False,
                description='Page number for paginated results.',
                type=int
            ),
            OpenApiParameter(
                name='page_size',
                required=False,
                description='Number of items per page for pagination.',
                type=int
            )
        ]
    )
    def get(self, request):
        try:
            search_keyword = request.GET.get('q', None)

            filters = Q()

            if search_keyword:
                filters &= Q(name__icontains=search_keyword)
                filters |= Q(location__icontains=search_keyword)
                filters |= Q(contact_details__icontains=search_keyword)

            stores = Store.objects.filter(filters)

            paginator = CustomPagination()
            results = paginator.paginate_queryset(stores, request)
            serializer = StoreSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)
        except ProgrammingError:
            return Response({"error": "Not Valid for public schema"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        request=StoreSerializer,
        responses={
            201: StoreSerializer,
            400: {'description': 'Bad request. '},
            500: {'description': 'Internal server error. Something went wrong'}
        },
        description="create a new VendorUser.(Admin access)")
    def post(self, request):
        try:
            serializer = StoreSerializer(data=request.data)
            if serializer.is_valid():
                vendor_user = VendorUser.objects.get(user=request.user)
                serializer.save(added_by=vendor_user)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except ProgrammingError:
            return Response({"error": "Not Valid for public schema"},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSupervisor]

    @extend_schema(
        request=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: {'description': 'Bad request.'},
            500: {'description': 'Internal server error. Something went wrong'}
        },
        description="create a new Product.(Supervisor access)")
    def post(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                vendor_user = VendorUser.objects.get(user=request.user)
                serializer.save(added_by=vendor_user)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except ProgrammingError:
            return Response({"error": "Not Valid for public schema"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UploadCSVView(APIView):
    """
        Uploads a CSV file containing product data and adds the products
        to the store.(Supervisor access)

        Parameters:
            - file: File CSV format

        Returns:
            HTTP 201 Created if products are added successfully.
            HTTP 400 Bad Request if there are validation errors in the CSV data.
            HTTP 400 Bad Request if the request is not valid for public schema.
            HTTP 500 Internal Server Error if something went wrong during processing.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSupervisor]

    def post(self, request):
        csv_file = request.FILES.get('file')
        if not csv_file:
            raise serializers.ValidationError("No file uploaded")

        elif csv_file.size < 1:
            raise serializers.ValidationError("Empty file")
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = DictReader(decoded_file)
            CSVValidator.validate_csv_data(csv_reader)

            csv_reader = list(csv_reader)

            if len(csv_reader) < 1:
                raise serializers.ValidationError("No rows present")

            serializer = ProductSerializer(data=csv_reader, many=True)
            if serializer.is_valid():
                vendor_user = VendorUser.objects.get(user=request.user)
                serializer.save(added_by=vendor_user)
                return Response(status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        except ProgrammingError:
            return Response({"error": "Not Valid for public schema"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductSoldView(APIView):
    permission_classes = [IsSalesperson]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        request=ProductSoldSerializer,
        responses={
            201: ProductSoldSerializer,
            400: {'description': 'Bad request.'},
            500: {'description': 'Something went wrong'}
        },
        description="Register the prduct sold.(Salesperson access)")
    def post(self, request):
        try:
            vendor_user = VendorUser.objects.get(user=request.user)
            serializer = ProductSoldSerializer(data=request.data,
                                               context={"vendor_user":
                                                        vendor_user})
            if serializer.is_valid():

                serializer.save()
                return Response(status=status.HTTP_201_CREATED)

            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        except ProgrammingError:
            return Response({"error": "Not Valid for public schema"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerRegistrationView(APIView):
    @extend_schema(
        request=CustomerRegistrationSerializer,
        responses={
            201: {'description': 'message'},
            400: {'description': 'Bad request.'},
            500: {'description': 'Something went wrong'}
        },
        description="Register the customer")
    def post(self, request):
        try:
            serializer = CustomerRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Customer registered successfully."},
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        except ProgrammingError:
            return Response({"error": "Not Valid for public schema"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductsView(APIView):
    """
    Retrieve a list Product with store (Customer Access)

    Parameters:
        product_name: list search product in all stores (one product,  All Stores)
        Store_name: list all product in store
        (if both not present , will list All products, all stores)

    """
    permission_classes = [IsCustomer]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='product_name',
                required=False,
                description='Search keyword for product_name.',
                type=str
            ),
            OpenApiParameter(
                name='store_name',
                required=False,
                description='Search keyword for store name.',
                type=str
            ),
            OpenApiParameter(
                name='page',
                required=False,
                description='Page number for paginated results.',
                type=int
            ),
            OpenApiParameter(
                name='page_size',
                required=False,
                description='Number of items per page for pagination.',
                type=int
            )
        ]
    )
    def get(self, request):
        try:
            product_name = request.query_params.get('product_name')
            store_name = request.query_params.get('store_name')

            if product_name:
                # one product,  All store
                products = Product.objects.filter(name=product_name)

            elif store_name:
                # All products, one store
                products = Product.objects.filter(store__name=store_name)

            else:
                # All products, all stores
                products = Product.objects.all()

            paginator = CustomPagination()
            results = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(results, many=True)

            return paginator.get_paginated_response(serializer.data)
        except ProgrammingError:
            return Response({"error": "Not Valid for public schema"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

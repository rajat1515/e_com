# from django.http import JsonResponse
# from datetime import datetime
# import jwt
# from rest_framework import status
# from core.models import User


# class AuthMiddleWare:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if not (request.path.startswith('/admin/')
#                 or request.path.startswith('/api/')
#                 or (request.path.startswith('/vendor/customer/')
#                     and request.method == "POST")):
#             try:
#                 authorization_header = request.headers.get('Authorization', '')
#                 if not authorization_header:
#                     return JsonResponse({'error': 'Authentication credentials are not provided .'},
#                                         status=status.HTTP_401_UNAUTHORIZED)
#                 jwt_token = jwt.decode(authorization_header, options={"verify_signature": False}, verify=False)

#             except:
#                 return JsonResponse({'error': 'Authentication credentials are invalid.'},
#                                     status=status.HTTP_401_UNAUTHORIZED)

#             # if datetime.fromtimestamp(jwt_token['exp']) < datetime.now():
#             #     return JsonResponse({'error': 'Auth token Expired'})

#             request.core_user = User.objects.get(id=jwt_token['user_id'])

#         response = self.get_response(request)
#         return response

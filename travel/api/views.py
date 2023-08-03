from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .utils import PerevalRepositoryDjango


class ArtsApiView(APIView):
    def post(self, request):
        repository = PerevalRepositoryDjango()
        try:
            pereval_id = repository.add_pereval(request.data)
            return Response({'status': status.HTTP_201_CREATED, 'message': 'success', 'id': pereval_id})
        except KeyError as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f'Key error, enter {e}'})
        except Exception as e:
            return Response({'status': status.HTTP_502_BAD_GATEWAY, 'message': str(e)})

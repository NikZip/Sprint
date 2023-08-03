from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .utils import PerevalRepositoryDjango


class ArtsApiView(APIView):
    def post(self, request):
        repository = PerevalRepositoryDjango()
        pereval_id = repository.add_pereval(request.data)
        return Response({'status': status.HTTP_200_OK, 'message': 'success', 'id': pereval_id},
                        status=status.HTTP_201_CREATED)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status
from .utils import PerevalRepositoryDjango
from .exceptions import StatusIsNotNewException
from .serializers import *
from ..models import *


class PassApiView(APIView):
    def post(self, request):
        repository = PerevalRepositoryDjango()
        try:
            pereval_id = repository.add_pereval(request.data)
            return Response({'status': status.HTTP_200_OK, 'message': 'success', 'id': pereval_id})
        except KeyError as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f'Key error, enter {e}'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': status.HTTP_502_BAD_GATEWAY, 'message': str(e)},
                            status=status.HTTP_502_BAD_GATEWAY)


class PassListQueryView(APIView):
    def get(self, request):
        email = request.GET.get('user__email')
        try:
            user = PerevalUser.objects.get(email=email)
            submit_data = PerevalAddModel.objects.filter(created_by=user)
            serializer = PerevalAddSerializer(submit_data, many=True)
            return Response(serializer.data)
        except PerevalUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class PassDetailApiView(RetrieveUpdateAPIView):
    queryset = PerevalAddModel.objects.all()
    serializer_class = PerevalAddSerializer

    @staticmethod
    def _nested_serializer_partial_update(model_name, request_data, model_serializer, instance):
        if model_name in request_data:
            data = request_data[model_name]
            serializer = model_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                serializer.save()

    @staticmethod
    def _nested_serializer_partial_update_many(many_name, request_data, model, model_serializer):
        if many_name in request_data:
            data = request_data[many_name]
            for item in data:
                item_instance = model.objects.get(pk=item['id'])
                serializer = model_serializer(item_instance, data=item, partial=True)
                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    serializer.save()

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()

            if instance.status != "new":
                raise StatusIsNotNewException(instance.status)

            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)

            self._nested_serializer_partial_update('coords', request.data, CoordsSerializer, instance.coords)
            self._nested_serializer_partial_update('level', request.data, LevelSerializer, instance.level)
            self._nested_serializer_partial_update_many('images', request.data, PerevalImageModel, PerevalImagesSerializer)

            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response({"state": 1, "message": "success"})
        except Exception as e:
            return Response({"state": 0, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)




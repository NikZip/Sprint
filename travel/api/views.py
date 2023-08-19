from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .exceptions import StatusIsNotNewException
from .serializers import *
from ..models import *


class PassCreateApiView(CreateAPIView):
    """
    Post pass data to create a new pass in db
    return: status, message and id of created object
    """
    serializer_class = PerevalJsonPostSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Success', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'status': openapi.Schema(type=openapi.TYPE_STRING),
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER)
                            })),
            'Fail': openapi.Response('Error', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'message': openapi.Schema(type=openapi.TYPE_STRING)
                            })),
        })
    def post(self, request, **kwargs):
        repository = PerevalRepositoryDjango()
        try:
            pereval = repository.add_pereval(request.data)
            return Response({'status': status.HTTP_200_OK, 'message': 'success', 'id': pereval.id})
        except KeyError as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f'Key error, enter {e}'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': status.HTTP_502_BAD_GATEWAY, 'message': str(e)},
                            status=status.HTTP_502_BAD_GATEWAY)


class PassListQueryView(APIView):
    """
    Returns a list of passes that was created by user with entered email address
    return: List['PerevalAddModel']
    """
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('user__email', openapi.IN_QUERY, description='Filter by email', type=openapi.TYPE_STRING),
    ],
        responses={
            200: openapi.Response(description='Success', schema=openapi.Schema(
                type=openapi.TYPE_ARRAY, items=openapi.Schema(
                    type='List[Passes]'))),
            404: openapi.Response(description='User not found'),
        },
    )
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
    """
    GET: Returns detailed information about pass
    PATCH: Partial update for pass and it's dependencies
    return: state with message
    """
    allowed_methods = ['GET', 'PATCH']
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
            self._nested_serializer_partial_update_many('images', request.data, PerevalImageModel,
                                                        PerevalImagesSerializer)

            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response({"state": 1, "message": "success"})
        except KeyError as e:
            return Response({"state": 0, 'message': f'Key error, enter {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"state": 0, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)




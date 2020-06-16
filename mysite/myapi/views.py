from rest_framework.decorators import action
from rest_framework import viewsets
from .serializers import PersonSerializer, AdminSerializer
from .models import Person
from .models import Admin
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import renderers


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer


# @api_view(['GET', 'POST'])
# def person_list(request):
#     if request.method == 'GET':
#         people = Person.objects.all()
#         serializer = PersonSerializer(people, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PersonSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def person_detail(request, pk):
#     try:
#         person = Person.objects.get(pk=pk)
#     except Person.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = PersonSerializer(person)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = PersonSerializer(person, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         person.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class PersonList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Person.objects.all()
#     serializer_class = PersonSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         serializer.save()
#         # owner=self.request.user


# class PersonDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
#                    generics.GenericAPIView):
#
#     queryset = Person.objects.all()
#     serializer_class = PersonSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly]
#
#     def get(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class PersonViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.
#
#     Additionally we also provide an extra `highlight` action.
#     """
#     queryset = Person.objects.all()
#     serializer_class = PersonSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly]
#
#     @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
#     def highlight(self, request, *args, **kwargs):
#         person = self.get_object()
#         return Response(person.highlighted)
#
#     def perform_create(self, serializer):
#         serializer.save()
#         # owner=self.request.user
#
#
# class AdminViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Admin.objects.all()
#     serializer_class = AdminSerializer
#

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'admin': reverse('admin-list', request=request, format=format),
        'people': reverse('person-list', request=request, format=format)
    })


# class PersonHighlight(generics.GenericAPIView):
#     queryset = Person.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]
#
#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)









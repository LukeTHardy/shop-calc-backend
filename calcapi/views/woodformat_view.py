from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from calcapi.models import WoodFormat


class WoodFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = WoodFormat
        fields = '__all__'


class WoodFormatViewSet(ViewSet):

    def list(self, request):
        woodformats = WoodFormat.objects.all()
        serializer = WoodFormatSerializer(woodformats, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            woodformat = WoodFormat.objects.get(pk=pk)
            serializer = WoodFormatSerializer(woodformat)
            return Response(serializer.data)
        except WoodFormat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            name = request.data.get('name')
            woodformat = WoodFormat.objects.create(name=name)
            serializer = WoodFormatSerializer(woodformat, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            woodformat = WoodFormat.objects.get(pk=pk)
            self.check_object_permissions(request, woodformat)
            woodformat.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except WoodFormat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            woodformat = WoodFormat.objects.get(pk=pk)
            serializer = WoodFormatSerializer(data=request.data)
            if serializer.is_valid():
                woodformat.name = serializer.validated_data['name']
                woodformat.save()
                
                serializer = WoodFormatSerializer(woodformat, context={'request': request})
                return Response(None, status.HTTP_200_OK)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except WoodFormat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
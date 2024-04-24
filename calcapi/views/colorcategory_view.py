from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from calcapi.models import ColorCategory


class ColorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorCategory
        fields = '__all__'


class ColorCategoryViewSet(ViewSet):

    def list(self, request):
        colorcategories = ColorCategory.objects.all()
        serializer = ColorCategorySerializer(colorcategories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            colorcategory = ColorCategory.objects.get(pk=pk)
            serializer = ColorCategorySerializer(colorcategory)
            return Response(serializer.data)
        except ColorCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            name = request.data.get('name')
            colorcategory = ColorCategory.objects.create(name=name)
            serializer = ColorCategorySerializer(colorcategory, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            colorcategory = ColorCategory.objects.get(pk=pk)
            self.check_object_permissions(request, colorcategory)
            colorcategory.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except ColorCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            colorcategory = ColorCategory.objects.get(pk=pk)
            serializer = ColorCategorySerializer(data=request.data)
            if serializer.is_valid():
                colorcategory.name = serializer.validated_data['name']
                colorcategory.save()
                
                serializer = ColorCategorySerializer(colorcategory, context={'request': request})
                return Response(None, status.HTTP_200_OK)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except ColorCategory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
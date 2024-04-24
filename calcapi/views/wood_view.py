from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from calcapi.models import Wood, ColorCategory
from calcapi.views.colorcategory_view import ColorCategorySerializer
import base64
from django.core.files.base import ContentFile
from urllib.parse import urljoin

        
class WoodSerializer(serializers.ModelSerializer):
    colorCat = ColorCategorySerializer(many=False)
   
    class Meta:
        model = Wood
        fields = '__all__'
    
    
    def add_base_url(self, image_path):
        # Add the base URL to the image path
        request = self.context.get('request', None)
        if request is not None:
            base_url = request.build_absolute_uri('/')
            return urljoin(base_url, image_path)

        return image_path


class WoodViewSet(ViewSet):

    def retrieve(self, request, pk):
        try:
            wood = Wood.objects.get(pk=pk)
            serializer = WoodSerializer(wood, context={"request": request})
            return Response(serializer.data)
        except Wood.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        woods = Wood.objects.all()
        serializer = WoodSerializer(woods, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        try:
            image_data = request.data.get('image', None)

            image_format, image_str = request.data["image"].split(';base64,')
            image_ext = image_format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(image_str), name=f'{request.data["name"]}.{image_ext}')

            wood = Wood()
            wood.species = request.data.get('species')
            wood.domestic = request.data.get('domestic')
            wood.hardwood = request.data.get('hardwood')
            wood.density = request.data.get('density')
            wood.origin = request.data.get('origin')
            wood.appearance = request.data.get('appearance')
            wood.characteristics = request.data.get('characteristics')
            wood.colorCat = ColorCategory.objects.get(pk=request.data["colorCat"])
            wood.image = image_data

            wood.save()

            serializer = WoodSerializer(wood, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            wood = Wood.objects.get(pk=pk)
            
            # Check if new image data is provided (including empty string)
            new_image_data = request.data.get('image', None)
            if new_image_data is not None and ';' in new_image_data:  # Check for explicit empty string
                # Update the image
                image_format, image_str = new_image_data.split(';base64,')
                image_ext = image_format.split('/')[-1]
                image_data = ContentFile(base64.b64decode(image_str), name=f'{request.data["name"]}.{image_ext}')
                wood.image = image_data

            # Update wood fields
            wood.species = request.data.get('species', wood.species)
            wood.domestic = request.data.get('domestic', wood.domestic)
            wood.hardwood = request.data.get('hardwood', wood.hardwood)
            wood.density = request.data.get('density', wood.density)
            wood.origin = request.data.get('origin', wood.origin)
            wood.appearance = request.data.get('appearance', wood.appearance)
            wood.characteristics = request.data.get('characteristics', wood.characteristics)
            wood.colorCat = ColorCategory.objects.get(pk=request.data.get("colorCat", wood.colorCat.pk))

            wood.save()

            serializer = WoodSerializer(wood, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Wood.DoesNotExist:
            return Response({'error': 'Wood not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            wood = Wood.objects.get(pk=pk)
            wood.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Wood.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
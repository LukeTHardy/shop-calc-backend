from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from calcapi.models import Inventory, Wood, WoodFormat
from calcapi.views.woodformat_view import WoodFormatSerializer
from calcapi.views.wood_view import WoodSerializer

        
class InventorySerializer(serializers.ModelSerializer):
    species = WoodSerializer(many=False)
    format = WoodFormatSerializer(many=False)
   
    class Meta:
        model = Inventory
        fields = '__all__'
    


class InventoryViewSet(ViewSet):

    def retrieve(self, request, pk):
        try:
            inventory = Inventory.objects.get(pk=pk)
            serializer = InventorySerializer(inventory, context={"request": request})
            return Response(serializer.data)
        except Inventory.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        user_id = request.user.id
        inventory = Inventory.objects.filter(user__id=user_id)
        serializer = InventorySerializer(inventory, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        try:


            inventory = Inventory()
            inventory.user = User.objects.get(pk=request.user.id)
            inventory.species = Wood.objects.get(pk=request.data["species"])
            inventory.format = WoodFormat.objects.get(pk=request.data["format"])
            inventory.quantity = float(request.data.get('quantity'))
            inventory.length = float(request.data.get('length'))  # Convert to float
            inventory.width = float(request.data.get('width'))  # Convert to float
            inventory.thickness = float(request.data.get('thickness'))  # Convert to float
            inventory.notes = request.data.get('notes')


            # Perform the calculation
            boardfeet = float((inventory.length * inventory.width * inventory.thickness * inventory.quantity) / 144)

            inventory.totalBF = round(boardfeet, 2)

            inventory.save()

            serializer = InventorySerializer(inventory, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            inventory = Inventory.objects.get(pk=pk)
            
            inventory = Inventory()
            inventory.user = User.objects.get(pk=request.user.id)
            inventory.species = Wood.objects.get(pk=request.data.get("species", inventory.species.pk))
            inventory.format = WoodFormat.objects.get(pk=request.data.get("format", inventory.format.pk))
            inventory.quantity = request.data.get('quantity', inventory.quantity)
            inventory.length = float(request.data.get('length'), inventory.length) 
            inventory.width = float(request.data.get('width'), inventory.width) 
            inventory.thickness = float(request.data.get('thickness'), inventory.thickness)
            inventory.notes = request.data.get('notes', inventory.notes)
            


            # Perform the calculation
            boardfeet = (inventory.length * inventory.width * inventory.thickness) / 144

            inventory.totalBF = boardfeet

            inventory.save()
            serializer = InventorySerializer(inventory, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Inventory.DoesNotExist:
            return Response({'error': 'Inventory not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            inventory = Inventory.objects.get(pk=pk)
            inventory.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Inventory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
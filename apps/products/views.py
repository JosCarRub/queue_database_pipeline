
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.products.domain.exceptions import PublisherError
from apps.products.presentation.inyector import Inyector
from apps.products.presentation.serializers import CreateProductSerializer

import uuid 
from apps.products.domain.exceptions import ProductNotFoundError
from apps.products.infrastructure.mappers import ProductMapper


class ProductListView(APIView):
    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        try:
            request_creation_uc = Inyector.request_product_creation_uc()

            request_creation_uc.execute(
                name=validated_data['name'],
                description=validated_data['description'],
                price=validated_data['price']
            )

            return Response(
                {"message": "La petición de creación del producto ha sido aceptada y está siendo procesada."},
                status=status.HTTP_202_ACCEPTED
            )
        
        except PublisherError as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class ProductDetailView(APIView):
    def get(self, request, product_id: str):
        try:
            product_uuid = uuid.UUID(product_id)
        except ValueError:
            return Response(
                {"error": "El ID del producto no es un UUID válido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            get_uc = Inyector.get_product_by_id_uc()            
            product_entity = get_uc.execute(product_id=product_uuid)
            
            #convertir entidad a diccionario
            response_data = ProductMapper.entity_to_dict(product_entity)

            return Response(response_data, status=status.HTTP_200_OK)

        except ProductNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from apps.products.application.use_cases.create_product import CreateProduct
from apps.products.domain.exceptions import DuplicateProductError, InvalidProductError
from apps.products.presentation.inyector import Inyector
from apps.products.presentation.serializers import CreateProductSerializer


class ProductListView(APIView):
    create_product_uc = CreateProduct

    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        try:
            create_uc = Inyector.create_product_uc()
            new_product = create_uc.execute(
                name=validated_data['name'],
                description=validated_data['description'],
                price=validated_data['price']
            )

            response_data = {
                'id': str(new_product.id),
                'name': new_product.name,
                'description': new_product.description,
                'price': str(new_product.price),
                'stock': new_product.stock
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except DuplicateProductError as e:
            return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)
        
        except InvalidProductError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
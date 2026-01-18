from decimal import Decimal
import redis
import json
import uuid
from typing import Optional
from decouple import config

from apps.products.domain.entities import Product as ProductEntity
from apps.products.domain.repositories import ProductRepository
from apps.products.infrastructure.mappers import ProductMapper


class CachedProductRepository(ProductRepository):
    """
    añade una capa de caché sobre el repositorio decorated
    """
    def __init__(self, decorated_repository: ProductRepository):
        self.decorated_repository = decorated_repository
        
        host = config('REDIS_HOST_LOCAL', default='localhost')
        if not config('RUNNING_LOCALLY', default=True, cast=bool):
            host = config('REDIS_HOST', default='cache')
            
        port = config('REDIS_PORT', default=6379, cast=int)
        
        # conexión a redis
        self.redis_client = redis.Redis(host=host, port=port, db=0, decode_responses=True)
        self.cache_ttl = 60 # Time-to-live en segundos

    def get_by_id(self, product_id: uuid.UUID) -> Optional[ProductEntity]:
        cache_key = f"product:{product_id}"
        
        # obtiene el producto de la caché si estuvra
        cached_product_json = self.redis_client.get(cache_key)
        
        if cached_product_json:
            print(f"CACHE HIT for product {product_id}")
            product_data = json.loads(cached_product_json)
            #Redis guarda strings
            # Esto podría ir en el Mapper, pero por simplicidad lo hacemos aquí.
            return ProductMapper.dict_to_entity(product_data)
            
        print(f"CACHE MISS for product {product_id}")
        # si no está en la caché, llama al repositorio original
        product = self.decorated_repository.get_by_id(product_id)
        
        if product:
            #si lo encuentra en db, lo guarda en la caché para la próxima vez
            product_data = ProductMapper.entity_to_dict(product)

            self.redis_client.setex(cache_key, self.cache_ttl, json.dumps(product_data))
            
        return product

    def save(self, product: ProductEntity) -> None:
        # Llama al repositorio original para guardar en la BD
        self.decorated_repository.save(product)
        
        # INVALICACIÓN DE CACHÉ: Si se guarda un producto ,tanto create como update,
        # se borra su entrada antigua de la caché para evitar datos obsoletos
        cache_key = f"product:{product.id}"
        if self.redis_client.exists(cache_key):
            print(f"CACHE INVALIDATION for product {product.id}")
            self.redis_client.delete(cache_key)

    def get_by_name(self, name: str) -> Optional[ProductEntity]:
        # delegamos la llamada
        return self.decorated_repository.get_by_name(name)
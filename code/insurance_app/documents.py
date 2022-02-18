from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product


@registry.register_document
class ProductDocument(Document):
    company_id = fields.ObjectField(properties={
        'name': fields.TextField(),
        'description': fields.TextField(),
    })
    category_id = fields.ObjectField(properties={
        'name': fields.TextField(),
    })

    class Django:
        model = Product
        fields = [
            'name',
            'percentage',
            'period',
        ]

    class Index:
        name = 'product'

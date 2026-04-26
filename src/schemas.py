from apiflask import Schema
from apiflask.fields import Integer, String, Float
from apiflask.validators import Length, Range


class ProductIn(Schema):
    name = String(required=True)
    description = String(validate=[Length(max=2550)])
    quantity = Integer( validate=[Range(min=0)],load_default=0)
    price = Float(required=True, validate=[Range(min=0.01)])


class ProductOut(Schema):
    id = Integer()
    name = String()
    description = String()
    quantity = Integer()
    price = Float()


class ProductFilter(Schema):
    search = String(load_default=None)
    min_price = Float(load_default=None)
    mas_price = Float(load_default=None)
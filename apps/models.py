# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Merch(db.Model):

    __tablename__ = 'Merch'

    id = db.Column(db.Integer, primary_key=True)

    #__Merch_FIELDS__
    item_id = db.Column(db.Integer, nullable=True)
    item_name = db.Column(db.String(255),  nullable=True)
    item_cost = db.Column(db.Text, nullable=True)
    item_quantity = db.Column(db.Text, nullable=True)
    item_sku = db.Column(db.String(255),  nullable=True)

    #__Merch_FIELDS__END

    def __init__(self, **kwargs):
        super(Merch, self).__init__(**kwargs)


class Category(db.Model):

    __tablename__ = 'Category'

    id = db.Column(db.Integer, primary_key=True)

    #__Category_FIELDS__
    id = db.Column(db.Integer, nullable=True)
    category_name = db.Column(db.Text, nullable=True)
    category_description = db.Column(db.String(255),  nullable=True)

    #__Category_FIELDS__END

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)


class Cart(db.Model):

    __tablename__ = 'Cart'

    id = db.Column(db.Integer, primary_key=True)

    #__Cart_FIELDS__
    id = db.Column(db.String(255),  nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Cart_FIELDS__END

    def __init__(self, **kwargs):
        super(Cart, self).__init__(**kwargs)


class Cartitem(db.Model):

    __tablename__ = 'Cartitem'

    id = db.Column(db.Integer, primary_key=True)

    #__Cartitem_FIELDS__
    id = db.Column(db.Integer, nullable=True)
    product_id = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)

    #__Cartitem_FIELDS__END

    def __init__(self, **kwargs):
        super(Cartitem, self).__init__(**kwargs)


class Order(db.Model):

    __tablename__ = 'Order'

    id = db.Column(db.Integer, primary_key=True)

    #__Order_FIELDS__
    total_amount = db.Column(db.Text, nullable=True)
    status = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Order_FIELDS__END

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)


class Orderitem(db.Model):

    __tablename__ = 'Orderitem'

    id = db.Column(db.Integer, primary_key=True)

    #__Orderitem_FIELDS__
    product_id = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    price_at_purchase = db.Column(db.Text, nullable=True)
    order_id = db.Column(db.String(255),  nullable=True)

    #__Orderitem_FIELDS__END

    def __init__(self, **kwargs):
        super(Orderitem, self).__init__(**kwargs)


class Address(db.Model):

    __tablename__ = 'Address'

    id = db.Column(db.Integer, primary_key=True)

    #__Address_FIELDS__
    city = db.Column(db.Text, nullable=True)
    state = db.Column(db.Text, nullable=True)
    zip = db.Column(db.Integer, nullable=True)
    country = db.Column(db.String(255),  nullable=True)
    street = db.Column(db.String(255),  nullable=True)

    #__Address_FIELDS__END

    def __init__(self, **kwargs):
        super(Address, self).__init__(**kwargs)


class Payment(db.Model):

    __tablename__ = 'Payment'

    id = db.Column(db.Integer, primary_key=True)

    #__Payment_FIELDS__
    payment_method = db.Column(db.Text, nullable=True)
    transaction_id = db.Column(db.Text, nullable=True)
    status = db.Column(db.Boolean, nullable=True)

    #__Payment_FIELDS__END

    def __init__(self, **kwargs):
        super(Payment, self).__init__(**kwargs)



#__MODELS__END

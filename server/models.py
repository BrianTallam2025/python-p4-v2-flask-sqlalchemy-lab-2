from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin # Ensure this is imported
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    items = association_proxy('reviews', 'item')

    # Serialization rules for Customer
    serialize_rules = ('-reviews.customer',) # Exclude review's customer to prevent recursion

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')

    # Serialization rules for Item
    serialize_rules = ('-reviews.item',) # Exclude review's item to prevent recursion

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    # Serialization rules for Review
    serialize_rules = ('-customer.reviews', '-item.reviews',) # Exclude related reviews to prevent recursion

    def __repr__(self):
        return f'<Review {self.id}, Customer: {self.customer_id}, Item: {self.item_id}>'
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import os
# import sqlite3
# from init_db import init_db

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'dev'
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     'mysql+pymysql://root:10000'
#     '@/bookstore?unix_socket=/cloudsql/genial-current-403917:Iowa:genial-current-403917:us-central1:bookstore'
# )
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column('orderid', db.Integer, primary_key=True)
    book_id = db.Column('bookid', db.String, nullable=False)
    customer_id = db.Column('customerid', db.Integer, nullable=False)


class OrderForm(FlaskForm):
    book_id = StringField('Book ID (ISBN)', validators=[DataRequired()])
    customer_id = IntegerField('Customer ID', validators=[DataRequired()])
    submit = SubmitField('Add Order')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()
    if form.validate_on_submit():
        new_order = Order(book_id=form.book_id.data, customer_id=form.customer_id.data)
        db.session.add(new_order)
        db.session.commit()
        flash('Order added successfully!', 'success')
        return redirect(url_for('index'))

    orders = Order.query.all()
    return render_template('index.html', orders=orders, form=form)


@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

from flask import Flask, redirect, render_template, request, url_for
api = Flask(__name__)

import sqlite3
con = sqlite3.connect('Garage.db', check_same_thread=False)
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS cars(Model, Color, Year)")


@api.route('/')
def hello():
    return render_template('index.html')

@api.route('/register', methods=['POST'])
# entering data from the user into the sql table and redirecting to display_cars endpoint
def print_cars():
    color = request.form['color']
    model = request.form['model']
    year = request.form['year']
    cur.execute(f"INSERT INTO cars Values('{model}', '{color}', '{year}')")
    con.commit()
    print(color, model, year)
    return redirect(url_for('display_cars'))

@api.route('/display_cars', methods=['Post', 'Get'])
# Takes all data in cars table and prints them into the block content in the cars.html page
def display_cars():
    cur.execute("SELECT ROWID, * FROM cars")
    cars = cur.fetchall()
    return render_template('cars.html', cars=cars)


@api.route('/del/<int:id>', methods=['DELETE'])
def del_cars(id):
    # Delete the car from the database here
    cur.execute(f"DELETE FROM cars WHERE ROWID = {id}")
    con.commit()
    print("Deleted car with id:", id)
    return "Car deleted successfully"





if __name__ == '__main__':
    api.run(debug=True)
#˜”*°•.˜”*°• CSEC 311 - DEFENSIVE PROGRAMMING  | FINAL PROJECT •°*”˜"
#                NANALE, KRIZIA BELLE L. | VALLE, NERISA S.  |  BSCS -3A

from flask import Flask, render_template, url_for, request, redirect, jsonify, abort, session, flash
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
from functools import wraps

# Database setup
engine = create_engine('sqlite:///restaurant.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for session management

# Utility function for handling database session errors
def handle_db_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exc.SQLAlchemyError as e:
            session.rollback()
            app.logger.error(f"Database error: {e}")
            flash("An error occurred while accessing the database. Please try again later.", "danger")
            abort(500, description="An error occurred while accessing the database.")
    return wrapper

# Login route
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Dummy authentication logic (replace with actual validation)
        if username == "admin" and password == "password123":
            session['user'] = username
            flash("Login successful!", "success")
            return redirect(url_for('showRestaurantNames'))
        else:
            flash("Invalid username or password. Please try again.", "danger")
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# Login required decorator
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function

# Route to display all restaurants
@app.route('/')
@app.route('/restaurants')
@handle_db_exceptions
@login_required
def showRestaurantNames():
    restaurants = db_session.query(Restaurant).all()
    if not restaurants:
        flash("No restaurants found.", "warning")
    return render_template("restaurants.html", restaurants=restaurants)

# Route to create a new restaurant
@app.route('/restaurants/create/', methods=['POST', 'GET'])
@handle_db_exceptions
@login_required
def createRestaurantName():
    if request.method == 'POST':
        rest_name = request.form.get('rest_name')
        if not rest_name:
            flash("Please provide a restaurant name.", "danger")
            return redirect(url_for('createRestaurantName'))
        new_rest = Restaurant(name=rest_name)
        db_session.add(new_rest)
        db_session.commit()
        flash(f"Restaurant '{rest_name}' created successfully.", "success")
        return redirect(url_for('showRestaurantNames'))
    else:
        return render_template("newrestaurants.html")

# Route to edit a restaurant's name
@app.route('/restaurants/edit/<int:restaurant_id>', methods=['POST', 'GET'])
@handle_db_exceptions
@login_required
def editRestaurantName(restaurant_id):
    restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    if not restaurant:
        flash("Restaurant not found.", "danger")
        return redirect(url_for('showRestaurantNames'))
    
    if request.method == 'POST':
        new_name = request.form.get('edit_rest_name')
        if not new_name:
            flash("Please provide a new name for the restaurant.", "danger")
            return redirect(url_for('editRestaurantName', restaurant_id=restaurant_id))
        restaurant.name = new_name
        db_session.commit()
        flash(f"Restaurant name updated to '{new_name}'.", "success")
        return redirect(url_for('showRestaurantNames'))
    else:
        return render_template("editrestaurant.html", restaurants=restaurant)

# Route to delete a restaurant
@app.route('/restaurants/delete/<int:restaurant_id>', methods=['POST', 'GET'])
@handle_db_exceptions
@login_required
def deleteRestaurantName(restaurant_id):
    restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    if not restaurant:
        flash("Restaurant not found.", "danger")
        return redirect(url_for('showRestaurantNames'))
    
    if request.method == 'POST':
        db_session.delete(restaurant)
        db_session.commit()
        flash(f"Restaurant '{restaurant.name}' has been deleted.", "danger")
        return redirect(url_for('showRestaurantNames'))
    else:
        return render_template("deleterestaurant.html", restaurant_id=restaurant_id)

# Route to display menu items of a restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/')
@handle_db_exceptions
@login_required
def showMenuItem(restaurant_id):
    restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    if not restaurant:
        flash("Restaurant not found.", "danger")
        return redirect(url_for('showRestaurantNames'))
    
    items = db_session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    if not items:
        flash("No menu items found for this restaurant.", "warning")
    return render_template("menu.html", restaurants=restaurant, items=items)

# Route to create a new menu item
@app.route('/restaurants/<int:restaurant_id>/menu/create/', methods=['POST', 'GET'])
@handle_db_exceptions
@login_required
def createMenuItem(restaurant_id):
    restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    if not restaurant:
        flash("Restaurant not found.", "danger")
        return redirect(url_for('showRestaurantNames'))
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            course = request.form['course']
            
            if not all([name, description, price, course]):
                flash("All fields are required", "danger")
                return redirect(url_for('createMenuItem', restaurant_id=restaurant_id))
            
            newItem = MenuItem(
                name=name, 
                description=description, 
                price=price, 
                course=course, 
                restaurant_id=restaurant_id
            )
            db_session.add(newItem)
            db_session.commit()
            flash(f"Menu item '{name}' added successfully.", "success")
            return redirect(url_for('showMenuItem', restaurant_id=restaurant_id))
        except KeyError:
            flash("Missing form data.", "danger")
            return redirect(url_for('createMenuItem', restaurant_id=restaurant_id))
    else:
        return render_template("newmenuitem.html", restaurant=restaurant)

# Route to edit a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/edit/<int:menu_id>/', methods=['POST', 'GET'])
@handle_db_exceptions
@login_required
def editMenuItem(restaurant_id, menu_id):
    restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    item = db_session.query(MenuItem).filter_by(id=menu_id).one_or_none()
    
    if not restaurant or not item or restaurant.id != item.restaurant_id:
        flash("Menu item or restaurant not found.", "danger")
        return redirect(url_for('showMenuItem', restaurant_id=restaurant_id))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        course = request.form.get('course')
        
        if not all([name, description, price, course]):
            flash("All fields are required", "danger")
            return redirect(url_for('editMenuItem', restaurant_id=restaurant_id, menu_id=menu_id))
        
        item.name = name
        item.description = description
        item.price = price
        item.course = course
        db_session.commit()
        flash(f"Menu item '{name}' updated successfully.", "success")
        return redirect(url_for('showMenuItem', restaurant_id=restaurant_id))
    else:
        return render_template("editmenuitem.html", restaurant=restaurant, item=item)

# Route to delete a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/delete/<int:menu_id>/', methods=['POST', 'GET'])
@handle_db_exceptions
@login_required
def deleteMenuItem(restaurant_id, menu_id):
    item = db_session.query(MenuItem).filter_by(id=menu_id).one_or_none()
    if not item:
        flash("Menu item not found.", "danger")
        return redirect(url_for('showMenuItem', restaurant_id=restaurant_id))
    
    if request.method == 'POST':
        db_session.delete(item)
        db_session.commit()
        flash(f"Menu item '{item.name}' has been deleted.", "danger")
        return redirect(url_for('showMenuItem', restaurant_id=restaurant_id))
    else:
        return render_template("deletemenuitem.html", restaurant_id=restaurant_id, menu_id=menu_id)

# JSON endpoint for menu items
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
@handle_db_exceptions
@login_required
def restaurantMenuJSON(restaurant_id):
    menu_items = db_session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    if not menu_items:
        flash("No menu items found.", "warning")
        return jsonify({"error": "No menu items found"}), 404
    return jsonify(MenuItems=[item.serialize for item in menu_items])

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
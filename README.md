# Flask Restaurant Management Application

This is a Flask-based web application for managing restaurants and their menus. Users can perform CRUD operations (Create, Read, Update, Delete) on restaurants and menu items. Authentication is implemented to secure the application.

## Features

- **Authentication:** Users must log in to access features.
- **Restaurant Management:**
  - View a list of restaurants.
  - Add, edit, and delete restaurant names.
- **Menu Management:**
  - View the menu items for a specific restaurant.
  - Add, edit, and delete menu items.
- **JSON API:**
  - Retrieve menu items for a specific restaurant in JSON format.
- **Database:** Uses SQLite for storing restaurant and menu data.

## Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- SQLite

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/flask-restaurant-app.git
   cd flask-restaurant-app
   ```

2. **Install Dependencies:**
   Use `pip` to install the required Python packages:
   ```bash
   pip install flask sqlalchemy
   ```

3. **Set Up the Database:**
   Create the database schema by running:
   ```bash
   python database_setup.py
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```
   The application will be accessible at `http://localhost:8000`.

## File Structure

```
flask-restaurant-app/
├── app.py                # Main Flask application
├── database_setup.py     # Database schema definition
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── README.md             # Application documentation
└── requirements.txt      # Python dependencies
```

## API Endpoints

- **GET /restaurants/<restaurant_id>/menu/JSON/**
  - Returns menu items for the specified restaurant in JSON format.

Example Response:
```json
{
    "MenuItems": [
        {
            "id": 1,
            "name": "Pizza",
            "description": "Cheesy goodness",
            "price": "$9.99",
            "course": "Main"
        },
        {
            "id": 2,
            "name": "Pasta",
            "description": "Classic Italian",
            "price": "$7.99",
            "course": "Main"
        }
    ]
}
```

## Templates

- `login.html`: Login page.
- `restaurants.html`: Displays all restaurants.
- `newrestaurants.html`: Form to create a new restaurant.
- `editrestaurant.html`: Form to edit a restaurant.
- `deleterestaurant.html`: Confirmation to delete a restaurant.
- `menu.html`: Displays menu items for a specific restaurant.
- `newmenuitem.html`: Form to add a menu item.
- `editmenuitem.html`: Form to edit a menu item.
- `deletemenuitem.html`: Confirmation to delete a menu item.

## Usage

1. Navigate to `http://localhost:8000` and log in.
2. Perform operations like creating, editing, or deleting restaurants and menu items.
3. Use the JSON API to integrate with other applications.

## Error Handling

- Database errors are caught and logged.
- Users are notified with flash messages for errors and successful operations.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.
from flask import Flask, jsonify, render_template, request # 'request' added here
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Define the Activity model (table structure)
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    cost = db.Column(db.String(100), nullable=True)
    source_url = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Activity {self.title}>'

    # Method to convert an Activity object to a dictionary for JSON serialization
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'location': self.location,
            'cost': self.cost,
            'source_url': self.source_url
        }

# Function to create the database tables
def create_database():
    """
    Creates the database tables if they don't already exist.
    This function should only be called once.
    """
    # Ensure the 'instance' folder exists for the database file
    instance_path = app.instance_path
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    with app.app_context():
        # Check if the database file exists within the instance folder
        db_path = os.path.join(instance_path, 'site.db')
        if not os.path.exists(db_path):
            db.create_all()
            print("Database 'site.db' created successfully.")
        else:
            print("Database 'site.db' already exists.")


# New route to serve the main HTML page
@app.route('/')
def index():
    """
    Renders the main page (index.html).
    """
    return render_template('index.html')


# API endpoint to get all activities with search and filter capabilities
@app.route('/activities', methods=['GET'])
def get_activities():
    """
    Returns activities from the database as a JSON array,
    filtered by search term and cost if provided.
    """
    query = Activity.query

    # Get search term from request arguments
    search_term = request.args.get('search')
    if search_term:
        # Filter by title or description using 'ilike' for case-insensitive search
        query = query.filter(
            (Activity.title.ilike(f'%{search_term}%')) |
            (Activity.description.ilike(f'%{search_term}%'))
        )

    # Get cost filter from request arguments
    cost_filter = request.args.get('cost')
    if cost_filter == 'free':
        # Filter for activities explicitly marked as "Free" or "Ücretsiz" (or similar)
        # We need to consider how your scraper saves 'cost' for free activities.
        # Common values could be "Free", "0", "Ücretsiz", "No Cost", etc.
        # For simplicity, we'll check for "Free" or "Ücretsiz" or similar indicators.
        query = query.filter(
            (Activity.cost.ilike('%free%')) |
            (Activity.cost.ilike('%ücretsiz%')) |
            (Activity.cost == '0')
        )
    
    all_activities = query.all()
    return jsonify([activity.to_dict() for activity in all_activities])


# Main execution block
if __name__ == '__main__':
    # Uncomment the line below ONLY ONCE to create the database file and table.
    # After the first run, comment it out again or delete it.
    # create_database() # This should be commented out after initial setup!

    app.run(debug=True) # Run the Flask development server
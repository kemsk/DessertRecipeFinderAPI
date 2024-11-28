from flask import Flask, jsonify
from flask_restx import Api, Resource
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")  
db = client['RecAPI']  # Replace with your database name
recipes_collection = db['Recipes']  # Replace with your collection name

# Flask-RESTX API setup
api = Api(app, version='1.0', title='Recipe API', description='API for retrieving dessert recipes')

# ------------------------------ Recipe Endpoints ------------------------------

@api.route('/Recipes')
class RecipeList(Resource):
    def get(self):
        """Retrieve a list of recipe names and IDs"""
        # Retrieve recipe data from MongoDB (only name and recipeID)
        recipes = recipes_collection.find({}, {"_id": 0, "name": 1, "recipeID": 1})
        
        # Convert MongoDB cursor to a list
        recipe_list = [{"name": recipe["name"], "recipeID": recipe["recipeID"]} for recipe in recipes]
        
        # Return the list of recipes
        return jsonify(recipe_list)

# ------------------------------ Main Section ------------------------------

if __name__ == '__main__':
    app.run(debug=True)

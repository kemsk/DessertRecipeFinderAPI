from flask import Flask, jsonify, request
from flask_restx import Api, Resource, reqparse
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection setup
client = MongoClient("mongodb+srv://20220024573:T7CmWQ47ed9s8kpv@recipecluster.81ir5.mongodb.net/")
db = client['RecAPI']  # Replace with your database name
recipes_collection = db['Recipes']  # Replace with your collection name

# Flask-RESTX API setup
api = Api(app, version='1.0', title='Recipe API', description='API for retrieving dessert recipes')

# Request Parser for query parameters
recipe_parser = reqparse.RequestParser()
recipe_parser.add_argument('name', type=str, required=False, help='Name of the recipe to search for', location='args')

# ------------------------------ Recipe Endpoints ------------------------------

@api.route('/Recipes')
@api.doc(params={'name': 'Filter recipes by name'})  # Add Swagger parameter documentation
class RecipeList(Resource):
    def get(self):
        """Retrieve a list of recipe names and IDs based on the 'name' parameter"""
        
        # Parse the query parameters
        args = recipe_parser.parse_args()
        recipe_name = args.get('name')

        filters = {}
        if recipe_name:
            filters['name'] = {'$regex': recipe_name, '$options': 'i'}  # Case-insensitive search

        try:
            recipes = recipes_collection.find(filters, {"_id": 0, "name": 1, "recipeID": 1})
            recipe_list = [{"name": recipe["name"], "recipeID": recipe["recipeID"]} for recipe in recipes]

            return recipe_list if recipe_list else {"message": "No recipes found"}  # Automatically serialized
        
        except PyMongoError as e:
            return {"error": f"Database error: {str(e)}"}, 500
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

# ------------------------------ Main Section ------------------------------

if __name__ == '__main__':
    app.run(debug=True)

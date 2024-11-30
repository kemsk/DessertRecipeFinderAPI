from flask import Flask, jsonify, render_template, request
from flask_restx import Api, Resource, fields
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection setup
client = MongoClient(
    "mongodb+srv://20220024573:T7CmWQ47ed9s8kpv@recipecluster.81ir5.mongodb.net/?retryWrites=true&w=majority",
    tls=True,
    tlsAllowInvalidCertificates=False
)
db = client.RecAPI

# Define the collections
recipes_collection = db['Recipes']
ingredients_collection = db['Ingredients']
authors_collection = db['Authors']
dietary_benefits_collection = db['Dietarybenefits']
nutrition_info_collection = db['Nutritioninfo']
pictures_collection = db['Pictures']
users_collection = db['Users']
videos_collection = db['Videos']

# Flask-RESTX API setup
api = Api(app, version='1.0', title='Recipe API', description='API for dessert recipes')

# Recipe model for Flask-RESTX
recipe_model = api.model('Recipe', {
    'name': fields.String(required=True, description='Recipe Name'),
    'recipeID': fields.String(required=True, description='Recipe ID'),
    'ingredients': fields.List(fields.String, description='List of ingredients')
})

# Cache decorator (optional, depending on setup)
# @cache.cached(timeout=60, query_string=True)  # Add caching if needed


@app.route('/')
def home():
    return render_template('index.html')  # Renders the HTML front end

# API endpoint to get all data from Recipes collection with associated Ingredients
@app.route('/api/recipes', methods=['GET'])
def get_all_recipes():
    try:
        # Fetch all recipes from the Recipes collection
        recipes = recipes_collection.find({})
        response = []

        # Loop through each recipe to fetch its ingredients
        for recipe in recipes:
            recipe_ingredients = []
            # Fetch the ingredients that match the current recipeID from the Ingredients collection
            ingredients = ingredients_collection.find({'recipeID': recipe['recipeID']})
            for ingredient in ingredients:
                recipe_ingredients.append({
                    'name': ingredient.get('name', 'N/A'),
                    'quantity': ingredient.get('quantity', 'N/A')
                })

            # Add the recipe along with its ingredients
            response.append({
                'recipeID': str(recipe['recipeID']),
                'name': recipe.get('name', 'N/A'),
                'instructions': recipe.get('instructions', 'N/A'),
                'category': recipe.get('category', 'N/A'),
                'ingredients': recipe_ingredients
            })

        # Return the recipes and ingredients in JSON format
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return an error response if something goes wrong


# API endpoint to fetch a list of recipes (RESTful approach using Flask-RESTX)
@api.route('/api/recipe-list')
class RecipeList(Resource):
    def get(self):
        """Retrieve a list of recipes"""
        try:
            recipe_name = request.args.get('name')
            filters = {'name': {'$regex': recipe_name, '$options': 'i'}} if recipe_name else {}
            recipes = recipes_collection.find(filters, {"_id": 0, "name": 1, "recipeID": 1}).limit(100)
            return list(recipes), 200
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500


# API endpoint for Recipe with Ingredients using Flask-RESTX
@api.route('/api/recipe-with-ingredients')
class RecipeWithIngredients(Resource):
    def get(self):
        """Retrieve recipes with ingredients"""
        try:
            recipes = recipes_collection.find({})
            response = []

            for recipe in recipes:
                recipe_ingredients = []
                ingredients = ingredients_collection.find({'recipeID': recipe['recipeID']})
                for ingredient in ingredients:
                    recipe_ingredients.append({
                        'name': ingredient.get('name', 'N/A'),
                        'quantity': ingredient.get('quantity', 'N/A')
                    })

                response.append({
                    'recipeID': str(recipe['recipeID']),
                    'name': recipe.get('name', 'N/A'),
                    'instructions': recipe.get('instructions', 'N/A'),
                    'category': recipe.get('category', 'N/A'),
                    'ingredients': recipe_ingredients
                })

            return jsonify(response)
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request
from flask_restx import Api, Resource, fields
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app, version='1.0', title='Recipe API', description='API for dessert recipes')

client = MongoClient("mongodb+srv://20220024573:T7CmWQ47ed9s8kpv@recipecluster.81ir5.mongodb.net/")
db = client['RecAPI']
recipes_collection = db['Recipes']
ingredients_collection = db['Ingredients']


ns = api.namespace('recipes', description='Recipe operations')


recipe_model = api.model('Recipe', {
    'recipeID': fields.String(required=True, description='Recipe ID'),
    'name': fields.String(required=True, description='Recipe Name'),
    'instructions': fields.String(description='Recipe Instructions'),
    'category': fields.String(description='Recipe Category'),
    'ingredients': fields.List(fields.Nested(api.model('Ingredient', {
        'name': fields.String(description='Ingredient Name'),
        'quantity': fields.String(description='Ingredient Quantity')
    })))
})

# Endpoint to get all recipes
@ns.route('/')
class RecipeList(Resource):
    @ns.doc('list_recipes')
    @ns.marshal_list_with(recipe_model)
    def get(self):
        """Retrieve all recipes with ingredients"""
        recipes = recipes_collection.find({})
        response = []
        for recipe in recipes:
            recipe_ingredients = ingredients_collection.find({'recipeID': recipe['recipeID']})
            ingredients = [{'name': ing['name'], 'quantity': ing['quantity']} for ing in recipe_ingredients]
            response.append({
                'recipeID': recipe['recipeID'],
                'name': recipe['name'],
                'description': recipe['description'],
                'origin': recipe['origin'],
                'category': recipe.get('type', ''),
                'serving': recipe['serving'],
                'preptime': recipe['prep_time'],
                'cooktime': recipe['cook_time'],
                'difficulty': recipe['difficulty'],
                'majorIngredient': recipe['majorIngredient'],
                'instructions': recipe.get('instructions', ''),
                'createdDate': recipe('createdAt', ''),
                'UpdatedDate': recipe('updatedAt', '')
            })
        return response

    @ns.doc('create_recipe')
    @ns.expect(recipe_model)
    def post(self):
        """Create a new recipe with ingredients"""
        new_recipe = request.json
        recipes_collection.insert_one({
            'recipeID': new_recipe['recipeID'],
            'name': new_recipe['name'],
            'description': new_recipe['description'],
            'origin': new_recipe['origin'],
            'category': new_recipe.get('type', ''),
            'serving': new_recipe['serving'],
            'preptime': new_recipe['prep_time'],
            'cooktime': new_recipe['cook_time'],
            'difficulty': new_recipe['difficulty'],
            'majorIngredient': new_recipe['majorIngredient'],
            'instructions': new_recipe.get('instructions', ''),
            'createdDate': new_recipe('createdAt', ''),
            'UpdatedDate': new_recipe('updatedAt', '')
        })
        for ingredient in new_recipe.get('ingredients', []):
            ingredient['recipeID'] = new_recipe['recipeID']
            ingredients_collection.insert_one(ingredient)
        return {"message": "Recipe added successfully"}, 201

# Endpoint to get a recipe by name
@ns.route('/search')
class RecipeSearch(Resource):
    @ns.doc('get_recipe_by_name')
    @ns.param('name', 'Name of the recipe to search')
    @ns.marshal_list_with(recipe_model)
    def get(self):
        """Retrieve recipes by name"""
        recipe_name = request.args.get('name', '')
        recipes = recipes_collection.find({'name': {'$regex': recipe_name, '$options': 'i'}})
        response = []
        for recipe in recipes:
            recipe_ingredients = ingredients_collection.find({'recipeID': recipe['recipeID']})
            ingredients = [{'name': ing['name'], 'quantity': ing['quantity']} for ing in recipe_ingredients]
            response.append({
                'recipeID': recipe['recipeID'],
                'name': recipe['name'],
                'instructions': recipe.get('instructions', 'N/A'),
                'category': recipe.get('type', 'N/A'),
                'ingredients': ingredients
            })
        return response

if __name__ == '__main__':
    app.run(debug=True)

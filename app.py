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
    'description': fields.String(description='Recipe Description'),
    'origin': fields.String(description='Recipe Origin'),
    'category': fields.String(description='Recipe Category'),
    'serving': fields.String(description='Number of servings'),
    'preptime': fields.String(description='Preparation time'),
    'cooktime': fields.String(description='Cooking time'),
    'difficulty': fields.String(description='Recipe Difficulty'),
    'majorIngredient': fields.String(description='Major Ingredient'),
    'instructions': fields.String(description='Recipe Instructions'),
    'createdDate': fields.String(description='Creation Date'),
    'UpdatedDate': fields.String(description='Last Updated Date'),
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
                    'description': recipe.get('description', ''),
                    'origin': recipe.get('origin', ''),  # Use .get() to avoid KeyError
                    'category': recipe.get('type', ''),
                    'serving': recipe.get('serving', ''),
                    'preptime': recipe.get('prep_time', ''),
                    'cooktime': recipe.get('cook_time', ''),
                    'difficulty': recipe.get('difficulty', ''),
                    'majorIngredient': recipe.get('majorIngredient', ''),
                    'instructions': recipe.get('instructions', ''),
                    'createdDate': recipe.get('createdAt', ''),
                    'UpdatedDate': recipe.get('updatedAt', ''),
                    'ingredients': ingredients
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
                'description': new_recipe.get('description', ''),
                'origin': new_recipe.get('origin', ''),  # Use .get() to avoid KeyError
                'category': new_recipe.get('type', ''),
                'serving': new_recipe.get('serving', ''),
                'preptime': new_recipe.get('prep_time', ''),
                'cooktime': new_recipe.get('cook_time', ''),
                'difficulty': new_recipe.get('difficulty', ''),
                'majorIngredient': new_recipe.get('majorIngredient', ''),
                'instructions': new_recipe.get('instructions', ''),
                'createdDate': new_recipe.get('createdAt', ''),
                'UpdatedDate': new_recipe.get('updatedAt', ''),
    
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
                    'description': recipe.get('description', ''),
                    'origin': recipe.get('origin', ''),  # Use .get() to avoid KeyError
                    'category': recipe.get('type', ''),
                    'serving': recipe.get('serving', ''),
                    'preptime': recipe.get('prep_time', ''),
                    'cooktime': recipe.get('cook_time', ''),
                    'difficulty': recipe.get('difficulty', ''),
                    'majorIngredient': recipe.get('majorIngredient', ''),
                    'instructions': recipe.get('instructions', ''),
                    'createdDate': recipe.get('createdAt', ''),
                    'UpdatedDate': recipe.get('updatedAt', ''),
                    'ingredients': ingredients
            })
        return response

if __name__ == '__main__':
    app.run(debug=True)

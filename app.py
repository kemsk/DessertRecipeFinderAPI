from flask import Flask, request
from flask_restx import Api, Resource, fields
from pymongo import MongoClient

app = Flask(__name__)

api = Api(app, version='1.0', title='Recipe API', description='API for dessert recipes')

client = MongoClient("mongodb+srv://20220024573:T7CmWQ47ed9s8kpv@recipecluster.81ir5.mongodb.net/")
db = client['RecAPI']
recipes_collection = db['Recipes']
ingredients_collection = db['Ingredients']
dietarybenefits_collection = db['Dietarybenefits']
nutritioninfo_collection = db['Nutritioninfo']

ns = api.namespace('Recipes', description='Recipe operations')

recipe_model = api.model('Recipe', {
    'recipeID': fields.String(required=True, description='Recipe ID'),
    'name': fields.String(required=True, description='Recipe Name'),
    'description': fields.String(description='Recipe Description'),
    'origin': fields.String(description='Recipe Origin'),
    'type': fields.String(description='Recipe Category'),
    'serving': fields.String(description='Number of servings'),
    'preptime': fields.String(description='Preparation time'),
    'cooktime': fields.String(description='Cooking time'),
    'difficulty': fields.String(description='Recipe Difficulty'),
    'majorIngredient': fields.String(description='Major Ingredient'),
    'instructions': fields.String(description='Recipe Instructions'),
    'userID': fields.String(description='userID'), 
    'createdDate': fields.String(description='Creation Date'),
    'UpdatedDate': fields.String(description='Last Updated Date'),
    'videos': fields.String(description='videos'), 
    'pictures': fields.String(description='pictures'), 

    'ingredients': fields.List(fields.Nested(api.model('Ingredient', {
        'name': fields.String(description='Ingredient Name'),
        'quantity': fields.String(description='Ingredient Quantity'),
    }))),

    'dietarybenefits': fields.List(fields.Nested(api.model('DietaryBenefit', {
        'is_vegan': fields.String(description='Vegan or no'),
        'is_vegetarian': fields.String(description='Vegetarian or no'),
        'is_gluten_free': fields.String(description='Gluten-free or no'),
        'allergens': fields.String(description='List of allergens'),
    }))),

    'nutritioninfos': fields.List(fields.Nested(api.model('nutritioninfo', { 
        'calories_per_serving': fields.String(description='calories per serving'), 
        'protein_grams': fields.String(description='protein grams'), 
        'fat_grams': fields.String(description='fat grams'), 
        'carbohydrates_grams': fields.String(description='carbohydrates grams'), 
        'sugar_grams': fields.String(description='sugar grams'), 
    }))),
})

Diet_model = api.model('DietaryBenefits', {  
        'recipeID': fields.String(required=True, description='Recipe ID'),
        'name': fields.String(required=True, description='Recipe Name'),
        'description': fields.String(description='Recipe Description'),
        'dietarybenefits': fields.List(fields.Nested(api.model('DietaryBenefit', {
        'is_vegan': fields.String(description='Vegan or no'),
        'is_vegetarian': fields.String(description='Vegetarian or no'),
        'is_gluten_free': fields.String(description='Gluten-free or no'),
        'allergens': fields.String(description='List of allergens'),
    }))),
})

Nutri_model = api.model('NutritionInfo', {  
        'recipeID': fields.String(required=True, description='Recipe ID'),
        'name': fields.String(required=True, description='Recipe Name'),
        'description': fields.String(description='Recipe Description'),
        'nutritioninfos': fields.List(fields.Nested(api.model('nutritioninfo', { 
        'calories_per_serving': fields.String(description='calories per serving'), 
        'protein_grams': fields.String(description='protein grams'), 
        'fat_grams': fields.String(description='fat grams'), 
        'carbohydrates_grams': fields.String(description='carbohydrates grams'), 
        'sugar_grams': fields.String(description='sugar grams'), 
    }))),
})

@ns.route('/')
class RecipeList(Resource):
    @ns.doc('list_recipes')    # can retrieve all recipes but can also retrieve by /search plus param/s 
    @ns.marshal_list_with(recipe_model)
    def get(self):
        """Retrieve all recipes with ingredients and dietary benefits."""
        recipes = recipes_collection.find({})
        response = []

        for recipe in recipes:
            recipe_ingredients = list(ingredients_collection.find({'recipeID': recipe['recipeID']}))

            ingredients = [{'name': ing.get('name', ''), 
                            'quantity': ing.get('quantity', '')
            } for ing in recipe_ingredients]

            recipe_dietarybenefits = list(dietarybenefits_collection.find({'recipeID': recipe['recipeID']}))
            dietarybenefits = [{
                'is_vegan': diet.get('is_vegan', 'No'),
                'is_vegetarian': diet.get('is_vegetarian', 'No'),
                'is_gluten_free': diet.get('is_gluten_free', 'No'),
                'allergens': diet.get('allergens', '')
            } for diet in recipe_dietarybenefits]

            recipe_nutritioninfos = list(nutritioninfo_collection.find({'recipeID': recipe['recipeID']}))
            nutritioninfos = [{
                'calories_per_serving': nut.get('calories_per_serving', 'No'),
                'protein_grams': nut.get('protein_grams', 'No'),
                'fat_grams': nut.get('fat_grams', 'No'),
                'carbohydrates_grams': nut.get('carbohydrates_grams', ''),
                'sugar_grams': nut.get('sugar_grams', '')

            } for nut in recipe_nutritioninfos]

            response.append({
                'recipeID': recipe.get('recipeID', ''),
                'name': recipe.get('name', ''),
                'description': recipe.get('description', ''),
                'origin': recipe.get('origin', ''),
                'type': recipe.get('type', ''),
                'serving': recipe.get('servings', ''),
                'preptime': recipe.get('prep_time', ''),
                'cooktime': recipe.get('cook_time', ''),
                'difficulty': recipe.get('difficulty', ''),
                'majorIngredient': recipe.get('majorIngredient', ''),
                'instructions': recipe.get('instructions', ''),
                'userID': recipe.get('userID', ''),
                'createdDate': recipe.get('createdDate', ''),
                'UpdatedDate': recipe.get('UpdatedDate', ''),
                'ingredients': ingredients,
                'pictures': recipe.get('pictures', ''),
                'videos': recipe.get('videos', ''),
                'dietarybenefits': dietarybenefits,
                'nutritioninfo': nutritioninfos
            })
        
        return response

    @ns.doc('create_recipe')
    @ns.expect(recipe_model)
    def post(self):
        """Create a new recipe with ingredients and dietary benefits."""
        new_recipe = request.json
        recipes_collection.insert_one({
            'recipeID': new_recipe['recipeID'],
            'name': new_recipe['name'],
            'description': new_recipe.get('description', ''),
            'origin': new_recipe.get('origin', ''),
            'category': new_recipe.get('type', ''),
            'serving': new_recipe.get('servings', ''),
            'preptime': new_recipe.get('prep_time', ''),
            'cooktime': new_recipe.get('cook_time', ''),
            'difficulty': new_recipe.get('difficulty', ''),
            'majorIngredient': new_recipe.get('majorIngredient', ''),
            'instructions': new_recipe.get('instructions', ''),
            'userID': new_recipe.get('userID', ''),
            'createdDate': new_recipe.get('createdDate', ''),
            'UpdatedDate': new_recipe.get('UpdatedDate', ''),
            'pictures': new_recipe.get('pictures', ''),
            'videos': new_recipe.get('videos', ''),
        })

        for ingredient in new_recipe.get('ingredients', []):
            ingredient['recipeID'] = new_recipe['recipeID']
            ingredients_collection.insert_one(ingredient)

        for dietarybenefit in new_recipe.get('dietarybenefits', []):
            dietarybenefit['recipeID'] = new_recipe['recipeID']
            dietarybenefits_collection.insert_one(dietarybenefit)

        for nutritioninfo in new_recipe.get('nutritioninfos', []):
            nutritioninfo['recipeID'] = new_recipe['recipeID']
            nutritioninfo_collection.insert_one(nutritioninfo)

        return {"message": "Recipe added successfully"}, 201

@ns.route('/<string:name>')
@ns.param('name', 'The name of the recipe to search for')
class RecipeSearch(Resource):
    @ns.doc('search_recipe_by_name')
    @ns.marshal_with(recipe_model)
    def get(self, name):
        """Search for a recipe by name."""
        recipes = recipes_collection.find({})
        response = []

        for recipe in recipes:
            recipe_ingredients = list(ingredients_collection.find({'recipeID': recipe['recipeID']}))

            ingredients = [{'name': ing.get('name', ''), 
                            'quantity': ing.get('quantity', '')
            } for ing in recipe_ingredients]

            recipe_dietarybenefits = list(dietarybenefits_collection.find({'recipeID': recipe['recipeID']}))
            dietarybenefits = [{
                'is_vegan': diet.get('is_vegan', 'No'),
                'is_vegetarian': diet.get('is_vegetarian', 'No'),
                'is_gluten_free': diet.get('is_gluten_free', 'No'),
                'allergens': diet.get('allergens', '')
            } for diet in recipe_dietarybenefits]

            recipe_nutritioninfos = list(nutritioninfo_collection.find({'recipeID': recipe['recipeID']}))
            nutritioninfos = [{
                'calories_per_serving': nut.get('calories_per_serving', 'No'),
                'protein_grams': nut.get('protein_grams', 'No'),
                'fat_grams': nut.get('fat_grams', 'No'),
                'carbohydrates_grams': nut.get('carbohydrates_grams', ''),
                'sugar_grams': nut.get('sugar_grams', '')

            } for nut in recipe_nutritioninfos]

            response.append({
                'recipeID': recipe.get('recipeID', ''),
                'name': recipe.get('name', ''),
                'description': recipe.get('description', ''),
                'origin': recipe.get('origin', ''),
                'type': recipe.get('type', ''),
                'serving': recipe.get('servings', ''),
                'preptime': recipe.get('prep_time', ''),
                'cooktime': recipe.get('cook_time', ''),
                'difficulty': recipe.get('difficulty', ''),
                'majorIngredient': recipe.get('majorIngredient', ''),
                'instructions': recipe.get('instructions', ''),
                'userID': recipe.get('userID', ''),
                'createdDate': recipe.get('createdDate', ''),
                'UpdatedDate': recipe.get('UpdatedDate', ''),
                'ingredients': ingredients,
                'pictures': recipe.get('pictures', ''),
                'videos': recipe.get('videos', ''),
                'dietarybenefits': dietarybenefits,
                'nutritioninfo': nutritioninfos
            })
        
        return response

@ns.route('/search/<string:name>/dietary-benefits')
@ns.param('name', 'The name of the recipe to search for')
class RecipeSearch(Resource):
    @ns.doc('search_dietary-benefits_by_name')
    @ns.marshal_list_with(Diet_model)
    def get(self, name):
        """Search for a recipe by name."""
        recipes = recipes_collection.find({'name': {'$regex': name, '$options': 'i'}})
        response = []
        for recipe in recipes:
            recipe_dietarybenefits = list(dietarybenefits_collection.find({'recipeID': recipe['recipeID']}))
            dietarybenefits = [{
                'is_vegan': diet.get('is_vegan', 'No'),
                'is_vegetarian': diet.get('is_vegetarian', 'No'),
                'is_gluten_free': diet.get('is_gluten_free', 'No'),
                'allergens': diet.get('allergens', '')
            } for diet in recipe_dietarybenefits]

            response.append({
                'recipeID': recipe.get('recipeID', ''),
                'name': recipe.get('name', ''),
                'description': recipe.get('description', ''),
                'dietarybenefits': dietarybenefits
            })

        return response
@ns.route('/search/<string:name>/nutrition-info')
@ns.param('name', 'The name of the recipe to search for')
class RecipeSearch(Resource):
    @ns.doc('search_nutrition-info_by_name')
    @ns.marshal_list_with(Nutri_model)
    def get(self, name):
        """Search for a recipe by name."""
        recipes = recipes_collection.find({'name': {'$regex': name, '$options': 'i'}})
        response = []

        for recipe in recipes:
            recipe_nutritioninfos = list(nutritioninfo_collection.find({'recipeID': recipe['recipeID']}))
            nutritioninfos = [{
                'calories_per_serving': nut.get('calories_per_serving', 'No'),
                'protein_grams': nut.get('protein_grams', 'No'),
                'fat_grams': nut.get('fat_grams', 'No'),
                'carbohydrates_grams': nut.get('carbohydrates_grams', ''),
                'sugar_grams': nut.get('sugar_grams', '')
            } for nut in recipe_nutritioninfos]

            response.append({
                'recipeID': recipe.get('recipeID', ''),
                'name': recipe.get('name', ''),
                'description': recipe.get('description', ''),
                'nutritioninfos': nutritioninfos
            })

        return response



if __name__ == '__main__':
    app.run(debug=True)

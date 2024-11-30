from flask import Flask, jsonify, request
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
recipes_collection = db.Recipes

# Flask-RESTX API setup
api = Api(app, version='1.0', title='Recipe API', description='API for dessert recipes')
recipe_model = api.model('Recipe', {
    'name': fields.String(required=True, description='Recipe Name'),
    'recipeID': fields.String(required=True, description='Recipe ID')
})

@cache.cached(timeout=60, query_string=True)
@app.route("/", methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True)

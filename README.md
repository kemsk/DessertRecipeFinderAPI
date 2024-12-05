# DessertRecipeFinderAPI
## Overview
The Culinary School Recipe Finder API offers culinary students and professionals a comprehensive system to explore, categorize, and manage recipes. The API supports filtering by recipe type, country of origin, and dietary needs, while also providing detailed nutritional and health-related data.

#### Description of the file inside the Repository
- **RecipeAPI Folder:** Extracted data from each of the collections in the mobngodb database 
- **app.py:** The python code to run the api (in localhost)
- **openAPI.yaml:** Is the Api design using swagger

## Api Functionality 
- Retrieve All Recipes: Get a list of all recipes stored in the database.
- Post Recipes: Add new recipes to the database.
**Post method request body format**
~~~
{
  "recipeID": "string",
  "name": "string",
  "description": "string",
  "origin": "string",
  "type": "string",
  "serving": "string",
  "preptime": "string",
  "cooktime": "string",
  "difficulty": "string",
  "majorIngredient": "string",
  "instructions": "string",
  "userID": "string",
  "createdDate": "string",
  "UpdatedDate": "string",
  "videos": "string",
  "pictures": "string",
  "ingredients": [
    {
      "name": "string",
      "quantity": "string"
    }
  ],
  "dietarybenefits": [
    {
      "is_vegan": "string",
      "is_vegetarian": "string",
      "is_gluten_free": "string",
      "allergens": "string"
    }
  ],
  "nutritioninfos": [
    {
      "calories_per_serving": "string",
      "protein_grams": "string",
      "fat_grams": "string",
      "carbohydrates_grams": "string",
      "sugar_grams": "string"
    }
  ]
}
~~~
- Retrieve Recipes by Name or Other Categories: Search recipes by name, type, country of origin, and other parameters.

## Personalized Element
Each user is assigned a unique UserID that personalizes the API usage. With this personalization:
- Users can manage their own recipe collections.
- Recipes created or updated are tagged to specific users.
This enables a user-centric approach, providing a tailored experience for different user groups such as culinary students, health professionals and others.

## Unique Feature
### Advanced Filtering and Categorization
Unlike many standard recipe APIs, this API allows users to filter recipes not only by type or origin but also by dietary preferences, allergens, and nutritional goals. Which will be ideal for:
- **Culinary Schools:** To explore regional desserts and types of recipes.
- **Nutritionists and Dieticians:** To recommend recipes tailored to specific health conditions or dietary restrictions.
- **Hospitals:** To offer patient-specific meal plans.

### Detailed Nutritional and Dietary Benefits
The API stands out by providing detailed dietary benefits and nutritional breakdowns of each recipe, helping users make informed decisions.

## How to setup and use the API
1. Clone the Git repository.
   ~~~
   git clone https://github.com/2401-XU-ITCC14A/semi-final-exam-kemsk.git
   ~~~
2. Install the required dependencies.
  ~~~
  pip install flask
  pip install flask-restx
  pip install pymongo
  ~~~
virtual envirenment setup is reccomended but was not implemented in this repo

3. Run the app.py file to start the server. 
  ~~~
  python app.py
  ~~~
4. Access the API locally at http://127.0.0.1:5000/. 
   
## Http requests
- ###### GET ALL RECIPES: http://127.0.0.1:5000/Recipes/ 
- ###### GET A RECIPE TROUGH PARAMS: http://127.0.0.1:5000/Recipes/search?<param=value>
  ###### Some of the Parameters
|  Parameters   | Values        |
|---------------|---------------|
| **name** | Name of a recipe **Ex. Biko, Leche Flan, Tiramisu, etc..** | 
| **origin** | Country a recipe is from or originated from **Ex. USA, UK, New Zealand, France, Italy, Philippines** | 
| **category** | From what dessert category a recipe is from **Ex. Dessert** |
| **majorIngredient** | Major Ingredient of a recipe you are finding **Ex. Glutinous Rice, Shaved Ice , Strawberries** |
| **serving** | Number of serving of a recipe in minutes **Ex. 4, 6, 8**  | 
| **preptime** | Preparation time of a recipe in minutes **Ex. 15, 20, 30**   | 
| **cooktime** | Cook time of a recipe **Ex. 10, 15, 45, 60**  | 
| **difficulty** | Difficulty of a recipe **Ex. Easy, Medium, Moderate** |
- ###### POST A RECIPE: http://127.0.0.1:5000/Recipes/ use in post method


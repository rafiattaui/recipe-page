from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate('recipe-page-project-firebase-adminsdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
recipes_ref = db.collection('recipes')

@app.route("/")
def index():
    # Fetch recipes from Firestore
    recipes = [
        {**doc.to_dict(), "id": doc.id} for doc in recipes_ref.stream()
    ]
    
    # Pass documents to templates in the form of a list with recipe dictionaries
    return render_template("recipes.html", recipes=recipes)

@app.route("/", methods=["POST","GET"])
def index_query():
    recipes = []
    if request.method == "POST":
        query = request.form.get("query","".lower())
        docs = recipes_ref.stream()
        recipes = [{**doc.to_dict(), "id": doc.id} for doc in docs if query in doc.to_dict()['name'].lower()]
        return render_template("recipes.html", recipes=recipes, query=query)
    
@app.route("/addrecipe")
def addrecipe():
    return render_template("addrecipe.html")

@app.route("/submit", methods=["POST"])

# Handle the submission of a new recipe via a POST request.
# This function retrieves form data submitted by the user, processes it, and stores it in the database.
# It also prints the submitted data to the console for debugging purposes and renders a confirmation page.
# Form Data:
#     recipe_name (str): The name of the recipe.
#     recipe_description (str): A description of the recipe.
#     recipe_video (str): A URL to a video of the recipe.
#     recipe_image (str): A URL to an image of the recipe.
#     recipe_difficulty (str): The difficulty level of the recipe.
#     ingredient_name[] (list of str): A list of ingredient names.
#     ingredient_quantity[] (list of str): A list of ingredient quantities corresponding to the ingredient names.
#     recipe_step[] (list of str): A list of steps to prepare the recipe.
# Returns:
#     Response: Renders the 'submitted.html' template with the recipe name and the length of the description (excluding spaces).
    
def submit():
    # Access form data
    recipe_name = request.form["recipe_name"]
    recipe_description = request.form["recipe_description"]
    recipe_video = request.form["recipe_video"]
    recipe_image = request.form["recipe_image"]
    recipe_difficulty = request.form["recipe_difficulty"]
    
    # Ingredients (Access ingredients names and quantities as seperate lists)
    ingredient_names = request.form.getlist("ingredient_name[]")
    ingredient_quantities = request.form.getlist("ingredient_quantity[]")
    
    # Steps (Access step descriptions as a list)
    recipe_steps = request.form.getlist("recipe_step[]")
    
    # Print values to check them
    print(f"Recipe Name: {recipe_name}")
    print(f"Description: {recipe_description}")
    print(f"Video Link: {recipe_video}")
    print(f"Image Link: {recipe_image}")
    print(f"Difficulty: {recipe_difficulty}")
    print(f"Ingredients: {dict(zip(ingredient_names, ingredient_quantities))}")
    print(f"Steps: {recipe_steps}")
    
    recipe_data = {
        'name': recipe_name,
        'description': recipe_description,
        'video': recipe_video,
        'imageurl': recipe_image,
        'difficulty': recipe_difficulty,
        'ingredients': dict(zip(ingredient_names, ingredient_quantities)),
        'steps': recipe_steps,
    }
    
    if not (len(recipe_description.replace(" ","")) > 100):
        recipes_ref.add(recipe_data) # Add data to database

    return render_template("submitted.html", name=recipe_data["name"], len=len(recipe_description.replace(" ",""))) # Redirect to submitted page

@app.route("/editrecipe=<recipeid>")
def editrecipe(recipeid):
    
    # Fetch document using recipe id, and turn it to a dictionary.
    doc_ref = recipes_ref.document(recipeid)
    recipe = {**doc_ref.get().to_dict(), "id": doc_ref.id}
    print(recipe)
    return render_template("editrecipe.html", recipe=recipe)

@app.route("/update=<recipeid>", methods=["POST"])
def update(recipeid):
    # Access form data
    recipe_name = request.form["recipe_name"]
    recipe_description = request.form["recipe_description"]
    recipe_video = request.form["recipe_video"]
    recipe_image = request.form["recipe_image"]
    recipe_difficulty = request.form["recipe_difficulty"]
    
    # Ingredients (Access ingredients names and quantities as seperate lists)
    ingredient_names = request.form.getlist("ingredient_name[]")
    ingredient_quantities = request.form.getlist("ingredient_quantity[]")
    
    # Steps (Access step descriptions as a list)
    recipe_steps = request.form.getlist("recipe_step[]")
    
    recipe_data = {
        'name': recipe_name,
        'description': recipe_description,
        'video': recipe_video,
        'imageurl': recipe_image,
        'difficulty': recipe_difficulty,
        'ingredients': dict(zip(ingredient_names, ingredient_quantities)),
        'steps': recipe_steps,
    }
    
    doc_ref = recipes_ref.document(recipeid)
    doc_ref.set(recipe_data)
    print(recipe_data)
    
    return render_template("update.html", name=recipe_data["name"])
    

@app.route("/recipe=<recipeid>")
def recipe(recipeid):
    
    # Fetch document using recipe id, and turn it to a dictionary.
    doc_ref = recipes_ref.document(recipeid)
    recipe = {**doc_ref.get().to_dict(), "id": doc_ref.id}
    print(recipe)
    return render_template("RecipePage.html", recipe=recipe)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/base")
def base():
    return render_template("base.html")

@app.route("/deleterecipe=<recipeid>")
def deleterecipe(recipeid):
    name = recipes_ref.document(recipeid).get().to_dict()["name"]
    recipes_ref.document(recipeid).delete()
    return render_template("deleted.html", name=name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

import firebase_admin
from firebase_admin import credentials, firestore

# Use a service account.
cred = credentials.Certificate('recipe-page-project-firebase-adminsdk.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
print("Firebase initialized")

def create_empty_recipe():
    # Create empty recipe
    db.collection('recipes').add({
        'name': '',
        'description': '',
        'difficulty':0,
        'imageurl': '',
        'ingredients': {},
        'tags': [],
    })

def create_recipe(dict):
    # Create recipe
    # ingredients is a dictionary with ingredient names as keys and quantities as values
    # tags is a list of strings
    # difficulty is an integer between 1 and 3
    # imageurl is a string
    # name is a string
    # description is a string
    
    db.collection('recipes').add({
        "name" : dict["name"],
        "description" : dict["description"],
        "difficulty" : dict["difficulty"],
        "imageurl" : dict["imageurl"],
        "ingredients" : dict["ingredients"],
        "steps" : dict["steps"],
        "tags": dict["tags"],
    })
    
def delete_recipe(recipe_id):
    # Delete recipe
    db.collection('recipes').document(recipe_id).delete()

def get_ids():
    # Get all recipe ids
    recipes_ref = db.collection('recipes')
    return [doc.id for doc in recipes_ref.stream()]

doc_ref = db.collection('recipes').document('zADB5D3wgIlSJkiib0uR')
db.collection('recipes').add(doc_ref.get().to_dict())

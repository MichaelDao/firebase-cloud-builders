import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# define our gcp project
project_id = "anzsandbox"

# Find and apply application default credentials
cred = credentials.ApplicationDefault()

# Initialize firebase admin with the credentials
firebase_admin.initialize_app(cred, {
    'projectId': project_id,
})


print (cred.get_access_token())

# playground
Sourced from many brilliant tutorials from google, i am just dumping all my code here for now as i figure out how things work.

## prerequisites
make sure your cloud build service account has the `Firebase Admin` role given to it

## python remote config
in the `/pythonRemoteConfig` directory, we will demonstrate how to use the remote config rest api script with cloud build

1. build your docker image and publish it into container registry
```
gcloud builds submit --tag gcr.io/<your gcp project>/uploadremoteconfig .
```
2. once your cloud build has finished building your docker image, run the tests
```
gcloud builds submit --config cloudbuild.yaml .
```
Now check the logs in cloud build.

You can refer to https://cloud.google.com/cloud-build/docs/running-builds/start-build-manually for more details


## python firestore
Here is something that posts up sample data to your firebase firestore database with firebase admin sdk

in the '/pythonFirestore' directory, you want to build your image and run it on cloud build.

1. build your docker image and publish it into container registry
```
gcloud builds submit --tag gcr.io/<your gcp project>/uploadfirestore .
```
2. once your cloud build has finished building your docker image, run the tests
```
gcloud builds submit --config cloudbuild.yaml .
```
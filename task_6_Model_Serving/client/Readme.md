# Client

<img src="ClientArchitecture.JPG">

## Deploying Model In Mobile
1. Model Trainig will happen in server(i.e. where ever training of model is done is refered as server here).
2. Model can be saved with .h5, .pkl, .sav, .tfjs extensions.
3. Covert the model to Tf lite using Tesnorflow API.
4. Then deployment of the TF Lite model using flutter.
5. Capture the image from mobile camera or browse from galary to predict the prediction in offline mode.
6. Connect with S3 bucket to save the output of for data archival.


## UI/UX design for mobile app
<img src="omdena_UI.png">

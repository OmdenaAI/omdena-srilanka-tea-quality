# Server Side


<img src="ServerArchitecture.JPG">

## Expose Model As An API
1. Model Trainig will happen in server(i.e. where ever training of model is done is refered as server here)
2. Model can be saved with .h5, .pkl, .sav
3. Hosting the model in server side using Flask Framework
4. Now Flask API can be consumend by mobile app.
5. Connect with S3 bucket to save the output of for data archival 


## Flask Api Deployment in EC2 instance AWS
1. Flask code
2. Run and check in local
3. Create AWS account
4. Create EC2 instance
5. Download putty and putty gen
6. Generate private key with putty gen
7. Download WinSCP(to copy and paste in cloud instance)
8. Update the port in flask code(make use you have 0.0.0.0 and 8080 as your default port
9. Install the librabies by connecting through putty
10. Run  python3 app.py
11. Get the exicution url from the ec2 instance and verify it

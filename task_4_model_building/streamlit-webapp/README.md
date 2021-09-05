
## General info
This application provides an inteface to detect and classify tea leaves.
	
## Dependencies
* Docker
* Model Weights
	
## Setup
To run this application, you need to enable the detection API:

For CPU
```
$ docker run -e VISION-DETECTION=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack
```
For GPU
```
$ sudo docker run --gpus all -e VISION-DETECTION=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack:gpu
```
For Windows OS
```
$ deepstack --VISION-DETECTION True --PORT 80
```
### Basic Parameters

**-e VISION-DETECTION=True** This enables the object detection API.

**-v localstorage:/datastore** This specifies the local volume where DeepStack will store all data.

**-p 80:5000** This makes DeepStack accessible via port 80 of the machine.



## Run App
```
$ streamlit run app.py
```

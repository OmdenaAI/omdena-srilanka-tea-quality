# Model serving (Task-6)

## [Server](server/)

Server handles task to serve the model via Flask API using Azure App service.

## [Client](client/)

Mobile application as a client uses the endpoint from server's API to make predictions of the uploaded image.

It also has offline mode (when internet service is unavailable), it has its on-premise model that is used for predictions.
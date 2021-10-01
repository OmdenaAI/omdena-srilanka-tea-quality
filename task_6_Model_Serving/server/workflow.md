# Requied Software Packages

- **Python3** and **PIP** package manager
- **Nginx** :- It's a web server which can also be used as a reverse proxy, load balancer and mail proxy.
- **Gunicorn3** :- Standalone WSGI web application server which offers a lot of functionality.
- **Flask** :- It's a micro web framework written in Python.

# Steps
 
- Create a new EC2 Instance
 
- Choose Ubuntu Server ( We can choose other one also but i do have some familarity with this)

-Then create a new Key pair (It will take around 1 minute or so)

- Now we have to include our port number where we are going to run our program.

- For that scroll down the description, and in `Security groups` there is `launch-wizard` option choose it.

- Then select the `Security group` and then choose edit `Inbound Rules`.

- New page will open then click on `Add Rule`, then add the `Port Number`(eg 80) and `Source` (eg 0.0.0.0/0). Then save the `rules`.


- As we have already created key value pair, so  we can download it and save it at someplace. 

- Let just say we save it at `C Drive`->`user`->`your_folder name`->`make a folder named .ssh`. Inside the `.ssh` folder we have saved it.

- Now inside the EC2 Dashboard click on `Connect` option and choose standalone SSH Client and copy the code written inside th Example is bold black.

- Now open `CMD` and go inside the `.ssh` folder directory using `cd` command and then paste that code on terminal.  They will ask for `Yes/No`, click on `Yes`.

- Now we are succcesfully connected to our `EC2 Instance`.

- Now we can download our program from `Github` (Always put every single content of project on Github) by using `git clone`.

***(All the required installing part)***

- Do `sudo apt-get update` on terminal
- Then `sudo apt-get install python-pip3`
- `sudo pip3 install flask`
- `sudo apt-get install nginx`
- `sudo apt-get gunicorn3`


- Now just go inside the python file inside which we have written our python code.

- run this code `python3 flaskapp.py`

- Now we can see our application running on web by copyinh `IPv4 Public IP` from the `Description` in the `EC2 Instance Dashboard`.

<!-- - `pip install --user -r requirements.txt` -->





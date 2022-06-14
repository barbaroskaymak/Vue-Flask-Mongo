
## Run the server-side Flask app in one terminal window

    $ cd Server
    
    $ pip install virtualenv 
    
    $ virtualenv venv
    
    $ source venv/bin/activate " for win " venv\Scripts\activate
    
    (venv)$ python -m pip install --upgrade pip
    
    (venv)$ pip install -r requirements.txt
    
    Open app.py Mongodb URI/(host) edit.
    
    (venv)$ flask run


    Navigate to [http://localhost:5000](http://localhost:5000)

## Run the client-side Vue app in a different terminal window:

    $ cd client
    
    $ npm install
    
    $ npm run serve
    
    

    Navigate to [http://localhost:8080](http://localhost:8080)

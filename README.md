
1. Run the server-side Flask app in one terminal window

    $ cd Server
    
    $ python3.9 -m venv env
    
    $ source venv/bin/activate win venv\Scripts\activate
    
    (venv)$ python -m pip install --upgrade pip
    
    (venv)$ pip install -r requirements.txt
    
    (venv)$ flask run


    Navigate to [http://localhost:5000](http://localhost:5000)

1. Run the client-side Vue app in a different terminal window:

    $ cd client
    
    $ npm install
    
    $ npm run serve
    
    

    Navigate to [http://localhost:8080](http://localhost:8080)

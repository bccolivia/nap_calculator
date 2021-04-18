# nap_calculator
Web-based nap calculator - Given preferred wake windows and desired bedtime, generates suggestions on when to cap a nap and when to start the next nap
Here's what it looks like:

http://54.191.38.114:5000/nap_calculator

Notes:
1) "Nap Calculator.ipynb" was the original version I put together in Jupyter Notebook
2) I adopted it to a web app by using Flask (following instructions here: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world )
3) To set this up on your webserver, "nap_calculator.py" is the Flask app you want to run:
    - export FLASK_APP=nap_calculator.py
    - flask run --host=0.0.0.0

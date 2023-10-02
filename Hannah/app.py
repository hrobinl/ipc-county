# 1. import Flask
from flask import Flask

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/home")
def home():
    print("Server received request for 'Home' page...")
    return "list,list"

@app.route("/charts")
def about():
    print("Server received request for 'Charts' page...")
    return "charts"


# 4. Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "static"


if __name__ == "__main__":
   app.run(debug=True)




# 1. Import Flask
#from flask import Flask


# 2. Create an app
#app = Flask(__name__)


# 3. Define static routes
#@app.route("/")
#def index():
#    return "r"


#@app.route("/about")
#def about():
#    name = "Peleke"
#    location = "Tien Shan"

#    return f"My name is {name}, and I live in {location}."


#@app.route("/contact")
#def contact():
#    email = "peleke@example.com"

#    return f"Questions? Comments? Complaints? Shoot an email to {email}."


# 4. Define main behavior
#if __name__ == "__main__":
#    app.run(debug=True)
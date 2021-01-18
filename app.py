# *****Flask project*****
# created by: *****Pradeep Kumar Yadav*****
# contact: *****pkyadav3444@gmail.com*****
# import required libraries
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@hostname/dbname'
app.config['SECRET_KEY'] = 'i_love_india' # you can right anything according to your choice
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# create a class to access the table or create if does not exist in db
class APIUserModel(db.Model):
    __tablename__='subscriber'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))


# create a simple route for url and mention your method also
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method=='POST':
        form = request.form
        # take the input from html form and save it to a variable
        email = form['email']
        # give the varible to the class as an argument
        api_user_model = APIUserModel(email=email)
        # every time you need to create a session to create changes in your database
        save_to_database = db.session()
        # use try and except for handle error
        try:
            # add to database using class(created above)
            save_to_database.add(api_user_model)
            # commit your changes to db
            save_to_database.commit()
            # and redirect to home page
            return redirect(url_for(index))
        except:
            # if not able to add to db than rollback everything as it is
            save_to_database.rollback()
            # and remove all garbage from your db
            save_to_database.flush()
    # and here this is your server's home page        
    return render_template("index.html")

if __name__ == "__main__":
    # for create changes in db you need to call create_all function
    db.create_all()
    # here you can add debug=True(optional) and port(optional) as you want
    app.run(debug= True, port=8000)
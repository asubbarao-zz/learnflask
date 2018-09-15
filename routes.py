from flask import Flask, render_template, request, session, redirect, url_for
#session/redirect are used for cookies 
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm #this is the signupform backent from flaskwtf




app = Flask(__name__)
print("test")
#start up the db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learnflask'
db.init_app(app)

#this protects against csrf attack 
app.secret_key = "development-key"

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about123")
def aboutabc():
  return render_template("about.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	#first create a new 
	form = SignupForm()
	if 'email' in session:
		return redirect(url_for('home'))


	if request.method == "POST":
	  if form.validate() == False:
	    return render_template('signup.html', form=form)
	  else:
	  	new_user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
	  	db.session.add(new_user)
	  	db.session.commit()

	  	session['email'] = new_user.email
	  	return redirect(url_for('home'))

	elif request.method == "GET":
	  return render_template('signup.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():

	form = LoginForm()

	if 'email' in session:
		return redirect(url_for('home'))


	if request.method == "POST":
		if form.validate() == False:
			return render_template("login.html", form=form)
		else:
			email = form.email.data
			password = form.password.data

			user = User.query.filter_by(email=email).first()
			
			if user is not None and user.check_password(password):
				session['email'] = form.email.data
				return redirect(url_for("home"))

			else:
				return redirect(url_for("login"))

	elif request.method == 'GET':
	  return render_template('login.html', form=form)


#distinguish between the GET and POST requests 
	if request.method == 'POST':
	  print("there was a POST")
	  if form.validate() == False:
	  	print("there was a validation error")
	  	return render_template('signup.html', form=form)

	  else:
	  	new_user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
	  	db.session.add(new_user)
	  	db.session.commit()
	  
	  session['email'] = new_user.email
	  return redirect(url_for('home'))

	elif request.method == "GET":
	  print("there was a GET")
	  return render_template('signup.html', form=form)

@app.route('/home', methods=['GET','POST'])
def home():
	form = AddressForm()

	places = []
	my_coordinates = (37.4221, -122.0844)

	if 'email' not in session:
		return redirect(url_for('login'))



	if request.method == 'POST':
		if form.validate() == False:
			return render_template('home.html', form=form)
		else:
			#get the address
			address = form.address.data

			#want to use geodata api - make a model (models.py)
			#query places around address
			p = Place()
			my_coordinates = p.address_to_latlng(address)
			places = p.query(address)

			return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)

			
	elif request.method == 'GET':
		return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)

@app.route('/logout')
def logout():
	session.pop('email', None)
	return redirect(url_for('index'))

if __name__ == "__main__":
  app.run(debug=True)

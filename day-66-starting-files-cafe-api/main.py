import random
from flask import Flask, jsonify, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import secrets
import requests

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
# Generate a random secret key
secret_key = secrets.token_hex(16)
print(secret_key)

app = Flask(__name__)

# Set the secret key for session management
app.config['SECRET_KEY'] = secrets.token_hex(16)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    def to_dict(self):
        # return {
        #     "id": self.id,
        #     "name":self.name,
        #     "map_url": self.map_url,
        #     "img_url": self.img_url,
        #     "location": self.location,
        #     "seats": self.seats,
        #     "has_toilet": self.has_toilet,
        #     "has_wifi": self.has_wifi,
        #     "has_sockets": self.has_sockets,
        #     "can_take_calls": self.can_take_calls,
        #     "coffee_price": self.coffee_price,
        # }

        # Method 2.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # # Method 3. Altenatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all() # Scalar return the first result or none if no rows present
    random_cafe = random.choice(all_cafes)
    return jsonify(random_cafe.to_dict())

# Let's create an API similar to this https://laptopfriendly.co/bristol
@app.route("/all", methods=["GET"])
def get_all_cafe():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    # Ensure there are cafes to choose from
    if not all_cafes:
        return jsonify({"error": "No cafes found"}), 404

    # Convert each Cafe object to a dictionary this give it the json structure [{},{}]
    cafes_list = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafe=cafes_list)

# search based on particular location
@app.route("/search", methods=["GET"])
def search_location():
    query_location = request.args.get("loc")

    # Check if the location parameter is provided
    if not query_location:
        return jsonify({"error": "Location parameter is required"}), 404

    # Query the database to find cafes with the matching location
    # The ilike function is used for a case-insensitive match, allowing partial matches.
    # This means searching with the term 'New' will match entries like 'New York' and 'New Jersey'.
    result = db.session.execute(db.select(Cafe).filter(Cafe.location.ilike(f"%{query_location}%")))
    cafes = result.scalars().all()

    # Check if any cafes are found
    if not cafes:
        return jsonify({"error": f"No cafes found for location '{query_location}'"}), 404

    # Convert each cafe object to a dictionary
    cafe_list = [cafe.to_dict() for cafe in cafes]
    return jsonify(cafes=cafe_list)



# HTTP POST - Create Record
# what if we want to add new cafe to the database like https://laptopfriendly.co/suggest
@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        map_url = request.form.get("map_url")
        img_url = request.form.get("img_url")
        location = request.form.get("location")
        seats = request.form.get("seats")
        has_toilet = bool(request.form.get("has_toilet"))
        has_wifi = bool(request.form.get("has_wifi"))
        has_sockets = bool(request.form.get("has_sockets"))
        can_take_calls = bool(request.form.get("can_take_calls"))
        coffee_price = request.form.get("coffee_price")

        # Create new cafe object
        new_cafe = Cafe(
            name=name,
            map_url=map_url,
            img_url=img_url,
            location=location,
            seats=seats,
            has_toilet=has_toilet,
            has_wifi=has_wifi,
            has_sockets=has_sockets,
            can_take_calls=can_take_calls,
            coffee_price=coffee_price
        )

        # Add to database
        db.session.add(new_cafe)
        try:
            db.session.commit()
            flash("Cafe added successfully!", "success")
            return redirect(url_for("get_all_cafe"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding cafe: {e}", "danger")
    return render_template("add.html")


# HTTP PUT/PATCH - Update Record
# PUT basically update an entirely, while PATCH only update that part where is needed.
# 127.0.0.1:5000/update-price/22?new_price=20 or POSTMAN
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    try:
        cafe = db.get_or_404(Cafe, cafe_id)

        if cafe:
            cafe.coffee_price = new_price
            db.session.commit()

            return jsonify({"message": f"Price updated for product {cafe_id}"})

    except Exception as e:
        return jsonify(error={f"{e}": "Cafe not found."}), 404

# HTTP DELETE - Delete Record
# http://127.0.0.1:5000/report-closed/23?api-key=TopSecretAPIKey
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    print("Received DELETE request")
    api_key = request.args.get("api-key")
    print(f"Received API key: {api_key}")

    if api_key == "TopSecretAPIKey":
        cafe_to_close = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        if cafe_to_close:
            db.session.delete(cafe_to_close)
            db.session.commit()
            return jsonify({"message": "Cafe successfully deleted"}), 200
        else:
            return jsonify({"error": "Cafe not found"}), 404
    else:
        return jsonify({"error": "Incorrect API key"}), 403



if __name__ == '__main__':
    app.run(debug=True)

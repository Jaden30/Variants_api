from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os 




# CREATING AN OBJECT OF THE CLASS FLASK 
app = Flask(__name__)
# setting up our base directory using the os.path
basedir = os.path.abspath(os.path.dirname(__file__))

#Database 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
# an app.config file that we dont need but if we dont use would complain in the terminal 
# the false will stop it from complaining to the terminal 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# create an object of the database taking our app onject as an argument 
db = SQLAlchemy(app)
# create an object of the marshmallow taking our app object as an argument 
ma = Marshmallow(app)

# create a class resources 

class Variants(db.Model):
    # the use of db.column assigns a field 
    Variant_id = db.Column(db.Integer, primary_key=True)
    location= db.Column(db.String(20))
    Alleles = db.Column(db.String(2))
    AF = db.Column(db.Float)


    def __init__(self, Variant_id, location, Alleles, AF):
        self.Variant_id = Variant_id
        self.location = location 
        self.Alleles = Alleles
        self.AF = AF 


# TO CREATE A PRODUCT SCHEMA 

class VariantsSchema(ma.Schema):
    # these are the fields we want to show when we put in our get requests
    class Meta:
        fields = ("Variant_id", "location", "Alleles", "AF")

# we need to initialize our schema 

# IF YOU DONT DO STRICT=TRUE, THE TERMINAL WILL RAISE AND ERROR 
# but while trying to create the database, I realized that strict=True, produced an eroor 
Variant_schema = VariantsSchema()
# the only difference between line 52 and line 54 is one returns a list of schema, that is one returns a list of variants.
Variants_schema = VariantsSchema(many=True)

# Create a Variant resources 
# using the POST method which is basically SQL create 
@app.route("/Variants", methods=["POST"])
def add_product():
    Variant_id = request.json["Variant_id"]
    location = request.json["location"]
    Alleles = request.json["Alleles"]
    AF = request.json["AF"]

    # then we create an instant of the class Product, check line 27, variants that is either added by us or the user 
    new_variants = Variants(Variant_id, location, Alleles, AF)

    # then we take db.session.add and add our new products 
    db.session.add(new_variants)
    # to commit to our database 
    db.session.commit()

    return Variant_schema.jsonify(new_variants)

# GET ALL VARIANTS 
@app.route("/Variants", methods=["GET"])
def get_Variants():
    # this will get all the products for us, like select all statements, more a less a stored procedure from SQLAlchemy 
    all_Variants = Variants.query.all()
    #because we are dealing with more than one variant, we use variants_schema 
    result = Variants_schema.dump(all_Variants)
    return jsonify(result)

# getting a single product 
@app.route("/Variants/<Variant_id>", methods=["GET"])
def get_Variant(Variant_id):
    # to get one variant using the variant_id 
    Variant = Variants.query.get(Variant_id)
    #because we are dealing with more than one variant, we use variants_schema 
    return Variant_schema.jsonify(Variant)
# TO UPDATE PRODUCT 
@app.route("/Variants/<Variant_id>", methods=["PUT"])
def update_product(Variant_id):
    # we need to first fetch the Variant 
    Variant = Variants.query.get(Variant_id)

    Variant_id = request.json["Variant_id"]
    location = request.json["location"]
    Alleles = request.json["Alleles"]
    AF = request.json["AF"]
   
    # to get the new update 
    Variant.location = location 
    Variant.Alleles = Alleles
    Variant.AF = AF

    # to commit to our database 
    db.session.commit()

    return Variant_schema.jsonify(Variant)

# to delete variants 
@app.route("/Variants/<Variant_id>", methods=["DELETE"])
def delete_product(Variant_id):
    Variant = Variants.query.get(Variant_id)
    db.session.delete(Variant)
    db.session.commit()

    return Variants_schema.jsonify(Variant)

# to run server 
if __name__ == "__main__":
    # calling debug = True is done because we are in developnent. 
    app.run(debug=True)
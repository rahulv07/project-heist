from flask import Flask, render_template
from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///charactersDB.db'
db = SQLAlchemy(app)
api = Api(app)
CORS(app)

#Declaring the Columns in the character database
class CharacterModel(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(255),nullable=True)
    alias = db.Column(db.String(255),nullable=True)
    occupation = db.Column(db.String(255),nullable=False)
    gender = db.Column(db.String(20),nullable=False)
    status = db.Column(db.String(10),nullable=True)
    romance = db.Column(db.String(255),nullable=True)
    family = db.Column(db.String(255),nullable=True)
    first_appearance = db.Column(db.String(20),nullable=False)
    last_appearance = db.Column(db.String(20),nullable=False)
    played_by = db.Column(db.String(255),nullable=True)
    image = db.Column(db.String(255),nullable=True)

    def __repr__(self):
        return f"Character(id={self.id},name={self.name},alias={self.alias},occupation={self.occupation},gender={self.gender},status={self.status},romance={self.romance},family={self.family},first_appearance={self.first_appearance},last_appearance={self.last_appearance},played_by={self.played_by},image={self.image})"

#Format of the JSON output
resource_fields = {
    'id': fields.Integer,
    'name':fields.String,
    'alias':fields.String,
    'occupation':fields.String,
    'gender':fields.String,
    'status':fields.String,
    'romance':fields.String,
    'family':fields.String,
    'first_appearance':fields.String,
    'last_appearance':fields.String,
    'played_by':fields.String,
    'image':fields.String,
}

class Characters(Resource):

    #When passed with id
    @marshal_with(resource_fields)
    def get(self,char_id):
        result = CharacterModel.query.filter_by(id=char_id).first()
        if not result:
            abort(404,message="Could not find a character with that id")
        return result


#Routes for API
api.add_resource(Characters,"/characters/<int:char_id>")

@app.errorhandler(404)
def invalid_route(e):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True)

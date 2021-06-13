from flask import Flask
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

character_put_args = reqparse.RequestParser()
character_put_args.add_argument("id",type=int,help="Character id is required",required=True)
character_put_args.add_argument("name",type=str)
character_put_args.add_argument("alias",type=str)
character_put_args.add_argument("occupation",type=str,help="Occupation is required",required=True)
character_put_args.add_argument("gender",type=str,help="Gender is required",required=True)
character_put_args.add_argument("status",type=str)
character_put_args.add_argument("romance",type=str)
character_put_args.add_argument("family",type=str)
character_put_args.add_argument("first_appearance",type=str,help="First Appearance is required",required=True)
character_put_args.add_argument("last_appearance",type=str,help="Last appearance is required",required=True)
character_put_args.add_argument("played_by",type=str)
character_put_args.add_argument("image",type=str)

character_update_args = reqparse.RequestParser()
character_update_args.add_argument("id",type=int)
character_update_args.add_argument("name",type=str)
character_update_args.add_argument("alias",type=str)
character_update_args.add_argument("occupation",type=str)
character_update_args.add_argument("gender",type=str)
character_update_args.add_argument("status",type=str)
character_update_args.add_argument("romance",type=str)
character_update_args.add_argument("family",type=str)
character_update_args.add_argument("first_appearance",type=str)
character_update_args.add_argument("last_appearance",type=str)
character_update_args.add_argument("played_by",type=str)
character_update_args.add_argument("image",type=str)

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


class EditCharacters(Resource):

    @marshal_with(resource_fields)
    def put(self,char_id):
        args = character_put_args.parse_args()
        result = CharacterModel.query.filter_by(id=char_id).first()
        if result:
            abort(409,message="Character already present")
        else:
            new_character = CharacterModel(id=char_id,name=args['name'],alias=args['alias'],occupation=args['occupation'],gender=args['gender'],status=args['status'],romance=args['romance'],family=args['family'],first_appearance=args['first_appearance'],last_appearance=args['last_appearance'],played_by=args['played_by'],image=args['image'])
            db.session.add(new_character)
            db.session.commit()
            return new_character,201

    @marshal_with(resource_fields)
    def patch(self,char_id):
        args = character_update_args.parse_args()
        result = CharacterModel.query.filter_by(id=char_id).first()
        if not result:
            abort(404,message="Character doesn't exist")
        else:
            if args['name']:
                result.name = args['name']
            if args['alias']:
                result.alias = args['alias']
            if args['occupation']:
                result.occupation = args['occupation']
            if args['gender']:
                result.gender = args['gender']
            if args['status']:
                result.status = args['status']
            if args['romance']:
                result.romance = args['romance']
            if args['family']:
                result.family = args['family']
            if args['first_appearance']:
                result.first_appearance = args['first_appearance']
            if args['last_appearance']:
                result.last_appearance = args['last_appearance']
            if args['played_by']:
                result.played_by = args['played_by']
            if args['image']:
                result.image = args['image']
            
            db.session.commit()
            return result

    def delete(self,char_id):
        result = CharacterModel.query.filter_by(id=char_id).first()
        if not result:
            abort(404,message="Character is not present with id: {char_id}")
        db.session.delete(result)
        db.session.commit()
        return '',204


#Routes for API
api.add_resource(Characters,"/characters/<int:char_id>")
api.add_resource(EditCharacters,"/editcharacters/<int:char_id>")


if __name__ == "__main__":
    app.run()

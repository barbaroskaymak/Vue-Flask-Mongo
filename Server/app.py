from flask_cors import CORS
from flask import Flask, jsonify 
from flask_mongoengine import MongoEngine
from flask_restful import Resource, Api,reqparse,inputs
from datetime import date


app = Flask(__name__) 
app.config['MONGO_URI'] = {
   'host':'mongodb://localhost:27017/deneme'
   
}

api = Api(app)
db = MongoEngine(app)
class TODOS(db.Document):
    title = db.StringField()
    description  = db.StringField()
    is_completed  = db.BooleanField(default=False)
    created_at  = db.DateTimeField(default=date.today())
    updated_at = db.DateTimeField()


# configuration
DEBUG = True
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

#Parser Zone
parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('description')
parser.add_argument('is_completed',type=inputs.boolean)

#Parser Zone End

def remove_book(book_id):
    todos = TODOS.objects.get_or_404(id=book_id)
    todos.delete()
    return True


class all_books(Resource):
    #Variable
    response_object = {'status': 'success'}

    def post(self):
        args = parser.parse_args()
        TODOS(title=args['title'],description=args['description'],is_completed=args['is_completed']).save()
        self.response_object['message'] = 'Todo added!'
        return jsonify(self.response_object)

    def get(self):
        todos = TODOS.objects.all()
        self.response_object['todos'] = todos
        return jsonify(self.response_object)


class single_book(Resource):
    #Variable
    response_object = {'status': 'success'}


    def put(self,book_id):
        args = parser.parse_args()
        todos = TODOS.objects.get_or_404(id=book_id)
        todos.title = args['title']
        todos.description=args['description']
        todos.is_completed=args['is_completed']
        todos.updated_at=date.today()
        todos.save()
        self.response_object['message'] = 'Todo updated!'
        return jsonify(self.response_object)
    def delete(self,book_id):
        remove_book(book_id)
        self.response_object['message'] = 'Todo removed!'
        return jsonify(self.response_object)



#End-Point
TODOS(title="barbaros",description="kaymak",is_completed=False).save()
api.add_resource(all_books, '/todos')
api.add_resource(single_book, '/todos/<book_id>')

#End-Point End

if __name__ == '__main__':
    app.run()

from flask_restx import Api
from app.api.auth import api as auth_ns
from app.api.books import api as books_ns

api = Api(
    title='Online Library API',
    version='1.0',
    description='A REST API for managing an online library system',
    doc='/docs/'
)

api.add_namespace(auth_ns, path='/users')
api.add_namespace(books_ns, path='/books')

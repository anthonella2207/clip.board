from flask import Flask
from flask_cors import CORS
from authRoutes import auth_routes

app = Flask(__name__)
CORS(app)
app.register_blueprint(auth_routes, url_prefix='/auth')

@app.route('/')
def home():
    return "¡Welcome to our cinema web!"

if __name__ == '__main__':
    app.run(debug=True)
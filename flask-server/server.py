from flask import Flask
from flask_cors import CORS
from authRoutes import auth_routes
from seats_routes import seats_routes
from filter_routes import filter_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(seats_routes, url_prefix='/api')
app.register_blueprint(filter_bp, url_prefix='/filters')

@app.route('/')
def home():
    return "¡Welcome to our cinema web!"

if __name__ == '__main__':
    app.run(debug=True)
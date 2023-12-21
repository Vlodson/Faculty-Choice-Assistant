from flask import Flask
from flask_cors import CORS

from backend.server.endpoints.predef_queries import bp as predef_queries_bp
from backend.server.endpoints.natural_language import bp as llm_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(predef_queries_bp, url_prefix="/predef_queries")
app.register_blueprint(llm_bp, url_prefix="/chat")


def main():
    app.run(port=5001, debug=True)


if __name__ == "__main__":
    main()

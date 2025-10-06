from flask import Flask, jsonify
from metadata_providers.service import MetadataService


app = Flask(__name__)
metadata_service = MetadataService()


@app.route("/mother_candidates/<isbn>", methods=["GET"])
def get_mother_candidates_by_isbn(isbn):
    response = metadata_service.get_mother_candidates_by_isbn(isbn)
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

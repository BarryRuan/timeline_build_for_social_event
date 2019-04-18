import google_search
import request
from flask import Flask, make_response, redirect, url_for, jsonify, render_template



app = Flask(__name__)



@app.route("/<query>")
def search(query):
    status_code = 200
    info = google_search.google_search(query)
    is_left = True
    for data in info['results']:
        data['position'] = 'left' if is_left else 'right'
        is_left = not is_left
        
    return render_template("index.html", **info)
    # return jsonify(info), status_code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

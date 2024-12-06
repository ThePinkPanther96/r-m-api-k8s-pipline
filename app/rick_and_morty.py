from flask import Flask, jsonify, render_template, abort, send_file
import requests
import csv
import os
import datetime

app = Flask(__name__)

healthchecks = []

BASE_URL = 'https://rickandmortyapi.com/api/character/'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'characters.csv')


def save_results_to_csv(results):
    try:   
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Location', 'Image']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    except (FileNotFoundError, KeyError, PermissionError) as e:
        status_message("ERROR", f"Failed to download results to CSV: {e}", "500")
        abort(500)
    except Exception as e:
        status_message("ERROR", f"An unexpected error occurred: {e}", "500")
        abort(500)


def status_message(status, message, status_code):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    healthchecks.append({
        'Status': status,
        'Message': message,
        'Status code': status_code,
        'Timestamp': time
    }) 


def api_check():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        status_message("PASSED","API healthchecks passed successfully.","200")
    else:
        status_message("ERROR",f"Failed to get Rick and Morty API. {BASE_URL}","500")


def get_characters():
    params = {
        'species': 'Human',
        'status': 'Alive',
    }
    results = []
    url = BASE_URL
    api_check()
    try:
        while url:
            response = requests.get(url, params=params)
            if response.status_code == 500:
                abort(500)
            data = response.json()

            for character in data.get('results', []):
                origin_name = character['location']['name']
                if 'Earth' in origin_name:
                    results.append({
                        'Name': character['name'],
                        'Location': character['location']['name'],
                        'Image': character['image']
                    })

            url = data['info']['next']
            params = None 
    
    except Exception as e:
        status_message("ERROR", str(e), "500")
        abort(500)

    return results


@app.route('/characters', methods=['GET'])
def return_characters():
    characters = get_characters()
    status_message("PASSED","Characters page rendered successfully","200")
    return render_template('characters.html', characters=characters)


@app.route('/download', methods=['GET'])
def download_results():
    characters = get_characters()
    save_results_to_csv(characters)
    return send_file(CSV_FILE, as_attachment=True, download_name='characters.csv')


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
   return jsonify({'Health Checks': healthchecks}), 200


@app.errorhandler(404)
def not_found(error): 
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html'), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
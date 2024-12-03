from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'OK'}), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    base_url = "https://rickandmortyapi.com/api/character/"
    params = {
        'species': 'Human',
        'status': 'Alive',
    }
    results = []
    url = base_url

    while url:
        response = requests.get(url, params=params)
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
        params = None  # Parameters are already in the 'next' URL

    # Render the template with character data
    return render_template('characters.html', characters=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
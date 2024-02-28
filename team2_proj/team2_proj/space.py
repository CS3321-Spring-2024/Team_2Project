from quart import Quart, jsonify, request
# import request

app = Quart(__name__)

@app.route('/nasa')
async def get_nasa_data():
    nasa_api_url = 'https://api.nasa.gov/planetary/apod?api_key=YOUR_API_KEY'
    response = request.get(nasa_api_url)
    data = response.json()
    return jsonify(data)

@app.route('/wikipedia')
async def get_wikipedia_data():
    wikipedia_api_url = 'https://en.wikipedia.org/api/rest_v1/page/summary/Python_(programming_language)'
    response = request.get(wikipedia_api_url)
    data = response.json()
    return jsonify(data)


if __name__ == '__main__':
    app.run()
    @app.route('/spacefact/<keyword>')
    async def get_space_fact(keyword):
        nasa_api_url = f'https://api.nasa.gov/planetary/apod?api_key=YOUR_API_KEY&search={keyword}'
        response = request.get(nasa_api_url)
        data = response.json()
        if 'error' in data:
            return jsonify({'error': 'No space fact found'})
        return jsonify(data)

    @app.route('/wikipedia/<keyword>')
    async def get_wikipedia_data(keyword):
        wikipedia_api_url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{keyword}'
        response = request.get(wikipedia_api_url)
        data = response.json()
        if 'title' not in data:
            return jsonify({'error': 'No Wikipedia page found'})
        return jsonify(data)
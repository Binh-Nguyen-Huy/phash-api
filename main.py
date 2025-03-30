from flask import Flask, request, jsonify
from PIL import Image
import imagehash
import requests
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Perceptual Hash API is running."

@app.route('/phash', methods=['GET'])
def phash():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing image URL'}), 400
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        hash_str = str(imagehash.phash(image))
        return jsonify({'hash': hash_str})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Let Render assign the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

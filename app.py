from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'status': 'Railway Backend is running!'})

@app.route('/get-subtitle', methods=['POST'])
def get_subtitle():
    try:
        data = request.get_json()
        video_id = data.get('videoId')
        
        if not video_id:
            return jsonify({'success': False, 'error': 'Video ID yok'}), 400
        
        # Türkçe altyazı çek
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['tr'])
        
        # Metni birleştir
        full_text = ' '.join([item['text'] for item in transcript])
        
        return jsonify({'success': True, 'subtitle': full_text})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

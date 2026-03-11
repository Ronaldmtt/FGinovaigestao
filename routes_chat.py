import json
from flask import Blueprint, request, jsonify, Response, render_template, stream_with_context
from flask_login import login_required, current_user
from ai_copilot import chat_stream

# Create a Blueprint for chat-related routes
chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/api/chat/message', methods=['POST'])
@login_required
def chat_message():
    """Endpoint for the AI Copilot chat that returns an SSE stream."""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Mensagem não fornecida"}), 400
        
    user_message = data['message']
    
    response = Response(
        stream_with_context(chat_stream(current_user.id, user_message)),
        mimetype='text/event-stream'
    )
    response.headers['X-Accel-Buffering'] = 'no'
    response.headers['Cache-Control'] = 'no-cache, no-transform'
    response.headers['Connection'] = 'keep-alive'
    return response

@chat_bp.route('/ia-hub')
@login_required
def ia_hub():
    """A tela principal, full-screen, do Assistente Virtual / Hub de IA."""
    return render_template('ai_hub.html')

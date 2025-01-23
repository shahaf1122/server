import os
from flask import Flask, request, jsonify
import asyncio
from pyrogram import Client

app = Flask(__name__)

api_id = os.getenv("API_ID")  # Telegram API ID
api_hash = os.getenv("API_HASH")  # Telegram API Hash
bot_token = os.getenv("BOT_TOKEN")  # Telegram Bot Token
session_name = "stremio_addon"
client = Client(session_name, api_id, api_hash)
bot_client = Client("bot", api_id, api_hash, bot_token=bot_token)

async def forward_file_to_bot(file_id, chat_id="@your_channel_or_group"):
    async with bot_client:
        # Forward the file to the bot
        forwarded_message = await bot_client.copy_message(
            chat_id="YOUR_BOT_USERNAME",  # Replace with your bot username
            from_chat_id=chat_id,
            message_id=file_id
        )
        # Generate a link for the forwarded file
        return f"https://t.me/YOUR_BOT_USERNAME?start={forwarded_message.id}"

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify([])

    # Search Telegram for files matching the query
    results = asyncio.run(search_telegram(query))
    return jsonify(results)

@app.route('/play', methods=['POST'])
def play():
    data = request.json
    file_id = data.get("file_id")
    if not file_id:
        return jsonify({"error": "file_id is required"}), 400

    # Forward the file to the bot and generate a link
    file_link = asyncio.run(forward_file_to_bot(file_id))
    return jsonify({"file_link": file_link})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, render_template, jsonify
import random
import requests
import time
import threading
from config import bot_url

app = Flask(__name__)

# Массив предсказаний
predictions = [
    "Скоро вас ждет удача!",
    "Будьте готовы к неожиданным событиям.",
]

last_update_id = None


@app.route('/')
def index():
    initial_prediction = random.choice(predictions)
    return render_template('index.html', prediction=initial_prediction)


@app.route('/new_prediction')
def new_prediction():
    new_prediction_ = random.choice(predictions)
    return jsonify(prediction=new_prediction_)


def get_updates():
    global last_update_id

    while True:
        response = requests.get(f'{bot_url}/getUpdates?offset={last_update_id}&timeout=100')
        updates = response.json().get('result', [])

        for update in updates:
            last_update_id = update['update_id'] + 1  # Обновляем ID последнего сообщения
            message = update.get('message', {}).get('text', '')
            chat_id = update['message']['chat']['id']

            if message:
                predictions.append(message)  # Добавляем сообщение в массив предсказаний
                send_message(chat_id, "Ваше сообщение добавлено в предсказания!")

        time.sleep(1)  # Задержка для предотвращения чрезмерного опроса


def send_message(chat_id, text):
    url = f'{bot_url}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, json=payload)


if __name__ == '__main__':
    threading.Thread(target=get_updates, daemon=True).start()

    app.run(debug=True)

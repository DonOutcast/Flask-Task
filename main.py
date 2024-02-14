import requests
from flask import Flask, jsonify, request

from database import database
from logger import logger
from service import User


app = Flask(__name__)


def fetch_weather(city):
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    api_key = "6ac5af39301f0668769c919db8839f4e"
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        temperature = data["main"]["temp"]
        return temperature
    except requests.RequestException as e:
        logger.error(f"Ошибка при получении данных о погоде: {e}")
        return None


@app.route("/update_balance", methods=["POST"])
def update_balance():
    user_id = request.json.get("user_id")
    city = request.json.get("city")
    temperature = fetch_weather(city)
    if temperature is None:
        return jsonify({"error": "Не удалось получить данные о погоде"}), 400

    user = User.fetch_user(database, user_id)
    if user is None:
        return jsonify({"error": "Пользователь не найден"}), 404

    new_balance = user.balance + temperature
    if new_balance < 0:
        return jsonify({"error": "Баланс не может быть отрицательным"}), 400

    user.update_balance(new_balance)
    return jsonify({"message": "Баланс обновлен", "new_balance": new_balance}), 200

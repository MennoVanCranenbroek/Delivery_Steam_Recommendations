from flask import Flask, request
from flask_cors import CORS, cross_origin
from recommend import recommend
import pandas as pd

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def helloWorld():
  return "Hello, cross-origin-world!"

df = pd.read_csv("../data/clean_game_data.csv")

@app.route("/GetRecommendations", methods=["GET"])
@cross_origin()
def get_recommendations():
    titles = request.args.get("titles")
    recommendations = recommend(titles, df)
    return recommendations

@app.route('/GetRandomGames', methods=["GET"])
def Get_Games():
    games = pd.read_csv("../data/clean_game_data.csv")
    random_games = games["title"].sample(n=20).tolist()
    return {"games": random_games}

Flask.run(app)
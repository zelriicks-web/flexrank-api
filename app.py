from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

RIOT_API_KEY = "RGAPI-dce6597d-046f-44f3-9fe7-04e46c1ec52f"  # reemplaza con tu API Key
REGION = "las1"  # Latinoamérica Sur

@app.route("/flexrank/<summoner_name>")
def flex_rank(summoner_name):
    # 1️⃣ Obtener summonerId
    url_summoner = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    r = requests.get(url_summoner, headers={"X-Riot-Token": RIOT_API_KEY})
    if r.status_code != 200:
        return jsonify({"error": "Summoner no encontrado"}), 404

    summoner_id = r.json()["id"]

    # 2️⃣ Obtener ranked stats
    url_ranked = f"https://{REGION}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    r2 = requests.get(url_ranked, headers={"X-Riot-Token": RIOT_API_KEY})
    if r2.status_code != 200:
        return jsonify({"error": "No se pudieron obtener los rankings"}), 500

    # 3️⃣ Buscar Flex 5v5
    ranked_data = r2.json()
    flex = next((entry for entry in ranked_data if entry["queueType"] == "RANKED_FLEX_SR"), None)
    if not flex:
        return jsonify({"message": "No tiene rank Flex"}), 200

    # 4️⃣ Devolver datos
    return jsonify({
        "summoner": summoner_name,
        "tier": flex["tier"],
        "rank": flex["rank"],
        "leaguePoints": flex["leaguePoints"],
        "wins": flex["wins"],
        "losses": flex["losses"]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, jwt, datetime

app = Flask(__name__)
CORS(app)

SECRET = "thug4ff"
LOGGER = "https://severth.onrender.com/save"

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return jsonify(
        name="THUG4FF API PROXY",
        status="ONLINE"
    )

# =========================
# API PROXY GOM HẾT BOT
# =========================
@app.route("/api")
def api():
    t = request.args.get("type")
    url = None

    try:
        if t == "check_ban":
            uid = request.args.get("uid")
            url = f"https://free-fire-check-ban.vercel.app/ban-info?uid={uid}"

        elif t == "info":
            uid = request.args.get("uid")
            region = request.args.get("region")
            url = f"https://free-fire-info-api-red.vercel.app/accinfo?uid={uid}&region={region}"

        elif t == "nick":
            nickname = request.args.get("nickname")
            url = f"https://danger-search-nickname.vercel.app/name/?nickname={nickname}"

        elif t == "longbio_jwt":
            bio = request.args.get("bio")
            token = request.args.get("token")
            url = f"https://danger-long-bio.vercel.app/update_bio?bio={bio}&token={token}"

        elif t == "longbio_acc":
            bio = request.args.get("bio")
            access = request.args.get("access_token")
            url = f"https://danger-long-bio.vercel.app/update_bio?bio={bio}&access_token={access}"

        elif t == "longbio_up":
            bio = request.args.get("bio")
            uid = request.args.get("uid")
            pw = request.args.get("password")
            url = f"https://danger-long-bio.vercel.app/update_bio?bio={bio}&uid={uid}&password={pw}"

        elif t == "join_guild":
            gid = request.args.get("guild_id")
            uid = request.args.get("uid")
            pw = request.args.get("password")
            url = f"http://guild-info-danger.vercel.app/join?guild_id={gid}&uid={uid}&password={pw}"

        elif t == "leave_guild":
            gid = request.args.get("guild_id")
            uid = request.args.get("uid")
            pw = request.args.get("password")
            url = f"http://guild-info-danger.vercel.app/leave?guild_id={gid}&uid={uid}&password={pw}"

        else:
            return jsonify(error=True, msg="Unknown type")

        # ======================
        # CALL API GỐC
        # ======================
        r = requests.get(url, timeout=20)

        try:
            data = r.json()
        except:
            data = {"raw": r.text}

        # ======================
        # SEND LOG TO SERVER 2
        # ======================
        try:
            requests.post(
                LOGGER,
                json={
                    "type": t,
                    "params": request.args.to_dict(),
                    "result": data
                },
                timeout=3
            )
        except:
            pass  # không để logger làm crash api

        # ======================
        # TRẢ JSON GỐC
        # ======================
        return jsonify(data)

    except Exception as e:
        return jsonify(error=True, msg=str(e))


# =========================
# JWT API
# =========================
@app.route("/jwt")
def jwt_api():
    uid = request.args.get("uid")
    password = request.args.get("password")

    if not uid or not password:
        return jsonify(error=True, msg="missing uid/password")

    token = jwt.encode(
        {
            "uid": uid,
            "password": password,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
        },
        SECRET,
        algorithm="HS256"
    )

    return jsonify(
        uid=uid,
        server="VN",
        token=token
    )


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000))

    except Exception as e:
        return jsonify(error=True, msg=str(e))


# =========================
# JWT THUG (API GỐC)
# =========================
@app.route("/jwt")
def jwt_api():
    uid = request.args.get("uid")
    password = request.args.get("password")

    if not uid or not password:
        return jsonify(error=True, msg="missing uid/password")

    token = jwt.encode(
        {
            "uid": uid,
            "password": password,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
        },
        SECRET,
        algorithm="HS256"
    )

    return jsonify(
        uid=uid,
        server="VN",
        token=token
    )


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
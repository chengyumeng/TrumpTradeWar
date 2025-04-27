from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求，方便本地前端开发

# 假设数据结构如下（实际可接数据库）
# 每个榜单类型一个列表，元素为字典
personal_best = {}  # {user: score}
region_best = [
    {"name": "小王", "score": 14},
    {"name": "阿李", "score": 11},
    {"name": "小明", "score": 10},
    {"name": "小张", "score": 9},
    {"name": "小刘", "score": 8},
]
global_best = [
    {"name": "Trump2024", "score": 23, "region": "USA"},
    {"name": "Ivan", "score": 18, "region": "RU"},
    {"name": "Ravi", "score": 15, "region": "IN"},
    {"name": "Hans", "score": 13, "region": "DE"},
]

@app.route('/api/leaderboard/<board_type>', methods=['GET'])
def get_leaderboard(board_type):
    user = request.args.get('user', '你')
    # 获取榜单
    if board_type == 'personal':
        score = personal_best.get(user, 0)
        return jsonify({"user": user, "score": score})
    elif board_type == 'region':
        # region榜首位始终是自己
        score = personal_best.get(user, 0)
        region = [{"name": user, "score": score}] + region_best
        region_sorted = sorted(region, key=lambda x: x["score"], reverse=True)[:10]
        return jsonify(region_sorted)
    elif board_type == 'global':
        # global榜首位始终是自己
        score = personal_best.get(user, 0)
        global_with_user = [{"name": user, "score": score, "region": "CN"}] + global_best
        global_sorted = sorted(global_with_user, key=lambda x: x["score"], reverse=True)[:10]
        return jsonify(global_sorted)
    else:
        return jsonify({"error": "invalid board"}), 400

@app.route('/api/leaderboard/personal', methods=['POST'])
def update_personal():
    data = request.json
    user = data.get("user", "你")
    score = int(data.get("score", 0))
    if user not in personal_best or score > personal_best[user]:
        personal_best[user] = score
    return jsonify({"success": True, "score": personal_best[user]})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)
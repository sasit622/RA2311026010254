from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

# Local storage (acts like DB)
notifications = []

# ---------------- CREATE NOTIFICATION ----------------
@app.route('/api/notifications', methods=['POST'])
def create_notification():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    new_notification = {
        "id": str(uuid.uuid4()),
        "userId": data.get("userId"),
        "title": data.get("title"),
        "message": data.get("message"),
        "type": data.get("type"),
        "read": False,
        "createdAt": datetime.utcnow().isoformat()
    }

    notifications.append(new_notification)

    return jsonify({
        "message": "Notification created",
        "data": new_notification
    }), 201


# ---------------- GET USER NOTIFICATIONS ----------------
@app.route('/api/notifications/<user_id>', methods=['GET'])
def get_notifications(user_id):
    user_notifications = [n for n in notifications if n["userId"] == user_id]

    return jsonify({
        "notifications": user_notifications
    }), 200


# ---------------- MARK AS READ ----------------
@app.route('/api/notifications/<notif_id>/read', methods=['PUT'])
def mark_as_read(notif_id):
    for n in notifications:
        if n["id"] == notif_id:
            n["read"] = True
            return jsonify({"message": "Marked as read"}), 200

    return jsonify({"error": "Notification not found"}), 404


# ---------------- DELETE NOTIFICATION ----------------
@app.route('/api/notifications/<notif_id>', methods=['DELETE'])
def delete_notification(notif_id):
    global notifications
    notifications = [n for n in notifications if n["id"] != notif_id]

    return jsonify({"message": "Deleted successfully"}), 200


# ---------------- RUN SERVER ----------------
if __name__ == '__main__':
    app.run(debug=True)
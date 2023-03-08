from authentication import validate_user
from models import Notifications, Users
from flask import make_response, jsonify
from datetime import datetime
from firebase_admin import messaging as firebase_push_notifications
import firebase_admin


def fetch_notifications(token):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        notifications = Notifications.objects(
            reciever=resp.user_github,
            notif_read_status=False
        ).all()
        message = [i.to_mongo().to_dict() for i in notifications]
        for i in message:
            del i["_id"]
        status_code = 200
    except Exception:
        message = {"error": "NotificationFetchFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)


def mark_notifs_as_read(token, reset=False):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        if not reset:
            Notifications.objects(reciever=resp.user_github).update(
                set__notif_read_status=True
            )
        else:
            Notifications.objects(reciever=resp.user_github).update(
                set__notif_read_status=False
            )
        message = {"status": "MarkAsReadSuccessful"}
        status_code = 200
    except Exception:
        message = {"error": "MarkAsReadFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)


def post_notifications(token, notif_json):
    isAuthorized, resp = validate_user(token)
    if not isAuthorized:
        return resp
    try:
        try:
            firebase_app = firebase_admin.get_app()
        except:
            firebase_creds = firebase_admin.credentials.Certificate(
                "/home/ubuntu/defios-api/defios_firebase.json"
            )
            firebase_app = firebase_admin.initialize_app(firebase_creds)
        user = Users.objects(
            user_github=notif_json["user_github"]
        ).only("user_fb_uid").first()
        notif = Notifications(
            reciever=notif_json["user_github"],
            sender_id=resp.user_github,
            sender_name=resp.user_gh_name,
            sender_profile_pic=resp.user_profile_pic,
            notif_post_time=datetime.now(),
            notif_type=notif_json["notif_type"],
            notif_content=notif_json["notif_content"],
            notif_action_path=notif_json["notif_action_path"],
            notif_action_state_params=notif_json["notif_state"],
            notif_action_api_params=notif_json["notif_api_specs"]
        )
        fb_notif = firebase_push_notifications.Message(
            token=user.user_fb_uid,
            notification=firebase_push_notifications.Notification(
                title="New Notification", body=notif_json["notif_content"]
            ),
            webpush=firebase_push_notifications.WebpushConfig(
                notification=firebase_push_notifications.WebpushNotification(
                    title="New Notification", body=notif_json["notif_content"],
                    icon=resp.user_profile_pic
                )
            )
        )
        notif.save()
        response = firebase_push_notifications.send(fb_notif)
        message = {
            "message": "NotificationPostSuccess",
            "notif_id": response
        }
        status_code = 200
    except Exception:
        message = {"error": "NotificationPostFailed"}
        status_code = 400
    return make_response(jsonify(message), status_code)
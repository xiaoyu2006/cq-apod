"""Image of the day from NASA APOD API"""

import json
import urllib

from .common import cq_send_message, load_config


def is_outdated(new_date):
    content = ""
    try:
        f = open("last_image_date.txt", "r")
        content = f.read()
        f.close()
    except FileNotFoundError:
        f = open("last_image_date.txt", "w")
        f.write(new_date)
        f.close()
        return True
    if new_date == content:
        return False
    f = open("last_image_date.txt", "w")
    f.write(new_date)
    f.close()
    return True


def send_apod():
    config = load_config()

    print("Fetching image of the day...")
    content = urllib.request.urlopen(
        "https://api.nasa.gov/planetary/apod?api_key=" + config["API_KEY"]
    ).read()
    content_json = json.loads(content)
    print("Received ", content_json)

    if not is_outdated(content_json["date"]):
        print("No new image of the day")
        return
    print("New image of the day! " + content_json["date"])

    news_msg = "[CQ:at,qq=all] Astronomy Picture of the Day: " + content_json["date"]
    cq_send_message(config["CQ_API"], config["CQ_GROUP"], news_msg)
    cq_send_message(config["CQ_API"], config["CQ_GROUP"], content_json["title"])
    cq_send_message(config["CQ_API"], config["CQ_GROUP"], content_json["explanation"])
    image_msg = "[CQ:image,file=" + content_json["url"] + "]"
    cq_send_message(config["CQ_API"], config["CQ_GROUP"], image_msg)

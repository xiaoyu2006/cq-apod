from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone
import urllib.request
import json
import sys

def load_config():
    with open("config.json") as f:
        return json.load(f)

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

        
def cq_send_message(api, group, message):
    safe_msg = urllib.parse.quote(message)
    url = "http://" + api + "/send_group_msg?group_id=" + group + "&message=" + safe_msg
    print("Sending message to CQ: " + url)
    result = urllib.request.urlopen(url).read()
    print("Result: " + result.decode("utf-8"))

def image_of_the_day():
    config = load_config()

    print("Fetching image of the day...")
    content = urllib.request \
        .urlopen("https://api.nasa.gov/planetary/apod?api_key=" + config["API_KEY"]).read()
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

def send_sun():
    config = load_config()
    image_msg = "[CQ:image," \
                "file=https://sdo.gsfc.nasa.gov/assets/img/latest/latest_4096_0193.jpg," \
                "cache=0]"
    cq_send_message(config["CQ_API"], config["CQ_GROUP"], image_msg)

def main():
    args = sys.argv[1:]
    if args and args[0] == "test":
        image_of_the_day()
        send_sun()
        return
    sched = BlockingScheduler(timezone=timezone("Asia/Shanghai"))
    # every hour to ensure images delivered on time
    sched.add_job(image_of_the_day, 'cron', minute=0)
    sched.add_job(send_sun, 'cron', hour='0,6,12,18')
    sched.start()


if __name__ == "__main__":
    main()

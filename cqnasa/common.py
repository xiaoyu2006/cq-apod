import json
import urllib


def load_config():
    with open("config.json") as f:
        return json.load(f)


def cq_send_message(api, group, message):
    safe_msg = urllib.parse.quote(message)
    url = "http://" + api + "/send_group_msg?group_id=" + group + "&message=" + safe_msg
    print("Sending message to CQ: " + url)
    result = urllib.request.urlopen(url).read()
    print("Result: " + result.decode("utf-8"))


def cq_download_file(api, file_url):
    url = "http://" + api + "/download_file?url=" + file_url
    print("Downloading file from CQ: " + url)
    result = urllib.request.urlopen(url).read()
    print("Result: " + result.decode("utf-8"))
    result_json = json.loads(result)
    if result_json["status"] == "failed":
        return None
    return result_json["data"]["file"]

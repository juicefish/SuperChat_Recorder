'''
Author: hymmnos_snow
Last-Edited: 2020-11-16
For Yukihana Lamy
Happy Birth Day
'''

import requests
import re
import json
import xlwt

# global
title = ""
session = requests.Session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
basic_link = "https://www.youtube.com/live_chat_replay/get_live_chat_replay?continuation="
lengthSeconds = 0
process = 0
GUI = 0
# Duplication check
last_timestamp = 0
last_superchat = ""
# excel interact
file = ""
line = 1


# get the link for comment
def get_live_comment_link(url):
    global session, basic_linka, lengthSeconds, title
    start_link = "https://www.youtube.com/live_chat_replay?continuation="
    try:
        html = session.get(url, headers=headers).text
        continuation = re.findall('"continuation":"(.*?)"', html)[2]
    except:
        return "NotAvailable"
    lengthSeconds = int(re.findall('\"lengthSeconds\":\"(\d+)\"', html)[0])
    title = re.findall(r'\"title\":\"(\S+)\",\"l', html)[0]
    next_link = start_link + continuation + '&hidden=false&pbj=1'
    html = session.get(next_link, headers=headers).text
    extract_superchat(json.loads(html)[1]["response"])
    continuation = json.loads(html)[1]['response']["continuationContents"]["liveChatContinuation"]["continuations"][0][
        "liveChatReplayContinuationData"]["continuation"]
    next_link = basic_link + continuation + '&hidden=false&pbj=1'
    return next_link


# extract Superchat from the link
def extract_superchat(json_data):
    global last_timestamp, timestamp, last_superchat, line, process
    for each in json_data["continuationContents"]["liveChatContinuation"]["actions"]:
        timestamp = int(each["replayChatItemAction"]["videoOffsetTimeMsec"])
        if "addChatItemAction" in each["replayChatItemAction"]["actions"][0] and 'liveChatPaidMessageRenderer' in \
                each["replayChatItemAction"]["actions"][0]["addChatItemAction"]['item']:
            raw_info = each["replayChatItemAction"]["actions"][0]["addChatItemAction"]['item'][
                'liveChatPaidMessageRenderer']
            supporter = raw_info['authorName']['simpleText']
            amount = raw_info['purchaseAmountText']['simpleText']
            text = ""

            # check if the Superchat contains message
            if 'message' in raw_info:
                # get rid of customized emoji, replace it with □
                for item in raw_info['message']['runs']:
                    text += item.get('text', "□")
            else:
                text = ""
            time = raw_info["timestampText"]['simpleText']

            # check duplication
            if last_superchat != time + supporter + amount:
                last_timestamp = timestamp
                last_superchat = time + supporter + amount
                #print(timestamp//1000,"/",lengthSeconds)
                GUI.process(int(((timestamp//1000) / lengthSeconds) * 100))
                # print(time, "  ", supporter, "", amount, "\n", text)
                file.write(line, 0, time)
                file.write(line, 1, supporter)
                file.write(line, 2, amount)
                file.write(line, 3, text)
                line += 1

            else:
                print("### SKIP DUPLICATED ###", time, supporter, amount)


# keep getting continue link
def extracting_loop(url):
    jump_to = 0
    next_link = get_live_comment_link(url)
    # check if the comment record available
    if next_link == "NotAvailable":
        GUI.error()
        return 1
    while True:
        html = session.get(next_link, headers=headers).text
        if "continuationContents" not in json.loads(html)['response']:
            jump_to += 1
            if (timestamp // 1000) + jump_to >= lengthSeconds:
                return 0
            print("### JUMP TO ###", url + "&t=%ss" % str((timestamp // 1000) + jump_to))
            next_link = get_live_comment_link(url + "&t=%ss" % str((timestamp // 1000) + jump_to))
            continue
        json_response = json.loads(html)['response']["continuationContents"]["liveChatContinuation"]
        if "liveChatReplayContinuationData" in json_response["continuations"][0]:
            continuation = json_response["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
            next_link = basic_link + continuation + '&hidden=false&pbj=1'
            extract_superchat(json.loads(html)['response'])

        else:
            jump_to += 1
            if (timestamp // 1000) + jump_to >= lengthSeconds:
                return 0
            print("### JUMP TO ###", url + "&t=%ss" % str((timestamp // 1000) + jump_to))
            next_link = get_live_comment_link(url + "&t=%ss" % str((timestamp // 1000) + jump_to))


def start(url, directory, handle):
    # create file
    global file, GUI
    GUI = handle
    workbook = xlwt.Workbook(encoding='utf-8')
    file = workbook.add_sheet("Super-chat")
    # sheet title
    file.write(0, 0, "Time")
    file.write(0, 1, "Name")
    file.write(0, 2, "Amount")
    file.write(0, 3, "Message")
    file.write(0, 4, title)
    # execute and save
    if extracting_loop(url) ==0:
        GUI.process(100)
        workbook.save(directory)


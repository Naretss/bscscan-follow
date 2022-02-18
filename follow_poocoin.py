#!/usr/bin/python3
import re
import requests
import time
import telegram
import click
import os
import sys

TOKEN = ''
CHAT_ID = ''
CHAT_ID2 = ''
bot = telegram.Bot(token=TOKEN)

adress = [
]
temp_last = []

indexs = 0
round = []


def forever():
    global temp_last
    global indexs
    global round

    while 1:
        try:

            print("-----")
            print("นักลาก "+str(indexs)+" : "+adress[indexs])
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

            data = requests.get(
                'https://bscscan.com/address/'+adress[indexs], headers=headers)
            txhash = re.findall(
                "<a class='hash-tag text-truncate myFnExpandBox_searchVal' href='\S+'>", data.text)

            txhash = txhash[0].split("/")[2]
            txhash = txhash.split("'")[0]
            if(temp_last[indexs] != txhash):
                print(temp_last[indexs])

                if(round[indexs] != 0):
                    data = requests.get(
                        'https://bscscan.com/tx/'+txhash, headers=headers)

                    reg_str = "<span class='mr-1'><span data-toggle=(.*?)>(.*?)</span> </span>"
                    res = re.findall(reg_str, data.text)
                    token = re.findall(
                        "<a href='/token/\S+'>", data.text)
                    text_res = "นักลากเบอ " + \
                        str(indexs) + " tx : " + \
                        "https://bscscan.com/tx/"+txhash+"\n"

                    text_res = str(text_res + res[0][1]) + \
                        str(res[0][0].split("/")[1].split('"')[0])

                    text_res = text_res + " -> " + str(res[len(res)-1][1])+str(res[len(res)-1]
                                                                               [0].split("/")[1].split('"')[0])

                    text_res = text_res + "\n " + \
                        "https://poocoin.app/tokens/" + \
                        str(str(token[len(token)-1]).split("/")
                            [2].split("'")[0])+"\n*ยังบัดราคาอยู่นะ ดูจากca poocoin อีกที*"
                    print(text_res)
                    bot.sendMessage(chat_id=CHAT_ID, text=text_res)
                    bot.sendMessage(chat_id=CHAT_ID2, text=text_res)
                temp_last[indexs] = txhash
                round[indexs] = round[indexs]+1

            time.sleep(1)

        except Exception as e:
            time.sleep(5)
            print(e)
        finally:
            indexs = indexs+1
            if(indexs == len(adress)):
                indexs = 0
                time.sleep(10)
                click.clear()


if __name__ == '__main__':
    try:
        forever()
    except Exception as e:
        print(e)
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

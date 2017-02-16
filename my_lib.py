import requests
from fake_useragent import UserAgent
import tkinter
import os


def get_html(url, coding):
    ua = UserAgent()
    headers = {'user-agent': f'{ua.opera}'}
    r = requests.get(url, auth=('doom', '123456'), headers=headers)
    r.encoding = coding
    return r.text

def get_window_size():
    r = tkinter.Tk()
    return r.winfo_screenwidth(), r.winfo_screenheight()


def save_file(url, name):
    r = requests.get(url, stream=True)
    if os.path.exists('img'):
        with open(name, 'bw') as f:
            f.write(r.content)
    else:
        os.mkdir('img')
        with open(name, 'bw') as f:
            f.write(r.content)
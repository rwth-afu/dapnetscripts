#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
from Tools import Tools


class News:
    # alternate URL: https://hampager.de/api
    def __init__(self, username, password, host="http://44.149.166.27:8080"):  # DevSkim: ignore DS137138
        self.username, self.password, self.host = username, password, host

    def send(self, message, rubric, slot=0):
        # Sends message to DAPNET
        # preparing the post-message
        tool = Tools()
        text = tool.make7bitclean(message)
        text = text[:80]

        if slot != 0:
            post = {"rubricName": rubric, "text": text, "number": slot}
        else:
            post = {"rubricName": rubric, "text": text}

        # and sending it to DAPNET
        try:
            resp = requests.post(
                self.host + "/news/",
                json=post,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=10,
            )
            if resp.status_code != 201:
                print("Error: POST /news/ {} post: {}".format(resp.status_code, post))
            else:
                print("Success: POST /news/ {} post: {}".format(resp.status_code, post))
        except requests.exceptions.Timeout:
            print("Timed out")
        except Exception as ex:
            print("Unexpected error: " + str(ex))
            raise

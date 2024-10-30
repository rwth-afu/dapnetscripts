#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from Tools import Tools
from requests.auth import HTTPBasicAuth


class Call:
    # alternate URL: https://hampager.de/api
    def __init__(self, username, password, host="http://44.149.166.27:8080"):  # DevSkim: ignore DS137138
        self.username, self.password, self.host = username, password, host

    def send(self, message, callsignnames, transmittergroupnames, emergency=False):
        # Sends message to DAPNET
        # preparing the post-message
        tool = Tools()
        text = tool.make7bitclean(message)
        text = text[:80]

        for callsign in callsignnames:

            post = {
                "text": text,
                "callSignNames": [callsign],
                "transmitterGroupNames": transmittergroupnames,
                "emergency": emergency,
            }
            # and sending it to DAPNET
            try:
                resp = requests.post(
                    self.host + "/calls/",
                    json=post,
                    auth=HTTPBasicAuth(self.username, self.password),
                    timeout=10,
                )
                if resp.status_code != 201:
                    print("Error: POST /calls/ {} post: {}".format(resp.status_code, post))
                else:
                    print("Success: POST /calls/ {} post: {}".format(resp.status_code, post))
            except requests.exceptions.Timeout:
                print("Timed out")
            except Exception as ex:
                print("Unexpected error: " + str(ex))
                raise

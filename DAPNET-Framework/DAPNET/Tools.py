#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Tools:

    def __init__(self):
        self.data = []

    @staticmethod
    def make7bitclean(s):
        s = str(s)
        s = s.replace("ä", "{")
        s = s.replace("ö", "|")
        s = s.replace("ü", "}")
        s = s.replace("Ä", "[")
        s = s.replace("Ö", "\\")
        s = s.replace("Ü", "]")
        s = s.replace("ß", "~")
        return s

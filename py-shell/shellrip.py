#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

class Imediate(object):
    def __init__(self, command, output):
        self.command = command
        self.output = output

    def __call__ (self, *args):
        result = os.popen("%s %s" % (self.command, " ".join(args))).readlines()
        if not self.output:
            return result
        print("".join(result))
        return None

class Shell(object):
    def __init__(self, output=False):
        self._output = output
    def __getattr__(self, attr):
        return Imediate(attr, self._output)

S = Shell()
I = Shell(True)
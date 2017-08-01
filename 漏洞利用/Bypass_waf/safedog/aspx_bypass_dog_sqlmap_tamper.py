#!/usr/bin/env python

"""

developers (goubuli)

"""

import random

import string

from lib.core.enums import PRIORITY

priority = PRIORITY.LOW

def tamper(payload, **kwargs):

retVal = ""



if payload:

    for i in xrange(len(payload)):

        if payload[i].isspace():

            retVal += "/*0a**/"

        elif payload[i] == '#' or payload[i:i + 3] == '-- ':

            retVal += payload[i:]

            break

        else:

            retVal += payload[i]



return retVal
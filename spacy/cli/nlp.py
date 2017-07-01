# coding: utf8
from __future__ import unicode_literals

import platform
from pathlib import Path
import spacy

from ..compat import unicode_
from .. import about
from .. import util


def nlp(sntnc=""):
    # lets parse a static sentence
    #sntnc = "At this time tomorrow, we will see if a summer crush can last the pressures of a Chicago winter."
    #util.print_msg('Hello!  You are in the parse function.', 'Hello Title')
    
    # parse the sentence
    nlp = spacy.load('en')
    doc = nlp(sntnc)
    util.print_doc(doc)

# coding: utf8
from __future__ import unicode_literals

import platform
from pathlib import Path
import spacy

from ..compat import unicode_
from .. import about
from .. import util


def parse():
    # lets parse a static sentence
    sentence = "At this time tomorrow, we will see if a summer crush can last the pressures of a Chicago winter."
    #util.print_msg('Hello!  You are in the parse function.', 'Hello Title')
    
    # parse the sentence
    nlp = spacy.en.English()
    doc = nlp(sentence)
    util.print_msg(str(doc.ents), 'Entity Recognition')

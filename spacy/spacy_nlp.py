"""
Print part-of-speech tagged, true-cased, (very roughly) sentence-separated
text, with each "sentence" on a newline, and spaces between tokens. Supports
multi-processing.
"""
from __future__ import print_function, unicode_literals, division
import io
import logging
from os import path
import sys
import plac
import unicodecsv as csv
import spacy
from spacy.tokens.doc import Doc
from spacy.symbols import *
import codecs


# initialize global
nlp = spacy.load('en')
writer = csv.writer(sys.stdout.buffer, delimiter="\t", encoding="utf-8")

#private class
class Annot():
    """Represent an annotation with start and stop values"""
    def __init__(self, start, end, label):
        self.start = start;
        self.end = end;
        self.label = label

    def __str__(self):
        return  's=' + str(self.start) + ' e=' + str(self.end) + ' l=' + str(self.label)

#define functions
def get_np_iob(index, np4iob):
    if index in np4iob:
        ann = np4iob.get(index)
        if ann.start == ann.end:
            return 'S'
        elif ann.start == index:
            return 'B'
        elif index > ann.start and index < ann.end:
            return 'I'
        elif index == ann.end:
            return 'E'
        else:
            return 'O'
    else:
        return 'O'

def represent_word(word):
    text = word.text
    # True-case, i.e. try to normalize sentence-initial capitals.
    # Only do this if the lower-cased form is more probable.
    if text.istitle() \
    and is_sent_begin(word) \
    and word.prob < word.doc.vocab[text.lower()].prob:
        text = text.lower()
    return text + '|' + word.tag_


def is_sent_begin(word):
    # It'd be nice to have some heuristics like these in the library, for these
    # times where we don't care so much about accuracy of SBD, and we don't want
    # to parse
    if word.i == 0:
        return True
    elif word.i >= 2 and word.nbor(-1).text in ('.', '!', '?', '...'):
        return True
    else:
        return False

def print_doc(doc):
    """
    Print formatted document. 
    """
    np4iob = {}
    
    #add noun chunks in IOB format
    #looking for noun phrases
    np_labels = set([nsubj, nsubjpass, dobj, iobj, pobj]) # Probably others too


    #load dictionary with annotations
    for word in doc:
        if word.dep in np_labels:
            #yield word.subtree
            subtree_span = doc[word.left_edge.i : word.right_edge.i + 1]
            #if key not in np4iob

            a = Annot(word.left_edge.i, word.right_edge.i, 'NP')
            for s in range(word.left_edge.i, word.right_edge.i + 1):
                if s not in np4iob:
                    np4iob[s] = a
                    #print(word.text, '|', subtree_span.text, '|', subtree_span.root.text, '|', word.left_edge, '|', word.left_edge.i, '|', word.right_edge, '|', word.right_edge.i)


    # header
    #writer.writerow(['INDEX', 'START', 'TEXT', 'LEMMA', 'TAG', 'POS', 'ENTITY', 'HEAD IDX', DEP'])
    for word in doc:
        #writer.writerow((str(word.i), str(word.idx), word.text, word.lemma_, word.tag_, word.pos_, word.ent_type_, str(word.head.i), word.dep_))
        writer.writerow((str(word.i), str(word.idx), word.text, word.lemma_, word.tag_, word.pos_, word.ent_type_, word.ent_iob_, 
            get_np_iob(word.i, np4iob), str(word.head.i), word.dep_))
    # complete with a newline row
    writer.writerow('')


def parse(sntnc, tokenized):
    # if it's tokenized, split the string by space and convert to a list for input

    if tokenized:
        doc = Doc(nlp.vocab, words=sntnc.split(" "))
        nlp.tagger(doc)
        nlp.parser(doc)
        nlp.entity(doc)
    else:
        doc = nlp(sntnc)

    return print_doc(doc)

@plac.annotations(
    interactive_mode=("Runs in interactive mode", "flag", "i"),
    tokenized=("Indicates input is pre-tokenized and delimited space character","flag", "usrtokens")
)
def main(interactive_mode, tokenized):
    if interactive_mode:
        try:
            # instantiate stdin_stream that we may need depending on input_mode
            sentence = None
            stdin_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

            # loop until exited or killed
            while True:
                #if input_mode:
                    #sys.stderr.write("Before keyboard mode input")
                    #sys.stderr.flush()
                    #sentence = input('')
                #else:
                    # pauses until input with newline
                sentence = stdin_stream.readline().rstrip()
                    #sentence = sys.stdin.readline().rstrip()

                # now process the sentence
                parse(sentence, tokenized)
                # stdout buffer should be ready to go, so flush
                sys.stdout.flush()

        except KeyboardInterrupt:
            print('spaCy interrupted!')
    else:
        print("Interactive Mode not selected.")

if __name__ == '__main__':
    plac.call(main)


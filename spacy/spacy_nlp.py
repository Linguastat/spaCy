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
#import csv
import unicodecsv as csv
import spacy
import codecs

# initialize global
nlp = spacy.load('en')
writer = csv.writer(sys.stdout.buffer, delimiter="\t", encoding="utf-8")

def transform_texts(batch_id, input_, out_dir):
    out_loc = path.join(out_dir, '%d.txt' % batch_id)
    if path.exists(out_loc):
        return None
    print('Batch', batch_id)
    nlp = spacy.en.English(parser=False, entity=False)
    with io.open(out_loc, 'w', encoding='utf8') as file_:
        for text in input_:
            doc = nlp(text)
            file_.write(' '.join(represent_word(w) for w in doc if not w.is_space))
            file_.write('\n')


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
    # header
    #writer.writerow(['INDEX', 'START', 'TEXT', 'LEMMA', 'TAG', 'POS', 'ENTITY', 'HEAD IDX', DEP'])
    for word in doc:
        writer.writerow((str(word.i), str(word.idx), word.text, word.lemma_, word.tag_, word.pos_, word.ent_type_, str(word.head.i), word.dep_))
    # complete with a newline row
    writer.writerow('')

def parse(sntnc):
    doc = nlp(sntnc)
    return print_doc(doc)

@plac.annotations(
    interactive_mode=("Runs in interactive mode", "flag", "i")
    #input_mode=("Runs using keyboard input functionality","flag", "k")
)
def main(interactive_mode):
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
                parse(sentence)
                # stdout buffer should be ready to go, so flush
                sys.stdout.flush()

        except KeyboardInterrupt:
            print('spaCy interrupted!')
    else:
        print("Interactive Mode not selected.")

if __name__ == '__main__':
    plac.call(main)


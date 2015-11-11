'''

This file implements some classes to work with text summaries

'''

import nltk
from komlibs.textman.model import patterns

class TextSummary:
    def __init__(self, text):
        self._text=nltk.Text(group[0] for group in nltk.regexp_tokenize(text,patterns.ro_text_tokenization))
        self.num_lines=self._text.count('\n')
        self.num_words=len(self._text)
        self.word_frecuency=nltk.FreqDist(self._text)
        self.content_length=len(text)


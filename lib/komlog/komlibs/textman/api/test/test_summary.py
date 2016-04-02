import unittest
import uuid
from komlog.komlibs.textman.api import summary as summaryapi
from komlog.komlibs.textman.model import summary as summarymodel
from komlog.komfig import logger

class TextmanApiSummaryTest(unittest.TestCase):
    ''' komlibs.textman.api.summary tests '''

    def test_get_summary_from_text_success(self):
        ''' get_summary_from_text should return a TextSummary object '''
        text='This is a sample text with 24 words counting spaces but no numbers'
        summary=summaryapi.get_summary_from_text(text=text)
        self.assertTrue(isinstance(summary, summarymodel.TextSummary))
        self.assertEqual(summary.num_lines,0)
        self.assertEqual(summary.num_words,24)
        self.assertEqual(summary.content_length,len(text))
        self.assertEqual(summary.word_frecuency,{'This':1,'is':1,'a':1,'sample':1,'text':1,'with':1,'words':1,'counting':1,'spaces':1,' ':12,'but':1,'no':1,'numbers':1})

    def test_get_summary_from_text_success_non_string_text(self):
        ''' get_summary_from_text should return a TextSummary object even if text is not a string. The resulting object should have an empty string as content '''
        texts=[1212, uuid.uuid4(), {'a':'dict'},['a','list'],{'set'},('a','tuple',2112)]
        for text in texts:
            summary=summaryapi.get_summary_from_text(text=text)
            self.assertTrue(isinstance(summary, summarymodel.TextSummary))
            self.assertEqual(summary.num_lines,0)
            self.assertEqual(summary.num_words,0)
            self.assertEqual(summary.content_length,0)
            self.assertEqual(summary.word_frecuency,{})



'''

This file implements functions to generate text summaries

'''

from komlog.komlibs.textman.model import summary

def get_summary_from_text(text):
    try:
        return summary.TextSummary(text)
    except Exception:
        return summary.TextSummary('')



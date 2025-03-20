from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def summarize_text(text, language="english", sentences_count=3, bullet_points=False):
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    
    if bullet_points:
        return "\n- " + "\n- ".join([str(sentence) for sentence in summary])
    return " ".join([str(sentence) for sentence in summary])
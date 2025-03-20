from IPython.display import Javascript, display

from .tokenizer import tokenize
from .wordcount import wordcount
from .corpus import corpus
from .grams import grams
from .smoothing import smoothing
from .pos import pos
from .stopwords import stopwords
from .stemming import stemming

def print_codes(codes):
    codes = codes[::-1]

    for code in codes:
        js_code = f'''
        var cell = Jupyter.notebook.insert_cell_below('code');
        cell.set_text(`{code}`);
        '''
        display(Javascript(js_code))

def code(program):
    if program == "tokenize":
        codes = tokenize()
    elif program == "wordcount":
        codes = wordcount()
    elif program == "corpus":
        codes = corpus()
    elif program == "grams":
        codes = grams()
    elif program == "smoothing":
        codes = smoothing()
    elif program == "pos":
        codes = pos()
    elif program == "stopwords":
        codes = stopwords()
    elif program == "stemming":
        codes = stemming()
    else:
        codes = []

    print_codes(codes)


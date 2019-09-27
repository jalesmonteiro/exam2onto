import os
from os import listdir
from os.path import isfile, join

from wiktextract import parse_wiktionary

class WikitionaryTools:

    def __init__(self, local, termos):
        self._local = local
        self._wcbs = []
        self._termos = termos

    def word_cb(self, data):
        self._wcbs.append(data)

    def capture_cb(self, title, text):
        if str.lower(title) in self._termos:
            with open(os.path.join(self._local, 'data', title+'.txt'), 'w') as termo:
                termo.write(text)
            return True
        else:
            return False

    def _extrair_termos(self):
        ctx = parse_wiktionary(
            os.path.join(self._local, 'wiktionary.xml.bz2'),
            word_cb = self.word_cb,
            capture_cb = self.capture_cb,
            languages=["Portuguese", "Translingual"],
            translations=False,
            pronunciations=False,
            redirects=False)

    def _get_substantivos(self):
        lista = []
        arquivos = [f for f in listdir(os.path.join(self._local, 'data')) if isfile(join(os.path.join(self._local, 'data'), f))]
        total = len(arquivos)

        for nome in arquivos:
            palavra = nome[:-4]
            with open(os.path.join(self._local, 'data', nome)) as wtermo:
                try:
                    texto = wtermo.read()
                    if '==Substantivo==' in texto:
                        lista.append(palavra)
                except UnicodeDecodeError:
                    print('erro: ', palavra)

        return lista

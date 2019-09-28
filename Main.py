import os
from tkinter import *
from tkinter import ttk
from pprint import pprint
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from collections import Counter

from ExtratorDeTexto import ExtratorDeTexto
from WikitionaryTools import WikitionaryTools

class Janela:
    _palavras = ''

    def __init__(self, toplevel):
        toplevel.title("Pré-processamento")

        self._inputWidth = 60
        self._text = None
        self._palavras = None
        self._unicas = None
        self._ranqueadas = None

        self._configuracoes = {
            'arquivo': '',
        }

        self.tabControl = ttk.Notebook(toplevel)
        self.tab1 = Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Geral')
        self.tabControl.pack(expand=1, fill="both")

        # criando tab1

        self.monty = Frame(self.tab1)
        self.monty.grid(column=0, row=0, padx=8, pady=4)

        self.frame1 = Frame(self.monty)
        self.frame1.grid(column=0, row=0, padx=8, pady=4, sticky='W E')

        Label(self.frame1, text="Diretório:").grid(column=0, row=0, sticky='W')

        self.local = StringVar()
        self.localInput = Entry(self.frame1, width=self._inputWidth, textvariable=self.local)
        self.localInput.grid(column=1, row=0)
        self.localInput.focus()

        self.btnExtrair = Button(self.frame1, text="Gerar termos", command=self.processar)
        self.btnExtrair.grid(column=0, row=2, sticky='W')

        self.local.set('/home/jales/Desenvolvimento/Workspaces/PycharmProjects/Mestrado/teste/')

    def processar(self):
        print('Processo iniciado.')
        self.verificar_pastas()
        self.extrair()
        self.unir()
        self.tokenizar()
        self.limpar()
        self.ranquear()
        self.wiki()
        print('Processo concluído.')

    def verificar_pastas(self):
        print('Verificando pastas.')
        if self.local.get()[-1:] != os.sep:
            self.local.set(self.local.get()+ os.sep)

        if not os.path.isdir( os.path.join(self.local.get(), 'provas') ):
            print('Pasta de provas não encontrada.')

        elif not os.path.isdir( os.path.join(self.local.get(), 'textos') ):
            os.mkdir( os.path.join(self.local.get(), 'textos') )

    def getNomes(self):
        arquivos = []
        arquivos = os.listdir(os.path.join(self.local.get(), 'provas'))
        arquivos.sort()
        return arquivos

    def extrair(self):
        self._arquivos = self.getNomes()
        extrator = ExtratorDeTexto()

        for nome in self._arquivos:
            print("Extraindo ", nome)
            with open(os.path.join(self.local.get(), 'provas', nome), 'rb') as file:
                with open(os.path.join(self.local.get(), 'textos', nome[:-4]+'.txt'), 'w') as out:
                    out.write(extrator.extrair(file))

    def unir(self):
        print('Unindo arquivos.')
        arquivos = os.listdir(os.path.join(self.local.get(), 'textos'))
        with open(os.path.join(self.local.get(), '1-todas.txt'), 'w') as todas:
            for nome in arquivos:
                with open(os.path.join(self.local.get(), 'textos', nome)) as prova:
                    for linha in prova:
                        todas.write(linha)

    def get_texto(self):
        texto = ''

        with open(os.path.join(self.local.get(), '1-todas.txt')) as file:
            texto = file.read().lower()

        return texto

    def tokenizar(self):
        print('Tokenizando.')
        with open(os.path.join(self.local.get(), '2-tokens.txt'), 'w') as out:
            self._palavras = word_tokenize(self.get_texto())
            for palavra in self._palavras:
                out.write(palavra+"\n")

    def limpar(self):
        print('Limpando.')
        with open(os.path.join(self.local.get(), '3-limpo.txt'), 'w') as out:
            stop_words = set(stopwords.words('portuguese') + list(punctuation))
            palavras = [line.rstrip('\n') for line in open(os.path.join(self.local.get(), '2-tokens.txt'), 'r')]
            palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stop_words]

            for palavra in palavras_sem_stopwords:
                if not os.sep in palavra:
                    out.write(palavra+'\n')

    def ranquear(self):
        print('Ranqueando.')
        with open(os.path.join(self.local.get(), '4-rank.txt'), 'w') as arquivo:
            cnt = Counter()
            palavras = [line.rstrip('\n') for line in open(os.path.join(self.local.get(), '3-limpo.txt'), 'r')]
            for palavra in palavras:
                cnt[palavra] += 1
            self._ranqueadas = sorted(cnt.items(), reverse=True, key=lambda tup: tup[1])
            for rank in self._ranqueadas:
                arquivo.write(rank[0]+'\n')

    def wiki(self):
        if os.path.isdir( os.path.join(self.local.get(), 'wiktionary') ):
            if os.path.isfile( os.path.join(self.local.get(), 'wiktionary', 'wiktionary.xml.bz2') ):
                termos = []

                print('Ferificando termos pelo wiktionary.')

                with open(os.path.join(self.local.get(), '4-rank.txt')) as rank:
                    for linha in rank:
                        termos.append(linha.rstrip('\n'))

                wt = WikitionaryTools(os.path.join(self.local.get(), 'wiktionary'), termos)

                if not os.path.isdir( os.path.join(self.local.get(), 'wiktionary', 'data') ):
                    os.mkdir( os.path.join(self.local.get(), 'wiktionary', 'data') )

                    wt._extrair_termos()

                substantivos = wt._get_substantivos()

                with open(os.path.join(self.local.get(), '5-wiktionary.txt'), 'w') as arquivo:
                    for palavra in substantivos:
                        arquivo.write(palavra+'\n')

        else:
            print('Pasta do wiktionary não encontrada.')

raiz = Tk()
Janela(raiz)
raiz.mainloop()

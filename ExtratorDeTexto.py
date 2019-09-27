import PyPDF2

class ExtratorDeTexto:

    def __init__(self):
        self.__texto = ''

    def __str__(self):
        print (self.__texto)

    def _extrair_usando_PyPDF2(self, arquivo):
        self.__texto = ''
        leitor_pdf = PyPDF2.PdfFileReader(arquivo)
        paginasQtd = leitor_pdf.getNumPages()

        for i in range(paginasQtd):
            pagina = leitor_pdf.getPage(i)
            try:
                self.__texto += pagina.extractText()+'\n'
            except Exception:
                pass

        return self.__texto

    def extrair(self, arquivo):
        self._extrair_usando_PyPDF2(arquivo)
        return self.__texto

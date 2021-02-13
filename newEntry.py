# Lucas Petersen
# 12 de Fevereiro de 2021

import tkinter as tk
import warnings
from pycadastros import formatCadastro


class EntryCPF:
    def __init__(self):
        pass


class EntryCNPJ:
    def __init__(self):
        pass


class EntryCadastro:
    def __init__(self, root, truebd='#74c454', falsebd='#c7271c', justify=tk.CENTER, borderwidth=3, mask=True,
                 update=True, changeBorder=True, highlightcolor='white', **kwargs):
        # TODO -- CONFIG -- criar opção de dar update no resultado ou não (callback)
        # TODO -- CONFIG -- criar opção de mudar a cor da borda ou não
        # TODO -- WIDGET -- criar opção de mask de cpf, mask de cnpj ou a atual, que serve pros dois
        # TODO -- VALIDAÇÃO -- criar opção de fill leading zeros ou não
        # TODO -- VALIDAÇÃO -- Autodetecção (validação por callback) não considera leading zeros ainda

        self.textvar = tk.StringVar()
        self.root = root
        self.borderwidth = borderwidth
        self.validate = 'key'
        self.vcmd = (self.root.register(self.validateNumbers), '%S')
        self.updateEntry = self.callback
        self.justify = justify
        self.truebd = truebd
        self.falsebd = falsebd
        self.mask = mask
        self.update = update
        self.changeBorder = changeBorder
        self.highlightcolor = highlightcolor

        self.mywidget = tk.Entry(self.root, validate=self.validate, vcmd=self.vcmd, justify=self.justify,
                                 highlightthickness=self.borderwidth, textvariable=self.textvar,
                                 highlightcolor=highlightcolor, **kwargs)

        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

        self.textvar.trace('w', lambda name, index, mode, sv=self.textvar: self.updateEntry())
        self.textvar.trace('w', lambda *args: self.characterLimit())

    def callback(self):
        self.mywidget.config(highlightcolor=self.falsebd, highlightbackground=self.falsebd)
        self.mywidget.config(selectbackground=self.mywidget.cget('highlightcolor'))
        cad = self.mywidget.get()
        if cad is not None:
            if len(self.mywidget.get().replace(',', '').replace('.', '').replace('/', '').replace('-', '')) >= 11:
                if self.mask:
                    cadmasked = self.get(mask=True)
                else:
                    cadmasked = self.get(mask=False)
                if cadmasked is not None:
                    self.textvar.set(cadmasked)
                    self.mywidget.config(vcmd=self.vcmd)
                    self.mywidget.icursor('end')

    def characterLimit(self):
        lchars = list(str(self.mywidget.get()))
        for lchar in lchars:
            if lchar not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '/', '.']:
                lchars.remove(lchar)

        self.textvar.set(''.join(lchars))
        if len(self.mywidget.get()) > 14:
            self.textvar.set(self.mywidget.get()[:-1])

    # TODO -- DEBUG -- Entender pq essa função tá esse Warning
    def validateNumbers(self, n):
        if n in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '/', '-']:
            return True
        else:
            return False

    def get(self, mask=False, fill=True):
        if mask and not fill:
            warnings.warn("'fill' convertido para True por conta de 'mask' estar como True.")
            self.mywidget.config(highlightcolor=self.truebd, highlightbackground=self.truebd)
            self.mywidget.config(selectbackground=self.mywidget.cget('highlightcolor'))

        cadastro = formatCadastro(self.mywidget.get())
        if cadastro is None:
            self.mywidget.config(highlightcolor=self.falsebd, highlightbackground=self.falsebd)
            return None

        else:
            self.mywidget.config(highlightcolor=self.truebd, highlightbackground=self.truebd)
            self.mywidget.config(selectbackground=self.mywidget.cget('highlightcolor'))
            if mask:
                return cadastro[2]

            else:
                if fill:
                    return cadastro[1]
                else:
                    return cadastro[0]

    def getType(self):
        return formatCadastro(self.mywidget.get())[3]

    def isValid(self):
        return formatCadastro(self.mywidget.get()) is not None

    def isCPF(self):
        try:
            cadastro = formatCadastro(self.mywidget.get())[3]
        except:
            return False
        return cadastro == 'CPF'

    def isCNPJ(self):
        try:
            cadastro = formatCadastro(self.mywidget.get())[3]
        except:
            return False
        return cadastro == 'CNPJ'

    def place(self, **kwargs):
        self.mywidget.place(**kwargs)

    def pack(self, **kwargs):
        self.mywidget.pack(**kwargs)

    def grid(self, **kwargs):
        self.mywidget.grid(**kwargs)


winW, winH = 600, 300
w, h = 270, 40
window = tk.Tk()
window.geometry(f'{winW}x{winH}')
window.configure(background='#051d60')

entry = EntryCadastro(window, font=('Century Gothic', '18'), bg='#051d60', borderwidth=1, relief=tk.FLAT, fg='white')
entry.place(x=(winW-w)//2, y=(winH-h)//2, h=43)

entry2 = EntryCadastro(window, font=('Roboto Medium', '14'), mask=False)
entry2.place(x=(winW-w)//2, y=(winH-h)//2+h+10, width=w, height=h)


def myf():
    print(entry.isValid())
    print(entry.isCPF())
    print(entry.isCNPJ())


def myf2():
    print(entry2.get(mask=True))


b = tk.Button(window, command=myf, text='entry de cima')
b.place(x=0, y=0, width=100, height=30)

b2 = tk.Button(window, command=myf2, text='entry de baixo')
b2.place(x=0, y=40, width=100, height=30)

window.mainloop()

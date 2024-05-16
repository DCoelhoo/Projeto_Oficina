import tkinter as tk
from tkinter import ttk, messagebox
from crud import CRUD


class FormMotas:
    '''Formulário para adicionar motas à BD'''

    def __init__(self, master, main_app):
        self.master = master
        self.main_app = main_app
        self.master.title("Adicionar Mota")

        self.crud = CRUD()

        self.button_voltar = ttk.Button(self.master, text="Voltar", command=self.open_main)
        self.button_voltar.pack()

        # Labels e Entries para matrícula, marca, modelo e ano
        self.label_matricula = tk.Label(master, text="Matrícula:")
        self.label_matricula.pack()
        self.entry_matricula = ttk.Entry(master)
        self.entry_matricula.pack()

        self.label_marca = tk.Label(master, text="Marca:")
        self.label_marca.pack()
        self.entry_marca = ttk.Entry(master)
        self.entry_marca.pack()

        self.label_modelo = tk.Label(master, text="Modelo:")
        self.label_modelo.pack()
        self.entry_modelo = ttk.Entry(master)
        self.entry_modelo.pack()

        self.label_ano = tk.Label(master, text="Ano:")
        self.label_ano.pack()
        self.entry_ano = ttk.Entry(master)
        self.entry_ano.pack()

        # Exemplo de botão para adicionar motas
        self.button_adicionar = ttk.Button(self.master, text="Adicionar Mota", command=self.adicionar_mota)
        self.button_adicionar.pack()

    def adicionar_mota(self):
        '''Adiciona as motas à tabela'''
        matricula = self.entry_matricula.get()
        marca = self.entry_marca.get()
        modelo = self.entry_modelo.get()
        ano = self.entry_ano.get()

        if matricula and marca and modelo and ano:
            self.crud.create_record('motas', ['matricula', 'marca', 'modelo', 'ano'], [matricula, marca, modelo, ano])
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
            self.entry_matricula.delete(0, 'end')
            self.entry_marca.delete(0, 'end')
            self.entry_modelo.delete(0, 'end')
            self.entry_ano.delete(0, 'end')
            self.open_main()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def open_main(self):
        # Limpa o conteúdo atual da janela
        for widget in self.master.winfo_children():
            widget.destroy()

        # Cria e exibe o formulário de motas na mesma janela, passando uma referência à classe App
        from main import App
        main = App(self.master)

from tkinter import *
from tkinter import messagebox
from crud import CRUD
import datetime

class NovaOcorrencia:
    def __init__(self, master, matricula):
        self.master = master
        self.matricula = matricula
        self.master.title("Nova Ocorrência")

        # Instância da classe CRUD
        self.crud = CRUD()

        # Criação dos componentes da interface
        Label(master, text="Matrícula:").grid(row=0, column=0)
        self.matricula_label = Label(master, text=matricula)
        self.matricula_label.grid(row=0, column=1)

        Label(master, text="Data:").grid(row=1, column=0)
        self.data_entry = Entry(master)
        self.data_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))  # Insere a data atual
        self.data_entry.grid(row=1, column=1)

        Label(master, text="KMs:").grid(row=2, column=0)
        self.km_entry = Entry(master)
        self.km_entry.grid(row=2, column=1)

        Label(master, text="Descrição:").grid(row=3, column=0)
        self.descricao_entry = Text(master, height=5, width=30)
        self.descricao_entry.grid(row=3, column=1)

        Label(master, text="Valor Total:").grid(row=4, column=0)
        self.valor_entry = Entry(master)
        self.valor_entry.grid(row=4, column=1)

        # Botão "Voltar"
        Button(master, text="Voltar", command=self.voltar).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Botão para salvar a nova ocorrência
        Button(master, text="Salvar", command=self.nova_ocorrencia).grid(row=5, column=1)

    def nova_ocorrencia(self):
        # Obter os dados do formulário
        data = self.data_entry.get()
        km = self.km_entry.get()
        descricao = self.descricao_entry.get("1.0", END)  # Obtém todo o texto da caixa de texto
        valor_total = self.valor_entry.get()

        # Validar os dados
        if not data or not km or not descricao or not valor_total:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        # Convertendo a string de KMs para inteiro
        try:
            km = int(km)
        except ValueError:
            messagebox.showerror("Erro", "O valor de KMs deve ser um número inteiro.")
            return

        # Convertendo a string de Valor Total para inteiro
        try:
            valor_total = float(valor_total)
        except ValueError:
            messagebox.showerror("Erro", "Algo não correu como esperado.")
            return

        # Inserir a nova ocorrência no banco de dados
        try:
            self.crud.create_record('ocorrencias', ['matricula', 'data', 'descricao', 'valor_total', 'km'],
                                    (self.matricula, data, descricao, valor_total, km))
            messagebox.showinfo("Sucesso", "Ocorrência criada com sucesso.")
            self.data_entry.delete(0, END)
            self.km_entry.delete(0, END)
            self.descricao_entry.delete("1.0", END)
            self.valor_entry.delete(0, END)
            self.voltar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar a ocorrência: {str(e)}")

    def voltar(self):
        # Limpa o conteúdo atual da janela
        for widget in self.master.winfo_children():
            widget.destroy()

        # Cria e exibe o formulário de motas na mesma janela, passando uma referência à classe App
        from tabela_ocorrencias import TabelaOcorrencias
        main = TabelaOcorrencias(self.master, self.matricula)
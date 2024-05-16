import tkinter as tk
from tkinter import ttk, messagebox
import database as db
from crud import CRUD

db.create_tables()
#db.populate_tables()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Minha Aplicação")
        
        # Instância da classe CRUD
        self.crud = CRUD()
        
        # Frame para conter a barra de pesquisa e o botão
        search_button_frame = tk.Frame(root)
        search_button_frame.pack(fill=tk.X)

        # Barra de pesquisa
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.search)
        self.search_entry = ttk.Entry(search_button_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill=tk.X, expand=True)  # Empacote a barra de pesquisa à esquerda

        # Botão para adicionar motas
        self.button_adicionar_mota = ttk.Button(search_button_frame, text="Adicionar Mota", command=self.open_form_motas)
        self.button_adicionar_mota.pack(side="right")  # Empacote o botão à direita

        # Frame para conter a tabela de motas
        tree_frame = tk.Frame(root)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Barra de rolagem vertical
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Árvore para exibir os dados da tabela
        self.tree = ttk.Treeview(tree_frame, columns=("Marca", "Modelo", "Nome"), yscrollcommand=scrollbar.set)
        self.tree.heading("#0", text="Matrícula")  # Coluna principal
        self.tree.heading("#1", text="Marca")      # Coluna 1
        self.tree.heading("#2", text="Modelo")     # Coluna 2
        self.tree.heading("#3", text="Cliente")    # Coluna 3
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configurar a barra de rolagem para rolar a árvore
        scrollbar.config(command=self.tree.yview)
        
        # Preencher a árvore com dados da tabela
        self.populate_tree()
        self.tree.bind("<Double-1>", self.open_tabela_ocorrencias)
    
    def populate_tree(self):
        # Limpar todos os itens na árvore
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Definindo as colunas para a consulta
        colunas = ['motas.matricula', 'motas.marca', 'motas.modelo', 'clientes.nome']
        join_clause = 'LEFT JOIN clientes ON motas.cliente_id = clientes.id'

        # Ler os registros da tabela motas com JOIN na tabela clientes
        motas = self.crud.read_records('motas', colunas, join=join_clause)
        
        if motas:
            for mota in motas:
                # Verificar se o nome do cliente está vazio
                nome_cliente = mota[3] if mota[3] else "Cliente Desconhecido"
                self.tree.insert("", "end", text=mota[0], values=(mota[1], mota[2], nome_cliente))

    def search(self, *args):
        # Obtenha o texto atual da barra de pesquisa
        matricula = self.search_var.get()

        # Limpe todos os itens na árvore
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Se o texto da barra de pesquisa estiver vazio, preencha a árvore com todos os registros
        if not matricula:
            self.populate_tree()
        else:
            # Realize a pesquisa na tabela apenas pela matrícula
            matricula_like = f"%{matricula}%"  # Adiciona wildcards para pesquisar em qualquer lugar da matrícula
            motas = self.crud.read_records('motas', ['matricula', 'marca', 'modelo'], condicoes="matricula LIKE ?", parametros=(matricula_like,))
            if motas:
                for mota in motas:
                    self.tree.insert("", "end", text=mota[0], values=(mota[1], mota[2]))


    def open_form_motas(self):
        # Limpa o conteúdo atual da janela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Cria e exibe o formulário de motas na mesma janela, passando uma referência à classe App
        from form_motas import FormMotas
        form_motas = FormMotas(self.root, self)

    def open_tabela_ocorrencias(self, event):
        # Obter a mota selecionada na árvore
        selected_item = self.tree.focus()
        matricula = self.tree.item(selected_item, "text")

        # Limpa o conteúdo atual da janela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Cria e exibe a página de tabela de ocorrências na mesma janela
        from tabela_ocorrencias import TabelaOcorrencias
        tabela_ocorrencias_page = TabelaOcorrencias(self.root, matricula)
        tabela_ocorrencias_page.populate_tree()  # Se necessário, atualize a árvore aqui




if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = App(root)
    root.mainloop()
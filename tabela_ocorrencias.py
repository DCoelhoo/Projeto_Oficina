import tkinter as tk
from tkinter import ttk, messagebox
from crud import CRUD

class TabelaOcorrencias:
    def __init__(self, master, matricula):
        self.master = master
        self.matricula = matricula
        self.master.title("Tabela ocorrências")

        # Instância da classe CRUD
        self.crud = CRUD()
        
        # Frame para conter a barra de pesquisa e o botão
        search_button_frame = tk.Frame(master)
        search_button_frame.pack(fill=tk.X)

        # Botão para voltar para o main
        self.button_adicionar_ocorrencia = ttk.Button(search_button_frame, text="Voltar", command=self.open_main)
        self.button_adicionar_ocorrencia.pack(side="left")  # Empacote o botão à direita

        # Botão para adicionar ocorrencias
        self.button_adicionar_ocorrencia = ttk.Button(search_button_frame, text="Adicionar Ocorrencia", command=self.open_new_ocorrencias)
        self.button_adicionar_ocorrencia.pack(side="right")  # Empacote o botão à direita
        
        #Botão para ver informações do cliente
        self.button_adicionar_ocorrencia = ttk.Button(search_button_frame, text="Informações Dono", command=self.open_info_cliente)
        self.button_adicionar_ocorrencia.pack(side="right")  # Empacote o botão à direita
        
        #Botão para ver informações do cliente
        self.button_adicionar_ocorrencia = ttk.Button(search_button_frame, text="Apagar Mota", command=self.apagar_mota)
        self.button_adicionar_ocorrencia.pack(side="right")  # Empacote o botão à direita        
        
        # Frame para conter a tabela de ocorrencias
        tree_frame = tk.Frame(master)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Barra de rolagem vertical
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Árvore para exibir os dados da tabela
        self.tree = ttk.Treeview(tree_frame, columns=("Data", "KM", "Valor"), yscrollcommand=scrollbar.set)
        self.tree.heading("#0", text="Data")        # Coluna principal
        self.tree.heading("#1", text="KM")      # Coluna 1
        self.tree.heading("#2", text="Valor")     # Coluna 2
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configurar a barra de rolagem para rolar a árvore
        scrollbar.config(command=self.tree.yview)
        
        # Preencher a árvore com dados da tabela
        self.populate_tree()
    
    def populate_tree(self):
        '''Alimenta a tabela'''

        # Limpar todos os items na árvore
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Definindo as colunas para a consulta
        colunas = ['data', 'km', 'valor_total']
        condicoes = f"matricula = '{self.matricula}'"
        ordenacao = "data DESC"

        # Ler os registros da tabela ocorrencias apenas para a mota selecionada
        ocorrencias = self.crud.read_records('ocorrencias', colunas, condicoes=condicoes, order_by=ordenacao)

        if ocorrencias:
            for ocorrencia in ocorrencias:
                # Insira os detalhes da ocorrência na árvore
                self.tree.insert("", "end", text=ocorrencia[0], values=(ocorrencia[1], ocorrencia[2]))

    def apagar_mota(self):
        # Solicitar confirmação do usuário
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja apagar esta mota?")
        if resposta:
            # O usuário confirmou a exclusão
            condicoes = f"matricula = '{self.matricula}'"  # Ajuste o nome do campo se necessário
            self.crud.delete_record('motas', condicoes)  # Chame o método para apagar a mota do banco de dados
            messagebox.showinfo("Ação Realizada", "Mota apagada com sucesso!")
            self.open_main()
        else:
            # O usuário cancelou a ação
            messagebox.showinfo("Ação Cancelada", "A exclusão da mota foi cancelada.")
        
    def open_new_ocorrencias(self):
        '''Cria novas ocorrencias '''
        
        # Limpa o conteúdo atual da janela
        for widget in self.master.winfo_children():
            widget.destroy()

        # Cria e exibe o formulário de motas na mesma janela, passando uma referência à classe App
        from ocorrencias import NovaOcorrencia
        info_clientes = NovaOcorrencia(self.master, self.matricula)

    def open_info_cliente(self):
        '''Vai para a página Info Clientes'''

        # Limpa o conteúdo atual da janela
        for widget in self.master.winfo_children():
            widget.destroy()

        # Cria e exibe o formulário de motas na mesma janela, passando uma referência à classe App
        from info_clientes import InfoCliente
        info_clientes = InfoCliente(self.master, self.matricula)


    def open_main(self):
        '''Volta para a página main.py'''

        # Limpa o conteúdo atual da janela
        for widget in self.master.winfo_children():
            widget.destroy()

        # Cria e exibe o formulário de motas na mesma janela, passando uma referência à classe App
        from main import App
        main = App(self.master)

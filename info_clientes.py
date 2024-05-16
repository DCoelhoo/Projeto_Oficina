from tkinter import *
from crud import CRUD

class InfoCliente:
    def __init__(self, master, matricula):
        self.master = master
        self.matricula = matricula  
        self.master.title("Informações do Cliente")

        # Instancia da classe CRUD
        self.crud = CRUD()

        # Criação dos componentes da interface
        Label(master, text="Nome:").grid(row=1, padx=10, pady=5, sticky="e")
        self.nome_entry = Entry(master)
        self.nome_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(master, text="NIF:").grid(row=2, padx=10, pady=5, sticky="e")
        self.nif_entry = Entry(master)
        self.nif_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(master, text="Morada:").grid(row=3, padx=10, pady=5, sticky="e")
        self.morada_entry = Entry(master)
        self.morada_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(master, text="Localidade:").grid(row=4, padx=10, pady=5, sticky="e")
        self.localidade_entry = Entry(master)
        self.localidade_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(master, text="Email:").grid(row=5, padx=10, pady=5, sticky="e")
        self.email_entry = Entry(master)
        self.email_entry.grid(row=5, column=1, padx=10, pady=5)

        Label(master, text="Código Postal:").grid(row=6, padx=10, pady=5, sticky="e")
        self.cpostal_entry = Entry(master)
        self.cpostal_entry.grid(row=6, column=1, padx=10, pady=5)

        Label(master, text="Telemóvel:").grid(row=7, padx=10, pady=5, sticky="e")
        self.tlm_entry = Entry(master)
        self.tlm_entry.grid(row=7, column=1, padx=10, pady=5)

        # Botão "Voltar"
        Button(master, text="Voltar", command=self.voltar).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Botão para atualizar ou criar cliente
        Button(master, text="Salvar", command=self.nova_cliente).grid(row=8, column=1, padx=10, pady=10)

        # Carregar dados automaticamente
        self.carregar_dados_cliente()

    def carregar_dados_cliente(self):
        colunas = ['c.nome', 'c.contribuinte', 'c.morada', 'c.localidade', 'c.email', 'c.codigo_postal', 'c.telemovel']
        join = 'INNER JOIN motas m ON m.cliente_id = c.id'
        condicoes = f'm.matricula = "{self.matricula}"'
        cliente = self.crud.read_records('clientes c', colunas, join, condicoes)

        if cliente:
            cliente = cliente[0]  # Como esperamos um único resultado
            self.nome_entry.insert(0, cliente[0])
            self.nif_entry.insert(0, cliente[1])
            self.morada_entry.insert(0, cliente[2])
            self.localidade_entry.insert(0, cliente[3])
            self.email_entry.insert(0, cliente[4])            
            self.cpostal_entry.insert(0, cliente[5])            
            self.tlm_entry.insert(0, cliente[6])            
            
        else:
            print("Nenhum cliente associado a esta matrícula.")

    def nova_cliente(self):
        nome = self.nome_entry.get()
        nif = self.nif_entry.get()
        morada = self.morada_entry.get()
        localidade = self.localidade_entry.get()
        email = self.email_entry.get()
        cpostal = self.cpostal_entry.get()
        tlm = self.tlm_entry.get()

        if nome and nif and morada and localidade and email and cpostal and tlm:
            # Verifica se o cliente já existe
            cliente_existente = self.crud.read_records('clientes', ['id'], condicoes=f'nif = {nif}')
            
            if cliente_existente:
                # Atualiza o cliente existente
                cliente_id = cliente_existente[0][0]
                update = {
                    'nome': nome,
                    'contribuinte': nif,
                    'morada': morada,
                    'localidade': localidade,
                    'email': email,
                    'codigo_postal': cpostal,
                    'telemovel': tlm
                }
                self.crud.update_record('clientes', update, f'id = {cliente_id}')
                print("Cliente atualizado com sucesso!")
            else:
                # Cria um novo cliente
                values = (nome, nif, morada, localidade, email, cpostal, tlm)
                cliente_id = self.crud.create_record('clientes', ['nome', 'contribuinte', 'morada', 'localidade', 'email', 'codigo_postal', 'telemovel'], values)
                print("Novo cliente criado com sucesso!")
                
                # Associa o novo cliente à mota
                self.crud.update_record('motas', {'cliente_id': cliente_id}, f'matricula = "{self.matricula}"')
                print("Cliente associado à matrícula com sucesso!")
        else:
            print("Por favor, preencha todos os campos.")


    def voltar(self):
        # Limpa o conteúdo atual da janela
        for widget in self.master.winfo_children():
            widget.destroy()

        # Cria e exibe o formulário de motas na mesma janela, passando uma referência à classe App
        from tabela_ocorrencias import TabelaOcorrencias
        main = TabelaOcorrencias(self.master, self.matricula)

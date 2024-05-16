import sqlite3

def get_connection():
    return sqlite3.connect('my_bd.db')

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Cria a tabela de clientes primeiro, já que Motas depende dela
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY, 
        nome TEXT,
        contribuinte INTEGER, 
        morada TEXT,
        localidade TEXT,
        email TEXT,
        codigo_postal TEXT,
        telemovel INTEGER)
    ''')

    # Cria a tabela de Motas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS motas (
        id INTEGER PRIMARY KEY, 
        matricula TEXT UNIQUE, 
        marca TEXT,
        modelo TEXT,
        ano INTEGER,
        cliente_id INTEGER,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id))
    ''')

    # Cria a tabela de Ocorrencias
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ocorrencias (
        id INTEGER PRIMARY KEY, 
        matricula TEXT, 
        data DATE,
        descricao TEXT,
        valor_total INTEGER,
        km INTEGER,
        FOREIGN KEY (matricula) REFERENCES motas(matricula))
    ''')

    conn.commit()
    conn.close()

def populate_tables():
    # Conectar ao banco de dados
    conn = sqlite3.connect('my_bd.db')

    try:
        cursor = conn.cursor()

        # Inserir dados na tabela de clientes
        clientes = [
            (1, 'João Silva', 123456789, 'Rua A, 10', 'Porto', 'joao.silva@email.com', '4000-123', 912345678),
            (2, 'Maria Joaquina', 987654321, 'Av Liberdade, 200', 'Lisboa', 'maria.joaquina@email.com', '1000-200', 921456789)
        ]
        cursor.executemany('''
            INSERT INTO clientes (id, nome, contribuinte, morada, localidade, email, codigo_postal, telemovel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', clientes)

        # Inserir dados na tabela de motas
        motas = [
            (1, 'AA-22-BB', 'Honda', 'CB500', 2020, 1),
            (2, 'BB-33-CC', 'Yamaha', 'YZF-R1', 2018, 2)
        ]
        cursor.executemany('''
            INSERT INTO motas (id, matricula, marca, modelo, ano, cliente_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', motas)

        # Inserir dados na tabela de ocorrências
        ocorrencias = [
            (1, 'AA-22-BB', '2023-04-02', "Revisao da Mota",200, 15000),
            (2, 'BB-33-CC', '2023-04-18', "Troca de Pneus",400, 25000),
            (3, 'AA-22-BB', '2022-04-07',"Troca de Pneus",200, 15000),
            (4, 'BB-33-CC', '2023-04-15', "Revisao da Mota",400, 25000),
        ]
        cursor.executemany('''
            INSERT INTO ocorrencias (id, matricula, data, descricao, valor_total, km)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ocorrencias)

        # Commit e fechar a conexão
        conn.commit()
    finally:
        conn.close()


# Agora chame create_tables para criar suas tabelas
create_tables()

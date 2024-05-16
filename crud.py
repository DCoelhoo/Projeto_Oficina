from database import get_connection

class CRUD:
    '''Agrupa as funções do CRUD'''
    
    def __init__(self):
        self.conn = get_connection()

    def create_record(self, tabela, coluna, valor):
        ''' Insere um registro em uma tabela específica. '''
        cursor = self.conn.cursor()
        placeholders = ', '.join('?' * len(valor))
        column_names = ', '.join(coluna)
        sql = f'INSERT INTO {tabela} ({column_names}) VALUES ({placeholders})'
        cursor.execute(sql, valor)
        self.conn.commit()

    def read_records(self, tabela, colunas, join=None, condicoes=None, order_by=None):
        ''' Lê registros de uma tabela com JOIN, condições opcionais e ordenação. '''
        cursor = self.conn.cursor()
        nome_colunas = ', '.join(colunas)
        sql = f'SELECT {nome_colunas} FROM {tabela}'
        if join:
            sql += f' {join}'
        if condicoes:
            sql += f' WHERE {condicoes}'
        if order_by:
            sql += f' ORDER BY {order_by}'
        cursor.execute(sql)
        records = cursor.fetchall()


    def update_record(self, tabela, update, condicoes):
        ''' Atualiza registros em uma tabela com base em condições especificadas. '''
        cursor = self.conn.cursor()
        update_stmt = ', '.join([f"{col} = ?" for col in update.keys()])
        sql = f'UPDATE {tabela} SET {update_stmt} WHERE {condicoes}'
        cursor.execute(sql, list(update.valor()))
        self.conn.commit()


    def delete_record(self, tabela, condicoes):
        ''' Remove registros de uma tabela com base em condições especificadas. '''
        cursor = self.conn.cursor()
        sql = f'DELETE FROM {tabela} WHERE {condicoes}'
        cursor.execute(sql)
        self.conn.commit()

    def close_connection(self):
        ''' Fecha a conexão com o banco de dados. '''
        self.conn.close()


import mysql.connector 
import datetime

conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'aluno',
        database = 'chatbot_pizzaria'
)

if conexao.is_connected():
    cursor = conexao.cursor()
    sql = 'INSERT INTO pedidos VALUES (%s,%s,%s,%s,)'
    valores = (
        '241128001','Uma pizza de mussarela','Rua do Tangomandapio, nº1, SBC', datetime.datetime.now().strftime("%y%m%d%H%M%S")
    )
    cursor.execute = (sql,valores)
    conexao.commit()
    cursor.close()
    conexao.close()
else:
    print('nok')
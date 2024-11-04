# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset

from rasa_sdk.events import SlotSet
import mysql.connector
import datetime

class Inserir_Pedidos(Action):
     def name(self) -> Text:
          return "action_salvar_pedido"
     
     def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         sabores = tracker.get_slot('pedido_pizza')
         qtde = tracker.get_slot('qtde_pizzas')
         endereco = tracker.get_slot('endereco_cliente')
         # Caso seja detectado mais sabores do que quantidades:
         while(len(sabores)>len(qtde)):
              qtde.append('uma')
         # Caso seja detectado mais quantidades do que sabores:
         # Caso sejam detectados mais qtdes do que sabores:
         while(len(sabores)<len(qtde)):
              qtde.pop(0)
         
         # Gerando o pedido do cliente baseado nos slots:
         pedido_completo = ""
         for sabor in range(len(sabores)):
               pedido_completo = pedido_completo + str(qtde[sabor]) + " pizza(s) de " + str(sabores[sabor])+" | " 
         # Conectando ao BD
         conexao = mysql.connector.connect(
                         host='localhost',
                         user='root',
                         password='aluno',
                         database='chatbot_pizzaria')
         if conexao.is_connected(): # Se funcionou a conexão            
               cursor = conexao.cursor()
               # Executar a consulta para obter o último item
               cursor.execute("SELECT * FROM pedidos ORDER BY cod_id DESC LIMIT 1")
               ultimo_item = cursor.fetchone() # Retorna os dados como uma tupla
               if ultimo_item is None: # Se nunca foi cadastrado um pedido
                    id_unico = str(datetime.datetime.now().strftime("%y%m%d")) + '001'
               elif(datetime.datetime.now().strftime("%y%m%d") == ultimo_item[3].strftime("%y%m%d")): 
                    # Se já foi cadastrado um pedido hoje:
                    id_unico = ultimo_item[0] + 1
               else:# Se não foi cadastrado um pedido hoje:
                    id_unico = str(datetime.datetime.now().strftime("%y%m%d")) + '001'
               # SQL de inserção
               sql = "INSERT INTO pedidos VALUES (%s, %s, %s, %s)"
               valores = (id_unico, 
                         pedido_completo, 
                         endereco, 
                         datetime.datetime.now().strftime("%y%m%d%H%M%S"))
               cursor.execute(sql, valores)# Executar a inserção
               conexao.commit()# Confirmar a transação
               # Fechando a conexão
               cursor.close()
               conexao.close()         

         # Salvando o valor no slot:
         return[SlotSet(key = "num_pedido_db",value = str(id_unico))]                  

class Reset_Todos_Slots(Action):

     def name(self) -> Text:
            return "action_resetar_slots"

     def run(self,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]):
         
         
         return [AllSlotsReset()]
     
# Não usado em aula, mas deixei aqui para lembrar como fazer o reset em cada slot.     
     
class Action_Sabor_Pizzas(Action):
     def name(self) -> Text:
            return "action_sabores_pizza"
     def run(self,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]):
         sabores = tracker.get_slot('pedido_pizza')
         qtde = tracker.get_slot('qtde_pizzas')
         endereco = tracker.get_slot('endereco_cliente')
         # Caso seja detectado mais sabores do que quantidades:
         while(len(sabores)>len(qtde)):
              qtde.append('uma')
         # Caso seja detectado mais quantidades do que sabores:
         qtde.reverse()
         while(len(sabores)<len(qtde)):
              qtde.pop()
         qtde.reverse()
         for sabor in range(len(sabores)):
              dispatcher.utter_message(text="\n - " + str(qtde[sabor]) + " pizza(s) de " + str(sabores[sabor]))
         dispatcher.utter_message(text='Além disso, o seu endereço é o '+str(endereco))
         dispatcher.utter_message(text='Favor confirmar com sim ou não.')
         return []     
      
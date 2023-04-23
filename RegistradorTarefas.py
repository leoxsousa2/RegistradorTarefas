import os
import datetime
import time

def tarefasExecutar():

    # Limpa o terminal 
    os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal
    print("Digite s para sair")
    print("     ")
    
    # lê o arquivo de tarefas se existir e mostra no terminal
    data_atual = datetime.datetime.now().strftime("%d-%m-%Y")
    nome_arquivo = f"tarefas do dia {data_atual}.txt"
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r") as arquivo:
            conteudo = arquivo.read()
        print(conteudo)

    # pede para o usuário informar a tarefa
    tarefa = input("Qual tarefa você vai realizar? ")

    # verifica se o usuário informou "s" e encerra o programa se for o caso
    if tarefa == "s":
        print("Programa encerrado.")
        time.sleep(2)
        exit()

    # gera o nome do arquivo com a data atual
    data_atual = datetime.datetime.now().strftime("%d-%m-%Y")
    nome_arquivo = f"tarefas do dia {data_atual}.txt"

    # verifica se o arquivo já existe, se não existir, cria um novo
    if not os.path.exists(nome_arquivo):
        with open(nome_arquivo, "w") as arquivo:
            arquivo.write("ID\tData\tHora\tTarefa\n")

    # adiciona a nova tarefa ao final do arquivo
    id_tarefa = sum(1 for _ in open(nome_arquivo))  # conta o número de linhas para gerar o ID da nova tarefa
    hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
    with open(nome_arquivo, "a") as arquivo:
        arquivo.write(f"{id_tarefa}\t{data_atual}\t{hora_atual}\t{tarefa}\n")

    print(f"Tarefa registrada com sucesso no arquivo {nome_arquivo}!")
    time.sleep(5)

    tarefasExecutar() # Inicia a função tarefasExecutar  # indica que o programa deve continuar em loop


tarefasExecutar() # Inicia a função tarefasExecutar
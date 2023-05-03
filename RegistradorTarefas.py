import os
import datetime
import time
import requests

global caminhoArquivo
caminhoArquivo = r"C:\Users\Acer\OneDrive\Documentos\tarefas" #O resto será preechido por strings

global verificador
verificador= "False"
dias_da_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']



def previsaoTempo(): #Quando chamar esse def o retorno sera a string PrevisaoTempo
    # Buscar credenciais - informacoes que nao podem estar no codigo principal
    with open('credenciaisAPI-OpenWeather.txt') as f:
        conteudo = f.readlines()
        cidade = conteudo[1].split(';')[0].strip()  #Ler segunda linha coluna 1 (separacao ";" )
        api_key = conteudo[1].split(';')[1].strip() #Ler segunda linha coluna 2 (separacao ";" )
    # Verifica conectividade com a internet
    try:
        requests.get('https://www.google.com/')
        net=1
    except requests.exceptions.ConnectionError:
        print('Erro: sem conexão com a internet')
        net=0
        
    if net == 1:
        # Previsão do tempo API OpenWeather
        url = f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()
        temperatura = data['main']['temp']
        tempo = data['weather'][0]['description']
        umidade = data['main']['humidity']
        PrevisaoTempo= f'Previsão do tempo para {cidade}: Temp: {data["main"]["temp"]}°C - Descrição: {data["weather"][0]["description"]} - Humidade: {data["main"]["humidity"]}%'
    if net == 0:
        PrevisaoTempo='Erro: Não tempo como verificar a previsão do tempo. Sem conexão com a internet'
    return PrevisaoTempo

def reniciar():
    global verificador
    verificador= "False"
    lerArquivoMostrar()

def lerArquivoMostrar():

    # Limpa o terminal 
    os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal
    print("     ")
    print("Digite s=sair ou d=modo discreto ou r=reiniciar")
    print("     ")
    
    # lê o arquivo de tarefas se existir e mostra no terminal
    data_atual = datetime.datetime.now().strftime("%a %d-%m-%Y")
    for i, dia in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
        data_atual = data_atual.replace(dia, dias_da_semana[i])
    nome_arquivo = caminhoArquivo + " de " + data_atual + ".txt"    #Ex: C:\Users\Acer\OneDrive\Documentos\tarefas de Dom 23-04-2023.txt
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r") as arquivo:
            conteudo = arquivo.read()
        print(conteudo)
    
    tarefasExecutar()



def tarefasExecutar():
    
    print("     ")

    # pede para o usuário informar a tarefa
    tarefa = input("Qual tarefa você vai realizar? ")

    if tarefa == "r":
        reniciar()

    # verifica se o usuário informou "s" e encerra o programa se for o caso
    if tarefa == "s":
        print("Programa encerrado.")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal
        exit()

    # verifica se o usuário informou "d" o programa para de mostrar informacoes do arquivo
    if tarefa == "d":
        os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal
        print(previsaoTempo())
        print("     ")
        print("modo discreto ativado")
        print("     ")
        time.sleep(2)
        global verificador
        verificador= "True"
        tarefasExecutar()
    
    if tarefa == "telaDark":
        os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal
        tarefa2 = input()
        if tarefa2 == "r":
            reniciar()

    if tarefa == "editArq":
        data_atual = datetime.datetime.now().strftime("%a %d-%m-%Y")
        for i, dia in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
            data_atual = data_atual.replace(dia, dias_da_semana[i])
        nome_arquivo = caminhoArquivo + " de " + data_atual + ".txt"    #Ex: C:\Users\Acer\OneDrive\Documentos\tarefas de Dom 23-04-2023.txt
        os.system("notepad.exe {}".format(nome_arquivo))
        reniciar()

    if tarefa == "abrirPasta":
        folder_path = r"C:\Users\Acer\OneDrive\Documentos\RegistradorTarefas"
        os.startfile(folder_path)
        reniciar()

    # gera o nome do arquivo com a data atual
    data_atual = datetime.datetime.now().strftime("%a %d-%m-%Y")
    for i, dia in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
        data_atual = data_atual.replace(dia, dias_da_semana[i])
    nome_arquivo = caminhoArquivo + " de " + data_atual + ".txt"    #Ex: C:\Users\Acer\OneDrive\Documentos\tarefas de Dom 23-04-2023.txt

    # verifica se o arquivo já existe, se não existir, cria um novo
    if not os.path.exists(nome_arquivo):
        with open(nome_arquivo, "w") as arquivo:
            
            with open(nome_arquivo, "r+") as arquivo:
                conteudo_arquivo = arquivo.read()
                arquivo.seek(0, 0) #cursor na primeira linha
                arquivo.write(f"{previsaoTempo()}\n{conteudo_arquivo}")
                arquivo.seek(0, 1) #cursor na segunda linha
                arquivo.write("\n") #Efeito de Enter
                arquivo.write("ID\tData\tHora\tTarefa\n")

    # adiciona a nova tarefa ao final do arquivo

    id_tarefa = sum(1 for _ in open(nome_arquivo)) -2  # conta o número de linhas para gerar o ID da nova tarefa
    hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
    with open(nome_arquivo, "a") as arquivo:
        arquivo.write(f"{id_tarefa}\t{data_atual}\t{hora_atual}\t{tarefa}\n")

    print("     ")
    print(f"Tarefa registrada com sucesso no arquivo {nome_arquivo}!")
    print("     ")
    time.sleep(5)


    if verificador == "True":
        os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal
        print(PrevisaoTempo)
        print("     ")
        print("modo discreto ativado")
        print("     ")
        time.sleep(2)
        tarefasExecutar()

    lerArquivoMostrar()


lerArquivoMostrar() # Inicia a função 
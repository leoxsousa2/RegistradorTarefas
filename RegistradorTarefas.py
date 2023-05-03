import os
import datetime
import time
import requests
import webbrowser
import openai
with open(r'C:\Users\Acer\OneDrive\Documentos\CredenciaisAPI\credenciaisAPI.txt') as f:
    conteudo = f.readlines()
    openai.api_key = conteudo[2].split(';')[1].strip() #Ler terceira linha coluna 2 (separacao ";" )
#"C:\Users\Acer\OneDrive\Documentos\CredenciaisAPI\credenciaisAPI.txt"

def perguntarTarefa():
    global tela   #pega a variavel que esta no inicio do codigo
    global tarefa
    os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal

    if tela == "Cheia" or tela == "Discreto":
        os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal
        print("     ")
        print("Digite s=sair//d=modo-discreto//r=reiniciar//dark=modoescuro//edit=editar-arquivoTXT//abriP=abrir-pasta-arquivo//utxt=atualizar-arquivoTXT//abrirPtese//abrirPsimu")
        print("     ")
    if tela == "Cheia":
        # lê o arquivo de tarefas se existir e mostra no terminal
        if os.path.exists(stringNomeArquivo()):
            with open(stringNomeArquivo(), "r") as arquivo:
                conteudo = arquivo.read()
            print(conteudo)
            print("     ")
        tarefa = input("Qual tarefa voce vai realizar? ")  # pede para o usuario informar a tarefa
    if tela == "Discretro":
        print(previsaoTempo())
        print("     ")
        print("modo discreto ativado")
        print("     ")
        time.sleep(2)
        print("     ")
        tarefa = input("Qual tarefa voce vai realizar? ")  # pede para o usuario informar a tarefa
    if tela == "Dark":
        os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal
        print("     ")
        tarefa = input()  # pede para o usuario informar a tarefa


    if tarefa == "r":
        reniciar()
    # verifica se o usuario informou "s" e encerra o programa se for o caso
    if tarefa == "s":
        print("Programa encerrado.")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal
        exit()
    # verifica se o usuario informou "d" o programa para de mostrar informacoes do arquivo
    if tarefa == "d":
        tela= "Discretro"
        perguntarTarefa()
    if tarefa == "dark":
        tela= "Dark"
        perguntarTarefa()
    if tarefa == "edit":
        print(stringNomeArquivo())
        os.system("notepad.exe {}".format(stringNomeArquivo()))
        reniciar()
    if tarefa == "gpt":
        url = 'https://chat.openai.com'
        webbrowser.open(url)
        reniciar()
    if tarefa == "gptcmd":
        openAIconfig()
    if tarefa == "gptsaldo":
        url = 'https://platform.openai.com/account/usage'
        webbrowser.open(url)
        reniciar()
    if tarefa == "abrirP":
        folder_path = r"C:\Users\Acer\OneDrive\Documentos\RegistradorTarefas"
        os.startfile(folder_path)
        reniciar()
    if tarefa == "utxt":
        os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal
        atualizarPrevisaoTempoArquivo()
    if tarefa == "abrirPtese":
        folder_path = r"C:\Users\Acer\Dropbox\Leo\3 - Dr-Pesquisa-WaterPhanton3D\0-Tese"
        os.startfile(folder_path)
        reniciar()
    if tarefa == "abrirPsimu":
        folder_path = r"C:\Users\Acer\OneDrive\Documentos\Simulacao-FOCAL"
        os.startfile(folder_path)
        reniciar()
    if tarefa == "links":
        url = 'https://leoxsousa2.github.io/website/dir/links.html'
        webbrowser.open(url)
        reniciar()
    tarefasExecutar()






def reniciar():
    global tela
    tela= "Cheia"
    perguntarTarefa()

def stringDataAtual(): 
    dias_da_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
    data_atual = datetime.datetime.now().strftime("%a %d-%m-%Y") 
    for i, dia in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
        data_atual = data_atual.replace(dia, dias_da_semana[i])
    return data_atual   

def stringNomeArquivo():
    caminhoArquivo = r"C:\Users\Acer\OneDrive\Documentos\tarefas" #O resto sera preechido por strings
    nome_arquivo = caminhoArquivo + " de " + stringDataAtual() + ".txt"    #Ex: C:\Users\Acer\OneDrive\Documentos\tarefas de Dom 23-04-2023.txt
    return nome_arquivo

def previsaoTempo(): #Quando chamar esse def o retorno sera a string PrevisaoTempo
    # Buscar credenciais - informacoes que nao podem estar no codigo principal
    with open(r'C:\Users\Acer\OneDrive\Documentos\CredenciaisAPI\credenciaisAPI.txt') as f:
        conteudo = f.readlines()
        cidade = conteudo[1].split(';')[0].strip()  #Ler segunda linha coluna 1 (separacao ";" )
        api_key = conteudo[1].split(';')[1].strip() #Ler segunda linha coluna 2 (separacao ";" )
        
    if verificarInternet() == 1:
        hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
        # Previsão do tempo API OpenWeather
        url = f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()
        temperatura = data['main']['temp']
        tempo = data['weather'][0]['description']
        umidade = data['main']['humidity']
        PrevisaoTempo= f'Previsao do tempo {cidade}: Temp: {data["main"]["temp"]}°C - Descricao: {data["weather"][0]["description"]} - Humidade: {data["main"]["humidity"]}% - Update: {hora_atual}'
    if verificarInternet() == 0:
        PrevisaoTempo='Erro: Nao tempo como verificar a previsao do tempo. Sem conexao com a internet'
    return PrevisaoTempo







def tarefasExecutar():
    # verifica se o arquivo ja existe, se nao existir, cria um novo
    if not os.path.exists(stringNomeArquivo()):
        with open(stringNomeArquivo(), "w") as arquivo:
            with open(stringNomeArquivo(), "r+") as arquivo:
                conteudo_arquivo = arquivo.read()
                arquivo.seek(0, 0) #cursor na primeira linha
                arquivo.write(f"{previsaoTempo()}\n{conteudo_arquivo}")
                arquivo.seek(0, 1) #cursor na segunda linha
                arquivo.write("\n") #Efeito de Enter
                arquivo.write("ID\tData\tHora\tTarefa\n")

    # adiciona a nova tarefa ao final do arquivo
    id_tarefa = sum(1 for _ in open(stringNomeArquivo())) -2  # conta o numero de linhas para gerar o ID da nova tarefa
    hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
    with open(stringNomeArquivo(), "a") as arquivo:
        arquivo.write(f"{id_tarefa}\t{stringDataAtual()}\t{hora_atual}\t{tarefa}\n")

    print("     ")
    print(f"Tarefa registrada com sucesso no arquivo {stringNomeArquivo()}!")
    print("     ")
    time.sleep(5)

    perguntarTarefa() # Inicia a funcao 

def atualizarPrevisaoTempoArquivo():
    with open(stringNomeArquivo(), 'r') as infoArquivo:
        linhas = infoArquivo.readlines()
        infoArquivo = ''.join(linhas[3:])

        with open(stringNomeArquivo(), "w") as arquivo:
            with open(stringNomeArquivo(), "r+") as arquivo:
                conteudo_arquivo = arquivo.read()
                arquivo.seek(0, 0) #cursor na primeira linha
                arquivo.write(f"{previsaoTempo()}\n{conteudo_arquivo}")
                arquivo.seek(0, 1) #cursor na segunda linha
                arquivo.write("\n") #Efeito de Enter
                arquivo.write("ID\tData\tHora\tTarefa\n")

    with open(stringNomeArquivo(), "a") as arquivo:
        arquivo.write(infoArquivo)
    perguntarTarefa()
 
def verificarInternet():
    # Verifica conectividade com a internet
    try:
        requests.get('https://www.google.com/')
        net=1
    except requests.exceptions.ConnectionError:
        net=0
    return net

def openAIconfig():
    os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal
    if verificarInternet() == 0:
        print("Erro: IA sem internet! ")
        time.sleep(5)
        reniciar()
    if verificarInternet() == 1:
        # Defina o modelo GPT que deseja usar
        model_engine = "text-davinci-002"
        user_input = "Converse comigo somente em português"
        # Envie uma consulta para o modelo GPT
        completions = openai.Completion.create(
            engine=model_engine,
            prompt=user_input,
            max_tokens=1,
            n=1,
            stop=None,
            temperature=0.5,
        )
        # Imprima a resposta do modelo GPT
        message = completions.choices[0].text.strip()
        #print(message)
        openAI()
    
def openAI():
    if verificarInternet() == 0:
        print("Erro: IA sem internet! ")
        time.sleep(5)
        reniciar()
    if verificarInternet() == 1:
        # Defina o modelo GPT que deseja usar
        model_engine = "text-davinci-002"
        user_input = input(">>>> ")
        os.system('cls' if os.name == 'nt' else 'clear')  # limpa a tela do terminal
        if user_input == "s" or user_input == "r":
            reniciar()
        # Envie uma consulta para o modelo GPT
        completions = openai.Completion.create(
            engine=model_engine,
            prompt=user_input,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Imprima a resposta do modelo GPT
        message = completions.choices[0].text.strip()
        print(user_input)
        print(" ")
        print(message)
        print(" ")
        print(" ")
        time.sleep(5)
        openAI()








tela= "Cheia"
perguntarTarefa() # Inicia a funcao 
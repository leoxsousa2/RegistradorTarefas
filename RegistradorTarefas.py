import os
import datetime
import time
import requests
import webbrowser
import openai    # pip install  openai       #chatGPT
import pyttsx3   # pip install  pyttsx3      #Usa a voz do windows
import platform
import json
from time import strftime
from sys import platform as _platform



if _platform == "linux" or _platform == "linux2":
    caminhoCredenciais= 'APIs/credenciaisAPI.md'
    caminhoArquivoSaida= 'Caderno//' #O resto sera preechido por strings
elif _platform == "win32" or _platform == "win64":
    caminhoCredenciais= fr'APIs\credenciaisAPI.md'
    caminhoArquivoSaida = fr'Caderno\\'  #duas barra representa uma. Se colocar so uma da erro



def ControleIDD():
    with open('APIs/Registro.md') as f:   
        conteudo = f.readlines()
        idd = int(conteudo[0].split(';')[0].strip())  
    return idd

def stringNomeArquivo():
    nome_arquivo = caminhoArquivoSaida + str(ControleIDD()) + '-tarefas' + " de " + stringDataAtual() + ".txt"    #Ex: C:\Users\Acer\OneDrive\Documentos\tarefas de Dom 23-04-2023.md
    return nome_arquivo


def perguntarTarefa():
    global tela                                                         #pega a variavel que esta no inicio do codigo
    global tarefa
    os.system('cls' if os.name == 'nt' else 'clear')                    # limpa a tela do terminal
    if tela == "Cheia" or tela == "Discreto":
        os.system('cls' if os.name == 'nt' else 'clear')                # limpa a tela do terminal
        print("     ")
        print("Digite s=sair//d=modo-discreto//r=reiniciar//dark=modoescuro//edit=editar-arquivomd//abriP=abrir-pasta-arquivo//umd=atualizar-arquivomd//abrirPtese//abrirPsimu")
        print("     ")
    if tela == "Cheia":
        if os.path.exists(stringNomeArquivo()):
            with open(stringNomeArquivo(), "r", encoding="latin-1") as arquivo:
                conteudo = arquivo.read()
            print(conteudo)
            print("     ")
        tarefa = input("Qual tarefa voce vai realizar? ")               # pede para o usuario informar a tarefa
    if tela == "Discreto":
        print(previsaoTempo())
        print("     ")
        print("modo discreto ativado")
        print("     ")
        #time.sleep(2)
        print("     ")
        tarefa = input("Qual tarefa voce vai realizar? ")               # pede para o usuario informar a tarefa
    if tela == "Dark":
        os.system('cls' if os.name == 'nt' else 'clear')                # limpa a tela do terminal
        print("     ")
        tarefa = input()                                                # pede para o usuario informar a tarefa

    if tarefa == "c":
        tela = "Cheia"
        perguntarTarefa()
    if tarefa == "r":
        reniciar()
    if tarefa == "s":
        print("     ")
        print("Programa encerrado.")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')                # limpa a tela do terminal
        exit()
    if tarefa == "d":
        tela= "Discreto"
        perguntarTarefa()
    if tarefa == "dk":
        tela= "Dark"
        perguntarTarefa()
    if tarefa == "edit":
        print(stringNomeArquivo())
        os.system("notepad.exe {}".format(stringNomeArquivo()))
        reniciar()
    if tarefa == "notas":
        os.startfile('notepad.exe')
        reniciar()
    if tarefa == "gpt":
        url = 'https://chat.openai.com'
        webbrowser.open(url)
        reniciar()
    if tarefa == "gpt2":
        url = 'https://chat.lmsys.org/'
        webbrowser.open(url)
        reniciar()
    if tarefa == "gptcmd":
        openAIconfig()
    if tarefa == "gptsaldo":
        url = 'https://platform.openai.com/account/usage'
        webbrowser.open(url)
        reniciar()
    if tarefa == "abrirP":
        folder_path = os.path.abspath(os.path.dirname(__file__))       #Este codigo informa o caminho em que o arquivo.py está 
        os.startfile(folder_path)
        reniciar()
    if tarefa == "umd":
        os.system('cls' if os.name == 'nt' else 'clear')                # limpa a tela do terminal
        atualizarPrevisaoTempoArquivo()
    if tarefa == "upy":
        os.system("RegistradorTarefas.py")
    if tarefa == "abrirPtese":
        folder_path = r"C:\Users\Acer\Dropbox\Leo\3 - Dr-Pesquisa-WaterPhanton3D\0-Tese"
        os.startfile(folder_path)
        reniciar()
    if tarefa == "abrirPsimu":
        folder_path = r"C:\Users\Acer\OneDrive\Documentos\Simulacao-FOCAL"
        os.startfile(folder_path)
        reniciar()
    if tarefa == "links":
        url = 'http://168.75.85.136/dir/links.html'
        webbrowser.open(url)
        reniciar()
    tarefasExecutar()

# --------------------------------------------->>> Def com retornos de strings


def stringDataAtual(): 
    dias_da_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
    data_atual = datetime.datetime.now().strftime("%a %d-%m-%Y") 
    for i, dia in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
        data_atual = data_atual.replace(dia, dias_da_semana[i])
    return data_atual   

def stringHoraAtual():
    #GetAPI = json.loads(requests.request("GET", 'https://timeapi.io/api/Time/current/zone?timeZone=America/Recife').text)
    #HoraMinuto = GetAPI['time']
    #Seg = GetAPI['seconds']
    #hora_atual = (str(HoraMinuto) + ':' + str(Seg))
    hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
    return hora_atual

def previsaoTempo():                                                #Quando chamar esse def o retorno sera a string PrevisaoTempo # Previsão do tempo API OpenWeather
    with open(caminhoCredenciais, encoding="latin-1") as f:                             # Buscar credenciais - informacoes que nao podem estar no codigo principal
        conteudo = f.readlines()
        cidade = conteudo[1].split(';')[0].strip()                  #Ler segunda linha coluna 1 (separacao ";" )
        api_key = conteudo[1].split(';')[1].strip()                 #Ler segunda linha coluna 2 (separacao ";" )
    if verificarInternet() == 1:
        hora_atual = stringHoraAtual()
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

def verificarInternet():                                            # Verifica conectividade com a internet
    try:
        requests.get('https://www.google.com/')
        net=1
    except requests.exceptions.ConnectionError:
        net=0
    return net

# --------------------------------------------->>> Def que somente executam funcções e depois retornam para o input

def reniciar():
    perguntarTarefa()

def tarefasExecutar():
    if not os.path.exists(stringNomeArquivo()):                    # verifica se o arquivo ja existe, se nao existir, cria um novo
        idd = ControleIDD() + 1
        with open('APIs/Registro.md', "w", encoding="latin-1") as arq:
            arq.write(str(idd) + "\n")
        with open(stringNomeArquivo(), "w", encoding="latin-1") as arquivo:
            with open(stringNomeArquivo(), "r+", encoding="latin-1") as arquivo:
                conteudo_arquivo = arquivo.read()
                arquivo.seek(0, 0)                                 #cursor na primeira linha
                arquivo.write(f"{previsaoTempo()}\n{conteudo_arquivo}")
                arquivo.seek(0, 1)                                 #cursor na segunda linha
                arquivo.write("\n")                                #Efeito de Enter
                arquivo.write("ID\tData\tHora\tTarefa\n")
    id_tarefa = sum(1 for _ in open(stringNomeArquivo(), encoding="latin-1")) -2       # conta o numero de linhas para gerar o ID da nova tarefa # adiciona a nova tarefa ao final do arquivo
    with open(stringNomeArquivo(), "a", encoding="latin-1") as arquivo:
        arquivo.write(f"{id_tarefa}\t{stringDataAtual()}\t{stringHoraAtual()}\t{tarefa}\n")
    print("     ")
    print(f"Tarefa registrada com sucesso no arquivo {stringNomeArquivo()}!")
    print("     ")
    time.sleep(5)
    perguntarTarefa()                                              # Inicia a funcao 

def atualizarPrevisaoTempoArquivo():
    with open(stringNomeArquivo(), 'r', encoding="latin-1") as infoArquivo:
        linhas = infoArquivo.readlines()
        infoArquivo = ''.join(linhas[3:])
        with open(stringNomeArquivo(), "w", encoding="latin-1") as arquivo:
            with open(stringNomeArquivo(), "r+", encoding="latin-1") as arquivo:
                conteudo_arquivo = arquivo.read()
                arquivo.seek(0, 0)                                 #cursor na primeira linha
                arquivo.write(f"{previsaoTempo()}\n{conteudo_arquivo}")
                arquivo.seek(0, 1)                                 #cursor na segunda linha
                arquivo.write("\n")                                #Efeito de Enter
                arquivo.write("ID\tData\tHora\tTarefa\n")
    with open(stringNomeArquivo(), "a", encoding="latin-1") as arquivo:
        arquivo.write(infoArquivo)
    perguntarTarefa()

def voz():
    engine = pyttsx3.init()   # Inicialize o objeto da biblioteca pyttsx3
    engine.setProperty('rate', 200)  # Defina a taxa de fala (opcional)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) # 10 é o índice da voz em português no meu computador
    # Texto a ser lido em português
    texto = "Você escreveu. " + user_input
    texto2 = "Resposta I. A."
    engine.say(texto)
    engine.runAndWait()
    time.sleep(1)
    engine.say(texto2)
    engine.runAndWait()
    engine.say(message)
    engine.runAndWait()   # Aguarde até que a fala seja concluída
    if VOZ  == 1:
        openAI()
def openAIconfig():
    os.system('cls' if os.name == 'nt' else 'clear')               # limpa a tela do terminal
    if verificarInternet() == 0:
        print("Erro: IA sem internet! ")
        time.sleep(5)
        reniciar()
    if verificarInternet() == 1:
        with open(caminhoCredenciais, encoding="latin-1") as f:
            conteudo = f.readlines()
            openai.api_key = conteudo[2].split(';')[1].strip()     #Ler terceira linha coluna 2 (separacao ";" )
        model_engine = "text-davinci-002"                          # Defina o modelo GPT que deseja usar
        user_input = "Você é um assistente educado e prestativo. Converse comigo somente em português"
        completions = openai.Completion.create(engine=model_engine, prompt=user_input, max_tokens=1, n=1, stop=None, temperature=0.5, )  # Envie uma consulta para o modelo GPT
        message = completions.choices[0].text.strip()
        os.system('cls' if os.name == 'nt' else 'clear')             # limpa a tela do terminal
        openAI()
    
def openAI():
    global message
    global VOZ
    global user_input
    if verificarInternet() == 0:
        print("Erro: IA sem internet! ")
        time.sleep(5)
        reniciar()
    if verificarInternet() == 1:
        with open(caminhoCredenciais, encoding="latin-1") as f:
            conteudo = f.readlines()
            openai.api_key = conteudo[2].split(';')[1].strip()       #Ler terceira linha coluna 2 (separacao ";" )
        model_engine = "text-davinci-002"                            # Defina o modelo GPT que deseja usar
        user_input = input(">>>> ")
        if user_input == "cls":    
            os.system('cls' if os.name == 'nt' else 'clear')             # limpa a tela do terminal
            openAI()
        if user_input == "s" or user_input == "r":
            reniciar()
        if user_input == "voz-on":
            VOZ = 1
            print("Modo voz ativado")
            print(" ")
            time.sleep(5)
            openAI()
        if user_input == "voz-off":
            VOZ = 0
            print("Modo voz desativado")
            print(" ")
            time.sleep(5)
            openAI()                                                                  # max_tokens=200 para economizar
        completions = openai.Completion.create( engine=model_engine, prompt=user_input, max_tokens=2000, n=1, stop=None, temperature=0.5, )  # Envie uma consulta para o modelo GPT
        message = completions.choices[0].text.strip()               # Imprima a resposta do modelo GPT
        #print(user_input)
        print(" ")
        print(message)
        print(" ")
        print(" ")
        if VOZ == 1:
            voz()
        openAI()

# --------------------------------------------->>> Depois de ler todo o codigo o programa executa o primeiro Def e determina uma variavel
VOZ = 0
tela= "Cheia"
perguntarTarefa()                                                   # Inicia a funcao 




# Converter arquivo python para programa .exe ((abra o cmd e coloque este codigo))
# pyinstaller RegistradorTarefas.py --onefile --noconsole
# pyinstaller RegistradorTarefas.py --onefile
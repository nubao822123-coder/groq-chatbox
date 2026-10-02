import json
import requests
import os
from colorama import init, Fore, Style
from pathlib import Path
from dotenv import load_dotenv

init(autoreset=True)
load_dotenv()

historico = []
contador = 1
API = ""
MODELO = "openai/gpt-oss-20b" # modelo mais util
NOME_PASTA = "conversas"
def criar_pasta(): 
    pasta = Path(NOME_PASTA)
    pasta.mkdir(exist_ok=True)


def carregar_api():
    global API
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            API = api_key
        else:
            raise ValueError("Chave GROQ_API_KEY não encontrada no arquivo .env")
    except Exception as e:
        print(Fore.RED + f"Erro ao carregar API: {e}")
        quit()
    except Exception as e:
        print(Fore.RED + f"Erro ao carregar API: {e}")
        quit()

while os.path.exists(os.path.join(NOME_PASTA, f"conversa_{contador}.json")):
    contador += 1
arquivo_atual = str(contador) 

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""[0;37m                                                     [0m
    [0;37m                                                     [0m
    [0;37m  [0;30;44m▀[0;37;44m▄▄▄▄▄▄▄[0;30;44m▀[0;37m     [0;30;44m▀[0;37;44m▄▄▄▄▄▄▄[0;30;44m▀[0;37m   [0;30;44m▀[0;37;44m▄▄▄▄▄▄▄[0;30;44m▀[0;37m     [0;30;44m▀[0;37;44m▄▄▄▄▄▄▄[0;30;44m▀[0;37m  [0m
    [0;37m [0;34m█[0;37;44m█▓█[0;34m█▀█[0;37;44m█▓█[0;34m█[0;37m   [0;34m█[0;37;44m█▓█[0;34m█▀█[0;37;44m█▓█[0;37m  [0;34m█[0;37;44m█▓█[0;34m█▀█[0;37;44m█▓█[0;34m█[0;37m   [0;34m█[0;37;44m█▓█[0;34m█▀█[0;37;44m█▓█[0;34m█[0;37m [0m
    [0;34m█[0;37;44m▓▒▓ [0;37m   [0;37;44m ▓▒▓[0;34m█[0;37m [0;34m█[0;37;44m▓▒▓ [0;34m▌[0;37m [0;34m▐[0;37;44m ▓▒[0;37m [0;34m█[0;37;44m▓▒▓ [0;37m   [0;37;44m ▓▒▓[0;34m█[0;37m [0;34m█[0;37;44m▓▒▓ [0;37m   [0;37;44m ▓▒▓[0;34m█[0m
    [0;34m█[0;37;44m▒░▒[0;34m▓[0;37m   [0;34m▓[0;37;44m▒░▒[0;34m█[0;37m [0;34m█[0;37;44m▒░▒[0;34m▓[0;37m       [0;34m█[0;37;44m▒░▒[0;34m▓[0;37m   [0;34m▓[0;37;44m▒░▒[0;34m█[0;37m [0;34m█[0;37;44m▒░▒[0;34m▓[0;37m   [0;34m▓[0;37;44m▒░▒[0;34m█[0m
    [0;34m█[0;37;44m░ ░[0;34m▓[0;37m   [0;34m▓[0;37;44m░ ░[0;34m█[0;37m [0;34m█[0;37;44m░ ░[0;34m▓[0;37m       [0;34m█[0;37;44m░ ░[0;34m▓[0;37m   [0;34m▓[0;37;44m░ ░[0;34m█[0;37m [0;34m█[0;37;44m░ ░[0;34m▓[0;37m   [0;34m▓[0;37;44m░ ░[0;34m█[0m
    [0;37m [0;34m█[0;34;44m [0;94;44m░▒ [0;34m▄[0;94;44m ▒░[0;34;44m [0;34m██[0;37m [0;34m██[0;34;44m [0;94;44m░░[0;37m        [0;34m█[0;34;44m [0;94;44m░▒ [0;34m▄[0;94;44m ▒░[0;34;44m [0;34m█[0;37m   [0;34m█[0;34;44m [0;94;44m░▒ [0;34m▄[0;94;44m ▒░[0;34;44m [0;34m██[0m
    [0;37m  [0;35m▀[0;35;44m▄▄▄[0;35m■[0;35;44m▄■[0;37;44m░[0;34m█[0;37;44m░[0;34m█[0;37m [0;35;44m▄▄[0;35m▀[0;35;44m▄▄[0;37m         [0;35m▀[0;35;44m▄▄▄[0;35m■[0;35;44m▄▄▄[0;35m▀[0;37m     [0;35m▀[0;35;44m▄▄▄[0;35m■[0;35;44m▄■[0;37;44m░[0;34m█[0;37;44m░[0;34m█[0m
    [0;37m    [0;34m▄▄[0;37m  [0;34m█[0;37;44m▒[0;34m█[0;37;44m▒[0;34m█[0;37m                                   [0;34m█[0;37;44m▒[0;34m█[0;37;44m▒[0;34m█[0m
    [0;37m  [0;34m▄[0;37;44m▄▀▀▄▄▄▓▄▀[0;34m█[0;37m                                   [0;34m█[0;37;44m▓▄▓[0;34m█[0m
    [0;37m   [0;34m▀[0;37m  [0;34m▀▀▀▀▀▀[0;37m                                    [0;34m▀▀▀▀▀[0m""")
    print(Fore.CYAN + "'Chatbox sem limites...'\n")
    print(Fore.CYAN + "Se quizer ajuda fale /ajuda para mostra a lista de comandos\n")
    print(Fore.CYAN + f"Modelo atual: {MODELO}\n")

def adicionar_mensagem(papel, texto):
    """Adiciona uma nova mensagem ao histórico."""
    historico.append({"role": papel, "content": texto})
    
def carregar_arquivo(nome):
    try:
        with open(f"{NOME_PASTA}/conversa_{arquivo_atual}.json", "r", encoding="utf-8") as arquivo:
            his = json.load(arquivo)
            print(f"Chat Carregado: {nome}")
            
            return his
            
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    
def salvar_mensagem():   
    with open(f"{NOME_PASTA}/conversa_{arquivo_atual}.json", "w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, indent=4, ensure_ascii=False)
def printar_historico(payload):
    for i, msg in enumerate(payload):
        label = msg["role"]
        if label == "user":
            print(Fore.RED + f"Usuario : {msg['content']}")
        else:
            print(Fore.MAGENTA + f"Modelo : {msg['content']}")

if __name__ == "__main__":
    # Carrega o histórico existente, se houver
    try:
        limpar_tela()
        carregar_api()
        criar_pasta()
        while True:
            msg = input(Fore.RED + "Usuario: ")
            txt = msg.split()
            if not txt:
                continue
            if txt[0] == "/exit":
                quit()
                
            elif txt[0] == "/novo_chat":
                limpar_tela()
                contador += 1
                arquivo_atual = str(contador)
                historico = []
                print(Fore.GREEN + f"Chat Criado: {contador}\n")   
                continue  
            elif txt[0] == "/ajuda": 
                print(Fore.GREEN + """  
    comandos:
        -- /carregar << carrega o chat usando o numero: exemplo /carregar 1
        -- /novo_chat << cria um novo chat
        -- /modelo << altera o modelo do groq: exemplo /carregar llama-3.1-8b-instant
        -- /exit << sai desse chatbox
        -- /ajuda << mostra essee print
    """)
                continue
            elif txt[0] == "/carregar":
                if len(txt) > 1:
                    resultado = carregar_arquivo(txt[1])
                    if resultado is not None:
                        limpar_tela()
                        historico = resultado
                        arquivo_atual = txt[1]
                        printar_historico(resultado)
                        try:
                            contador = int(txt[1])
                        except ValueError:
                            pass
                        continue 
                else:
                    print(Fore.RED + "Erro: Você precisa especificar o que deseja carregar. Ex: /carregar 1")
                    continue
                    
            elif txt[0] == "/modelo":
                if len(txt) > 1:
                    MODELO = txt[1]   
                    print(Fore.GREEN + f"Modelo mudado para {MODELO}\n")
                    continue
                else:
                    print(Fore.RED + "Erro: Especifique o modelo. Ex: /modelo openai/gpt-oss-20b")
                    continue
                
            else:
                adicionar_mensagem("user", f"{msg} \n")
                headers = {
                    "Authorization": "Bearer " + API,
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": MODELO,
                    "messages": historico
                }
                
                r = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
                if r.status_code == 200:
                    resposta = r.json()
                    conteudo = resposta["choices"][0]["message"]["content"]
                    adicionar_mensagem("assistant", f"{conteudo} \n")
                    print(Fore.MAGENTA + f"\nModelo: {conteudo} \n")
                    salvar_mensagem()
                elif r.status_code == 404: 
                    print(Fore.GREEN + "Chat invalido ou modelo invalido: 404")
                else:
                    print(Fore.GREEN + f"Falha na api: {r.status_code}")
                    
    except KeyboardInterrupt:
        print("\nKeyboard interrupt")
        print(Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\nOcorreu um erro inesperado: {e}")
        print(Style.RESET_ALL)
        
        
        

import json
import requests
import os
import subprocess
from colorama import init, Fore, Style
from pathlib import Path
from dotenv import load_dotenv
import sys
from rich.console import Console
from rich.markdown import Markdown

console = Console()
init(autoreset=True)
load_dotenv()

# --- Ferramentas do Agente ---
def list_dir(path="."):
    try:
        files = os.listdir(path)
        return "\n".join(files) if files else "Diretório vazio."
    except Exception as e:
        return f"Erro ao listar diretório: {e}"

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao ler arquivo: {e}"

def write_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Arquivo {path} criado/escrito com sucesso."
    except Exception as e:
        return f"Erro ao escrever arquivo: {e}"

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Erro ao executar comando: {e}"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "Útil para explorar o sistema de arquivos, ver quais arquivos existem em uma pasta e entender a estrutura do projeto.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Caminho do diretório (use '.' para atual)"}},
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Lê o conteúdo completo de um arquivo. Use isso para analisar códigos, ler READMEs ou logs.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Caminho completo do arquivo"}},
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Cria ou sobrescreve um arquivo com o conteúdo especificado. Útil para salvar scripts, notas ou configurações.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Caminho do arquivo a ser criado"},
                    "content": {"type": "string", "description": "Conteúdo do arquivo"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Sempre que precisar criar um arquivo, instalar um pacote ou executar um script python, use este comando. Você pode usar comandos como 'echo texto > arquivo.py' para criar arquivos ou 'python arquivo.py' para rodá-los.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string", "description": "Comando completo do terminal (bash/powershell)"}},
                "required": ["command"]
            }
        }
    }
]

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

# Mensagem de sistema para forçar a IA a usar ferramentas
SYSTEM_PROMPT = {
    "role": "system", 
    "content": "Você é um assistente programador proativo. Quando o usuário pedir um script ou código, NÃO apenas mostre o código. Use a ferramenta 'run_command' para criar o arquivo no disco e depois execute-o para mostrar o resultado ao usuário. Seja autônomo."
}

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

def adicionar_mensagem(papel, texto, tool_calls=None, tool_call_id=None):
    """Adiciona uma nova mensagem ao histórico."""
    msg = {"role": papel, "content": texto}
    if tool_calls:
        msg["tool_calls"] = tool_calls
    if tool_call_id:
        msg["tool_call_id"] = tool_call_id
    historico.append(msg)
    
def carregar_arquivo(nome):
    try:
        with open(f"{NOME_PASTA}/conversa_{nome}.json", "r", encoding="utf-8") as arquivo:
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
            conteudo = msg['content']
            md = Markdown(conteudo)
            console.print("\n[magenta]Modelo:[/magenta]")
            console.print(md, style="magenta")
            print()

if __name__ == "__main__":
    # Carrega o histórico existente, se houver
    try:
        limpar_tela()
        carregar_api()
        criar_pasta()
        
        # Inicializa o histórico com a mensagem de sistema
        historico = [SYSTEM_PROMPT]
        
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
                adicionar_mensagem("user", msg)
                headers = {
                    "Authorization": "Bearer " + API,
                    "Content-Type": "application/json"
                }
                
                # Loop de execução de ferramentas
                while True:
                    payload = {
                        "model": MODELO,
                        "messages": historico,
                        "tools": TOOLS,
                        "tool_choice": "auto"
                    }
                    
                    r = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
                    
                    if r.status_code != 200:
                        print(Fore.RED + f"Erro na API: {r.status_code}")
                        break
                    
                    resposta = r.json()
                    message = resposta["choices"][0]["message"]
                    
                    # Se a IA quiser usar uma ferramenta
                    if "tool_calls" in message:
                        for tool_call in message["tool_calls"]:
                            function_name = tool_call["function"]["name"]
                            args = json.loads(tool_call["function"]["arguments"])
                            
                            # Customização da mensagem de execução baseada na ferramenta e argumentos
                            msg_exec = f"🛠️ Executando {function_name}"
                            if function_name == "list_dir":
                                msg_exec += f" no diretório {args.get('path', '.')}"
                                result = list_dir(args.get("path", "."))
                            elif function_name == "read_file":
                                msg_exec += f" no arquivo {args.get('path', 'desconhecido')}"
                                result = read_file(args.get("path", ""))
                            elif function_name == "write_file":
                                msg_exec += f" criando o arquivo {args.get('path', 'desconhecido')}"
                                result = write_file(args.get("path", ""), args.get("content", ""))
                            elif function_name == "run_command":
                                msg_exec += f" o comando: {args.get('command', 'desconhecido')}"
                                result = run_command(args.get("command", ""))
                            else:
                                msg_exec += "..."
                                result = "Ferramenta desconhecida."
                            
                            console.print(f"\n[yellow]{msg_exec}...[/yellow]")
                            
                            # IMPORTANTE: Adiciona a chamada REAL da IA e depois o resultado
                            adicionar_mensagem("assistant", None, tool_calls=message["tool_calls"])
                            adicionar_mensagem("tool", result, tool_call_id=tool_call["id"])
                        
                        continue 
                    
                    conteudo = message.get("content", "")
                    markdown = Markdown(conteudo)
                    adicionar_mensagem("assistant", conteudo)
                    console.print("\n[bold magenta]Modelo:[/bold magenta]")
                    console.print(markdown, style="magenta")
                    print()
                    salvar_mensagem()
                    break
                
                # Nota: Os elifs de r.status_code foram movidos para dentro do loop ou removidos
                # pois o check 'if r.status_code != 200' já trata a maioria dos erros.
                    
    except KeyboardInterrupt:
        print("\nKeyboard interrupt")
        print(Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\nOcorreu um erro inesperado: {e}")
        print(Fore.RED + f"{r.json()}")
        print(Style.RESET_ALL)


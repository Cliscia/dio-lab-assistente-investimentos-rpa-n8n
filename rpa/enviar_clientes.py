
import requests
from bs4 import BeautifulSoup

# 1. Endereço da página com os clientes fictícios
URL_PAGINA = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"

# 2. Endereço do Webhook do n8n no Mac
N8N_WEBHOOK = "http://localhost:5679/webhook-test/Clientes"

# 3. Acessar a página web
response = requests.get(URL_PAGINA, timeout=15)
response.raise_for_status()

# 4. Interpretar o HTML
soup = BeautifulSoup(response.text, "html.parser")

# 5. Localizar as linhas da tabela de clientes
linhas = soup.select("#clientes tbody tr")

# 6. Criar uma lista para armazenar os clientes
clientes = []

# 7. Extrair os dados de cada cliente
for linha in linhas:
    colunas = linha.find_all("td")

    cliente = {
        "nome": colunas[0].get_text(strip=True),
        "email": colunas[1].get_text(strip=True),
        "saldo": colunas[2].get_text(strip=True),
        "perfil": colunas[3].get_text(strip=True),
    }

    clientes.append(cliente)

# 8. Verificar a quantidade de clientes encontrados
print(f"Clientes encontrados: {len(clientes)}")

# 9. Evitar enviar uma lista vazia
if not clientes:
    raise ValueError("Nenhum cliente foi encontrado.")

# 10. Enviar os clientes ao Webhook do n8n
response = requests.post(
    N8N_WEBHOOK,
    json={"clientes": clientes},
    timeout=15
)

# 11. Verificar se o envio foi realizado
response.raise_for_status()

print(f"Status HTTP: {response.status_code}")
print("Dados enviados ao n8n com sucesso!")

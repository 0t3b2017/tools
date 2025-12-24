import requests
import zipfile
import os


"""
Script to download and extract Dev Samurai courses available for free.
https://class.devsamurai.com.br/
"""

# pasta do drive onde os cursos serão baixados
drive_folder = "Cursos Dev Samurai"

# lista de urls que serão baixadas
# estrutura da lista:
# {
#     "name": "nome do curso",
#     "dir": "diretório onde o curso ficará no seu drive",
#     "url": "link de download do curso"
# }
links = [
    {"name": "Aulas ao Vivo",                               "dir": "Aulas",                 "url": "https://cursos.devsamurai.com.br/Aulas%20ao%20Vivo.zip"},
    {"name": "Backend - Dominando o NodeJS",                "dir": "Backend",               "url": "https://cursos.devsamurai.com.br/Backend%20-%20Dominando%20o%20NodeJS.zip"},
    {"name": "Backend - Dominando o Postgres",              "dir": "Backend",               "url": "https://cursos.devsamurai.com.br/Backend%20-%20Dominando%20o%20Postgres.zip"},
    {"name": "Carreira de Programador",                     "dir": "Carreira",              "url": "https://cursos.devsamurai.com.br/Carreira%20de%20Programador.zip"},
    {"name": "Flutter - Calculadora IMC",                   "dir": "Flutter",               "url": "https://cursos.devsamurai.com.br/Flutter%20-%20Calculadora%20IMC.zip"},
    {"name": "Flutter - Cardápio online",                   "dir": "Flutter",               "url": "https://cursos.devsamurai.com.br/Flutter%20-%20Card%C3%A1pio%20online.zip"},
    {"name": "Flutter - Fluck Noris",                       "dir": "Flutter",               "url": "https://cursos.devsamurai.com.br/Flutter%20-%20Fluck%20Noris.zip"},
    {"name": "Flutter - Lista de Leituras",                 "dir": "Flutter",               "url": "https://cursos.devsamurai.com.br/Flutter%20-%20Lista%20de%20Leituras.zip"},
    {"name": "Flutter Avançado",                            "dir": "Flutter",               "url": "https://cursos.devsamurai.com.br/Flutter%20Avan%C3%A7ado.zip"},
    {"name": "Flutter Básico",                              "dir": "Flutter",               "url": "https://cursos.devsamurai.com.br/Flutter%20B%C3%A1sico.zip"},
    {"name": "Flutter Snippets",                            "dir": "Flutter",               "url": "https://cursos.devsamurai.com.br/Flutter%20Snippets.zip"},
    {"name": "Frontend - Bootstrap",                        "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20Bootstrap.zip"},
    {"name": "Frontend - CSS Grid",                         "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20CSS%20Grid.zip"},
    {"name": "Frontend - Criando seu currículo",            "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20Criando%20seu%20curr%C3%ADculo.zip"},
    {"name": "Frontend - Criando seu portfólio",            "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20Criando%20seu%20portf%C3%B3lio.zip"},
    {"name": "Frontend - Curriculum HTML",                  "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20Curriculum%20HTML.zip"},
    {"name": "Frontend - Entendo o HTML com o CSS",         "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20Entendo%20o%20HTML%20com%20o%20CSS.zip"},
    {"name": "Frontend - Flexbox",                          "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20Flexbox.zip"},
    {"name": "Frontend - Formulário de Cadastro",           "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20Formul%C3%A1rio%20de%20Cadastro.zip"},
    {"name": "Frontend - HTML Básico",                      "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20HTML%20B%C3%A1sico.zip"},
    {"name": "Frontend - Loja de Café",                     "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20Loja%20de%20Caf%C3%A9.zip"},
    {"name": "Frontend - Mobile First",                     "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20Mobile%20First.zip"},
    {"name": "Frontend - Preprocessadores (Sass)",          "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20Preprocessadores%20(Sass).zip"},
    {"name": "Frontend - Sua primeira página Web",          "dir": "Frontend",              "url": "https://cursos.devsamurai.com.br/Frontend%20-%20Sua%20primeira%20p%C3%A1gina%20Web.zip"},
    {"name": "Full Stack - Food Commerce",                  "dir": "Full Stack",            "url": "https://cursos.devsamurai.com.br/Full%20Stack%20-%20Food%20Commerce.zip"},
    {"name": "Ionic",                                       "dir": "Ionic",                 "url": "https://cursos.devsamurai.com.br/Ionic.zip"},
    {"name": "JavaScript - Gerador Senhas",                 "dir": "JavaScript",            "url": "https://cursos.devsamurai.com.br/JavaScript%20-%20Gerador%20Senhas.zip"},
    {"name": "JavaScript Básico ao Avançado",               "dir": "JavaScript",            "url": "https://cursos.devsamurai.com.br/JavaScript%20B%C3%A1sico%20ao%20Avan%C3%A7ado.zip"},
    {"name": "Kapi Academy - API Supreme",                  "dir": "Kapi Academy",          "url": "https://cursos.devsamurai.com.br/Kapi%20Academy%20-%20API%20Supreme.zip"},
    {"name": "Linux para Programadores",                    "dir": "Linux",                 "url": "https://cursos.devsamurai.com.br/Linux%20para%20Programadores.zip"},
    {"name": "Lógica de Programação Avançada",              "dir": "Lógica",                "url": "https://cursos.devsamurai.com.br/L%C3%B3gica%20de%20Programa%C3%A7%C3%A3o%20Avan%C3%A7ada.zip"},
    {"name": "Lógica de Programação Básica",                "dir": "Lógica",                "url": "https://cursos.devsamurai.com.br/L%C3%B3gica%20de%20Programa%C3%A7%C3%A3o%20B%C3%A1sica.zip"},
    {"name": "Master Classes",                              "dir": "Master Classes",        "url": "https://cursos.devsamurai.com.br/Master%20Classes.zip"},
    {"name": "Minha Primeira Oportunidade",                 "dir": "Programador iniciante", "url": "https://cursos.devsamurai.com.br/Minha%20Primeira%20Oportunidade.zip"},
    {"name": "Minicurso Programar do Zero",                 "dir": "Programador iniciante", "url": "https://cursos.devsamurai.com.br/Minicurso%20Programar%20do%20Zero.zip"},
    {"name": "Monitoria Aberta",                            "dir": "Monitoria",             "url": "https://cursos.devsamurai.com.br/Monitoria%20Aberta.zip"},
    {"name": "Montando o ambiente Dev",                     "dir": "Programador iniciante", "url": "https://cursos.devsamurai.com.br/Montando%20o%20ambiente%20Dev.zip"},
    {"name": "Primeira Oportunidade",                       "dir": "Primeira Oportunidade", "url": "https://cursos.devsamurai.com.br/Primeira%20Oportunidade.zip"},
    {"name": "Programar do Zero - HTML",                    "dir": "Programador iniciante", "url": "https://cursos.devsamurai.com.br/Programar%20do%20Zero%20-%20HTML.zip"},
    {"name": "Programar do Zero - Jokenpo",                 "dir": "Programador iniciante", "url": "https://cursos.devsamurai.com.br/Programar%20do%20Zero%20-%20Jokenpo.zip"},
    {"name": "Programar do Zero - Ping-Pong",               "dir": "Programador iniciante", "url": "https://cursos.devsamurai.com.br/Programar%20do%20Zero%20-%20Ping-Pong.zip"},
    {"name": "Programar do Zero",                           "dir": "Programador iniciante", "url": "https://cursos.devsamurai.com.br/Programar%20do%20Zero.zip"},
    {"name": "Python - Forca",                              "dir": "Python Games",          "url": "https://cursos.devsamurai.com.br/Python%20-%20Forca.zip"},
    {"name": "Python - Jogo Adivinha",                      "dir": "Python Games",          "url": "https://cursos.devsamurai.com.br/Python%20-%20Jogo%20Adivinha.zip"},
    {"name": "Python - Jogo Cobrinha",                      "dir": "Python Games",          "url": "https://cursos.devsamurai.com.br/Python%20-%20Jogo%20Cobrinha.zip"},
    {"name": "Python - Juros Compostos",                    "dir": "Python Finanças",       "url": "https://cursos.devsamurai.com.br/Python%20-%20Juros%20Compostos.zip"},
    {"name": "Python - Tabela Fipe",                        "dir": "Python Finanças",       "url": "https://cursos.devsamurai.com.br/Python%20-%20Tabela%20Fipe.zip"},
    {"name": "Python Avançado",                             "dir": "Python",                "url": "https://cursos.devsamurai.com.br/Python%20Avan%C3%A7ado.zip"},
    {"name": "Python Básico",                               "dir": "Python",                "url": "https://cursos.devsamurai.com.br/Python%20B%C3%A1sico.zip"},
    {"name": "React - API Github",                          "dir": "React",                 "url": "https://cursos.devsamurai.com.br/React%20-%20API%20Github.zip"},
    {"name": "React - Fundamentos",                         "dir": "React",                 "url": "https://cursos.devsamurai.com.br/React%20-%20Fundamentos.zip"},
    {"name": "React - Lista de Leitura",                    "dir": "React",                 "url": "https://cursos.devsamurai.com.br/React%20-%20Lista%20de%20Leitura.zip"},
    {"name": "React Native - Calculadora IMC",              "dir": "React Native",          "url": "https://cursos.devsamurai.com.br/React%20Native%20-%20Calculadora%20IMC.zip"},
    {"name": "React Native - Publicando o Aplicativo",      "dir": "React Native",          "url": "https://cursos.devsamurai.com.br/React%20Native%20-%20Publicando%20o%20Aplicativo.zip"},
    {"name": "React Native - Smart Money - Firebase",       "dir": "React Native",          "url": "https://cursos.devsamurai.com.br/React%20Native%20-%20Smart%20Money%20-%20Firebase.zip"},
    {"name": "React Native - Smart Money - Navigation V5",  "dir": "React Native",          "url": "https://cursos.devsamurai.com.br/React%20Native%20-%20Smart%20Money%20-%20Navigation%20V5.zip"},
    {"name": "React Native - SmartMoney - Login",           "dir": "React Native",          "url": "https://cursos.devsamurai.com.br/React%20Native%20-%20SmartMoney%20-%20Login.zip"},
    {"name": "React Native - SmartMoney",                   "dir": "React Native",          "url": "https://cursos.devsamurai.com.br/React%20Native%20-%20SmartMoney.zip"},
    {"name": "React Native - TODO",                         "dir": "React Native",          "url": "https://cursos.devsamurai.com.br/React%20Native%20-%20TODO.zip"},
    {"name": "React Native",                                "dir": "React Native",          "url": "https://cursos.devsamurai.com.br/React%20Native.zip"},
    {"name": "Renda Extra 10x - Entrevistas",               "dir": "Renda Extra 10x",       "url": "https://cursos.devsamurai.com.br/Renda%20Extra%2010x%20-%20Entrevistas.zip"},
    {"name": "Renda Extra 10x - Mente Inabalável",          "dir": "Renda Extra 10x",       "url": "https://cursos.devsamurai.com.br/Renda%20Extra%2010x%20-%20Mente%20Inabal..zip"},
    {"name": "Renda Extra 10x - Precificação de Sistemas",  "dir": "Renda Extra 10x",       "url": "https://cursos.devsamurai.com.br/Renda%20Extra%2010x%20-%20Precifica%C3%A7%C3%A3o%20de%20Sistemas.zip"},
    {"name": "Renda Extra 10x - Treinamento extra",         "dir": "Renda Extra 10x",       "url": "https://cursos.devsamurai.com.br/Renda%20Extra%2010x%20-%20Treinamento%20extra.zip"},
    {"name": "Renda Extra 10x",                             "dir": "Renda Extra 10x",       "url": "https://cursos.devsamurai.com.br/Renda%20Extra%2010x.zip"},
    {"name": "TypeScript - TODO List",                      "dir": "TypeScript",            "url": "https://cursos.devsamurai.com.br/TypeScript%20-%20TODO%20List.zip"},
    {"name": "TypeScript Básico",                           "dir": "TypeScript",            "url": "https://cursos.devsamurai.com.br/TypeScript%20B%C3%A1sico.zip"}
]


for item in links:
  name = item["name"]
  dir = item["dir"]
  url = item["url"]

  if os.path.exists(f'/mnt/d/STUDIES/DEV Samurai/{name}.zip'):
    print(f"O arquivo {name}.zip já existe. Pulando download.")
    continue
  
  output_path = f'/mnt/d/STUDIES/DEV Samurai/{name}.zip'
  unzip_dir = f'/mnt/d/STUDIES/DEV Samurai/{dir}'

  # Passo 1 - Baixa o ZIP
  print(f"Iniciando o download de {name}")
  with requests.get(url, stream=True) as r:
    with open(output_path, 'wb') as f:
      for chunk in r.iter_content(chunk_size=8192):
        if chunk:
          f.write(chunk)
  print(f"Download completo. Arquivo salvo: {name}")

  # Passo 2 - Descompacta o arquivo
  try:
    with zipfile.ZipFile(output_path, 'r') as zip_ref:
      zip_ref.extractall(unzip_dir)
    print(f"Arquivo descompactado com sucesso na pasta: {unzip_dir}")
  except zipfile.BadZipFile:
    print(f"Erro: O arquivo não é um zip válido.")

  # Passo 3 - Remove o ZIP de origem
  if os.path.exists(output_path):
    os.remove(output_path)
    print(f"Arquivo zip original removido: {output_path}")
  else:
    print(f"Erro: O arquivo zip original não existe ou já foi removido: {output_path}")

print("Processamento concluído")
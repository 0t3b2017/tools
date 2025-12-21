import os
import sys
import random
import ctypes
from datetime import datetime, timedelta
from ctypes import wintypes

# --- Configurações da API do Windows para Data de Criação ---
class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", wintypes.DWORD),
                ("dwHighDateTime", wintypes.DWORD)]


def datetime_to_filetime(dt):
    """Converte datetime do Python para o formato FILETIME do Windows (100ns intervalos desde 1601)."""
    EPOCH_AS_FILETIME = 116444736000000000
    HUNDREDS_OF_NANOSECONDS = 10000000
    timestamp = dt.timestamp()
    return int(timestamp * HUNDREDS_OF_NANOSECONDS + EPOCH_AS_FILETIME)


def set_file_creation_time(filepath, new_datetime):
    """Altera a data de criação do arquivo usando a API Win32."""
    timestamp = datetime_to_filetime(new_datetime)
    ft = FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)
    
    handle = ctypes.windll.kernel32.CreateFileW(
        filepath, 256, 0, None, 3, 128, None
    )

    if handle == -1:
        return False

    result = ctypes.windll.kernel32.SetFileTime(handle, ctypes.byref(ft), None, None)
    ctypes.windll.kernel32.CloseHandle(handle)
    return result != 0

# --- Lógica Principal ---

def garantir_final_de_semana(dt_atual):
    """
    Se não for Sábado (5) ou Domingo (6), avança para o próximo Sábado.
    """
    while dt_atual.weekday() < 5:
        dt_atual += timedelta(days=1)
        # Ao pular para o Sábado, reseta o horário para de manhã
        dt_atual = dt_atual.replace(hour=random.randint(8, 10), minute=random.randint(0, 59))
    return dt_atual


def gerar_data_base_aleatoria():
    """Gera uma data aleatória entre 01/01/2023 e 30/11/2025 para servir de base para a pasta."""
    inicio = datetime(2025, 7, 7)
    fim = datetime(2025, 11, 30) # Limite máximo: final de Novembro 2025
    
    # Calcula a diferença exata em dias
    dias_totais = (fim - inicio).days
    
    dias_aleatorios = random.randint(0, dias_totais) 
    data_base = inicio + timedelta(days=dias_aleatorios)
    
    # Garante que começa num fim de semana
    return garantir_final_de_semana(data_base)


def processar_arquivos(pasta_raiz):
    print(f"Iniciando processamento recursivo em: {pasta_raiz}")
    
    total_arquivos = 0
    erros = 0
    data_limite_absoluta = datetime(2025, 11, 30, 23, 59, 59)

    # Percorre cada subpasta
    for root, dirs, files in os.walk(pasta_raiz):
        if not files:
            continue # Pula pastas vazias
            
        # --- NOVA LÓGICA: Data muda por PASTA ---
        # Para cada nova pasta (root), geramos uma data base nova
        tempo_corrente = gerar_data_base_aleatoria()
        
        # Define um horário inicial para o primeiro arquivo da pasta (ex: entre 08:00 e 10:00)
        tempo_corrente = tempo_corrente.replace(hour=random.randint(8, 10), minute=random.randint(0, 59))

        print(f"\n[Pasta] {root}")
        print(f" -> Data Base definida: {tempo_corrente.strftime('%d/%m/%Y')}")

        for file in files:
            caminho_completo = os.path.join(root, file)
            
            try:
                # 1. Incrementa minutos (10 a 25 min) para o próximo arquivo da mesma pasta
                minutos_extra = random.randint(10, 25)
                tempo_corrente += timedelta(minutes=minutos_extra)
                
                # 2. Checagem de segurança: Se a adição de minutos fez virar Segunda-feira (ou dia útil),
                # a função abaixo joga para o próximo Sábado para manter a regra dos finais de semana.
                tempo_corrente = garantir_final_de_semana(tempo_corrente)
                
                # 2.1 Checagem de Limite Máximo (Novembro 2025)
                # Se por acaso o incremento estourar o limite, voltamos para uma data segura aleatória
                if tempo_corrente > data_limite_absoluta:
                    tempo_corrente = gerar_data_base_aleatoria()
                    tempo_corrente = tempo_corrente.replace(hour=random.randint(8, 10), minute=random.randint(0, 59))
                
                # Visualização no console (opcional, pode comentar se forem muitos arquivos)
                # print(f"   - {file} -> {tempo_corrente.strftime('%d/%m/%Y %H:%M')}")

                # 3. Altera Data de Criação (Windows API)
                sucesso_criacao = set_file_creation_time(caminho_completo, tempo_corrente)
                
                # 4. Altera Data de Modificação e Acesso (Python Standard)
                timestamp_unix = tempo_corrente.timestamp()
                os.utime(caminho_completo, (timestamp_unix, timestamp_unix))
                
                if not sucesso_criacao:
                    print(f"   [!] Erro na data de CRIAÇÃO: {file} (Arquivo em uso/sistema?)")
                
                total_arquivos += 1
                
            except Exception as e:
                print(f"   [!] Erro fatal em {file}: {e}")
                erros += 1

    print("-" * 30)
    print(f"Concluído! Total processado: {total_arquivos}. Erros: {erros}.")


if __name__ == "__main__":
    # --- CONFIGURAÇÃO ---
    PASTA_ALVO = r"C:\Caminho\Para\Sua\Pasta"  # <-- Altere para a pasta desejada   
    
    if os.path.exists(PASTA_ALVO):
        processar_arquivos(PASTA_ALVO)
    else:
        print(f"Erro: A pasta '{PASTA_ALVO}' não foi encontrada.")

import pdfplumber
import pandas as pd
import os
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def verificar_arquivo(caminho_arquivo):
    """Verifica se o arquivo existe."""
    if not os.path.exists(caminho_arquivo):
        logging.error(f"Arquivo {caminho_arquivo} não encontrado.")
        raise FileNotFoundError(f"Arquivo {caminho_arquivo} não encontrado.")
    return True

def extrair_dados_pdf(caminho_pdf):
    """Extrai dados de um PDF usando pdfplumber."""
    dados = []
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                # Tentar extrair tabela primeiro
                tabela = pagina.extract_table()
                if tabela:
                    dados.extend(tabela)
                else:
                    # Fallback para extrair texto se não houver tabela
                    texto = pagina.extract_text()
                    if texto:
                        for linha in texto.split("\n"):
                            if linha.strip():
                                dados.append(linha.split())
        logging.info(f"Extraídas {len(dados)} linhas do PDF.")
        return dados
    except Exception as e:
        logging.error(f"Erro ao extrair dados do PDF: {e}")
        raise

def criar_dataframe(dados, colunas=None):
    """Cria um DataFrame a partir dos dados extraídos."""
    try:
        # Se colunas não forem fornecidas, usar padrão
        if colunas is None:
            colunas = ["Data", "Produto", "Quantidade", "Valor"]
        
        # Filtrar linhas com número correto de colunas
        dados_filtrados = [linha for linha in dados if len(linha) == len(colunas)]
        if len(dados_filtrados) < len(dados):
            logging.warning(f"{len(dados) - len(dados_filtrados)} linhas ignoradas por formato inválido.")
        
        df = pd.DataFrame(dados_filtrados, columns=colunas)
        
        # Converter tipos de dados
        df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")
        df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
        
        # Tratar valores nulos
        nulos = df.isnull().sum()
        if nulos.any():
            logging.warning(f"Valores nulos encontrados:\n{nulos}")
            df = df.dropna()  # Ou outro tratamento, se desejar
        
        return df
    except Exception as e:
        logging.error(f"Erro ao criar DataFrame: {e}")
        raise

def salvar_excel(df, caminho_saida):
    """Salva o DataFrame como arquivo Excel."""
    try:
        df.to_excel(caminho_saida, index=False)
        logging.info(f"Dados salvos em {caminho_saida}")
    except Exception as e:
        logging.error(f"Erro ao salvar arquivo Excel: {e}")
        raise

def main(caminho_pdf, caminho_saida="dados_tratados.xlsx", colunas=None):
    """Função principal para processar o PDF e salvar os dados."""
    try:
        verificar_arquivo(caminho_pdf)
        dados = extrair_dados_pdf(caminho_pdf)
        df = criar_dataframe(dados, colunas)
        salvar_excel(df, caminho_saida)
        print(df.head())
        logging.info("Processamento concluído com sucesso.")
    except Exception as e:
        logging.error(f"Erro no processamento: {e}")

if __name__ == "__main__":
    caminho_pdf = "relatorio.pdf"
    caminho_saida = "dados_tratados.xlsx"
    main(caminho_pdf, caminho_saida)

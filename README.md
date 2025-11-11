# 🏙️ Sistema de Processamento de Imagens – Grupo 2  
## 🧩 Conversão de Imagens para Escala de Cinza  

---



### 📘 Descrição do Projeto
A cidade de **Véridia** está desenvolvendo um **Sistema de Processamento de Imagens** para uso em áreas como **educação, saúde e indústria**.  
O sistema visa **analisar, transformar e realçar imagens digitais**, permitindo que operadores e administradores apliquem **filtros, transformações e análises de padrões**, mantendo registro dos resultados obtidos.  

Este repositório corresponde ao **Grupo 2**, responsável pelo módulo de **Conversão de Imagens para Escala de Cinza**, utilizando a linguagem **Python** e bibliotecas de processamento e análise de imagens.  

---

### 👩‍💻 Integrantes do Grupo

- DAVI ROCHA DOS SANTOS 
- JENIFER BEATRIZ SILVA DE LIMA 
- JOÃO THIAGO NUNES DA SILVEIRA FILHO 
- JOÃO VITOR REZENDE MOURA 
- JULIO RAFAEL SOUZA PEIXOTO 

---

### 🎯 Objetivos do Sistema
- Centralizar o processamento de imagens em uma única plataforma.  
- Facilitar a aplicação de filtros e transformações de forma controlada.  
- Garantir consistência e integridade dos resultados.  
- Permitir análise detalhada de padrões e componentes de imagens.  
- Incentivar pesquisa e aplicação de novas técnicas em processamento de imagens.  

---

### 🧱 Objetivos do Grupo 2
1. Implementar as funções propostas na Unidade I.  
2. Converter imagens coloridas para **escala de cinza** após detecção de ruído.  
3. Aplicar **filtros de suavização** (Gaussian, Bilateral e Median) e comparar resultados.  
4. Criar função para medir **nitidez (foco)** utilizando o **Laplaciano**.  
5. Desenvolver um **avaliador de qualidade de imagem** baseado em ruído e foco.  
6. Armazenar resultados em **tabelas comparativas** e **imagens processadas**.  
7. Documentar o processo de desenvolvimento.  
8. Elaborar um **artigo científico** detalhando todo o processo.  

---

### 🧰 Tecnologias e Bibliotecas Utilizadas
- **Python 3.10+**  
- **NumPy** – manipulação de matrizes e cálculos numéricos  
- **OpenCV (cv2)** – processamento e filtragem de imagens  
- **Pillow (PIL)** – leitura e manipulação de imagens  
- **scikit-image** – métricas e transformações avançadas  
- **matplotlib** – visualização de resultados  
- **scikit-learn** – análises estatísticas e comparação  
- **reportlab** – geração de relatórios em PDF  
- *(opcional)* **TensorFlow / Streamlit** – interface e IA  

---

### 🧪 Fluxo de Processamento
1. Upload ou carregamento da imagem
2. Detecção de ruído
3. Conversão para escala de cinza
4. Aplicação de filtros (Gaussian, Bilateral, Median)
5. Cálculo de nitidez com Laplaciano
6. Geração de tabela comparativa
7. Exportação de resultados e relatório

---

### 📁 Estrutura do Projeto
```plaintext
grupo2_conversao_cinza/
│
├── imagens/                # Imagens originais
├── docs/                   # Relatórios e documentação
├── src/                    # Códigos-fonte do projeto
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação do repositório

```

## Extração de Atributos

Dentro da extração de atributos, temos que uma das primeiras situações que temos, é a equalização da imagem quando contornada para a escala de cinza, e isso pode ser vista em:


![Comparação de Histogramas](src/processed_images/histogram_equalization_comparison-071a8acd-e0ed-4e6a-a49f-56d4926d7bd8.jpg)

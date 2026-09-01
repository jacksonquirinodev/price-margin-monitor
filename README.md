# Price Margin Monitor

Automação para monitoramento de preços de produtos, cálculo de margem de lucro e geração de relatórios utilizando Python.

## 📌 Sobre o projeto

O **Price Margin Monitor** foi desenvolvido para automatizar o processo de consulta de preços de produtos em diferentes lojas online.

A aplicação acessa as páginas dos produtos utilizando **Playwright**, coleta os preços, calcula a margem de lucro com base em um custo definido e gera um relatório em **Excel** e **TXT**.

Ao final da execução, o relatório é enviado automaticamente para um grupo do **WhatsApp**.

O projeto também possui um sistema de **agendamento automático**, permitindo que a automação seja executada diariamente em um horário definido.

## ⚙️ Funcionalidades

* 🔎 Consulta automatizada de preços em lojas online
* 📊 Cálculo da margem de lucro
* 📁 Geração de relatório em Excel
* 📄 Geração de relatório em arquivo TXT
* 💬 Envio automático do relatório pelo WhatsApp
* ⏰ Execução automática através de agendamento
* 🌐 Automação de navegador utilizando Playwright

## 🛠️ Tecnologias utilizadas

* **Python**
* **Playwright** — automação e navegação web
* **OpenPyXL** — geração de planilhas Excel
* **PyAutoGUI** — automação da interface do sistema
* **Pyperclip** — manipulação da área de transferência
* **Schedule** — agendamento das execuções
* **Pathlib** — manipulação de arquivos e diretórios

## 🔄 Fluxo da automação

```text
Agendamento
     ↓
Acesso às lojas online
     ↓
Coleta dos preços
     ↓
Cálculo da margem de lucro
     ↓
Geração dos relatórios
     ↓
Envio do relatório pelo WhatsApp
```

## 📂 Estrutura do projeto

```text
price-margin-monitor/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/price-margin-monitor.git
```

### 2. Acesse a pasta do projeto

```bash
cd price-margin-monitor
```

### 3. Crie um ambiente virtual

```bash
python -m venv venv
```

### 4. Ative o ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Instale os navegadores do Playwright

```bash
playwright install
```

### 7. Execute a aplicação

```bash
python app.py
```

## ⚠️ Observações

Este projeto utiliza automação de navegador e automação da interface gráfica para realizar algumas etapas do processo. Por isso, o ambiente utilizado para execução deve estar devidamente configurado.

As configurações de produtos, horário de execução, custo do produto e grupo de WhatsApp são definidas no código da aplicação.

O projeto foi desenvolvido com foco em **automação de processos e integração entre diferentes ferramentas**, servindo também como projeto prático para aplicação de conceitos de programação em Python.

## 📚 Objetivo

Este projeto faz parte do meu portfólio de desenvolvimento e representa uma aplicação prática de **Python, automação web, manipulação de dados e geração de relatórios**.

---

**Desenvolvido com Python 🐍**

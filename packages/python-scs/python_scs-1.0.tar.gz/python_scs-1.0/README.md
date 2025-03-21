# Python Scripts Cron Scheduler

**Abstração com Painel em Streamlit para gestão do agendamento de scripts Python através de CronJobs.**

![Demo](./demo.png)

## 📌 Instalação

```bash
pip install python_scs
```

Caso vá utilizar o painel em Streamlit
```bash
pip install python_scs[streamlit]
```

## 🚀 Configuração

Confira o [exemplo completo](https://github.com/iagobalmeida/python_scs/tree/master/examples).

1. Certifique-se de ter a seguinte estrutura de diretórios:

```
├── scripts/
│   ├── logs/
│   ├── script_teste.py
│   ├── __init__.py
├── main.py
```

2. Instancie o gerenciador de scripts e configure o painel:

```python
# main.py

import os
from python_scs import PythonScriptsCronManager
from python_scs.streamlit import PannelConfig, StreamlitPannel

scripts_manager = PythonScriptsCronManager(
    config=PythonScriptsCronManager.Config(
        app_path=os.path.abspath('.'),  # Raiz onde scripts_folder estará
        scripts_folder='scripts',       # Diretório com os códigos
        logs_folder='scripts/logs'      # Diretório de logs
    ),
    user=True
)

streamlit_pannel = StreamlitPannel(scripts_manager, config=PannelConfig(
    layout='wide',
    title='Crontab Interface',
    subheader='Interface para gerenciamento de agendamentos',
    allow_upload_script=True,
    allow_create_job=True,
    allow_execute_job=True,
    allow_toggle_job=True,
    allow_remove_job=True
))
```

3. Execute o painel utilizando o `streamlit`:

```bash
streamlit run streamlit_pannel.py
```

## 🛠 Uso da API

### Instanciando o gerenciador de scripts

```python
import os
from python_scs import PythonScriptsCronManager

scripts_manager = PythonScriptsCronManager(
    config=PythonScriptsCronManager.Config(
        app_path=os.path.abspath("."),  # Raiz onde scripts_folder estará
        scripts_folder="scripts",       # Diretório com os códigos
        logs_folder="scripts/logs"      # Diretório de logs
    ),
    user=True
)
```

📌 *Veja a [documentação do python-crontab](https://pypi.org/project/python-crontab/#how-to-use-the-module) para entender o parâmetro `user`.*

### Listando os scripts disponíveis

```python
scripts = scripts_manager.get_scripts()
print(scripts)  # ["script_teste.py"]
```

### Criando um agendamento

```python
job = scripts_manager.set_script_job(
    script_name="script_teste.py",
    schedule=["* * * * *"],
    comment="Agendamento teste",
    enable=True
)

# Criando um agendamento com comando customizado
job = scripts_manager.set_job(
    command='echo "Teste"',
    schedule=["* * * * *"],
    log_file_name="teste.txt",  # Necessário para armazenar a saída
    comment="Agendamento customizado",
    enable=True
)
```

📌 Para verificar se o agendamento foi criado, execute:
```bash
crontab -l
```

### Listando os agendamentos configurados

```python
jobs = scripts_manager.get_jobs()
for job in jobs:
    print(f"{job.comment} - {job.script_name} - {job.is_runing()}")

# Busca um agendamento por filtros
job_script_test = scripts_manager.get_job({
    "script_name": "script_teste.py",
    "comment": "Agendamento teste"
})
```

### Habilitando, desabilitando, executando e removendo um agendamento

```python
job = scripts_manager.get_job({
    "script_name": "script_teste.py",
    "comment": "Agendamento teste"
})

job.enable_job()     # Habilita o job
job.disable_job()    # Desabilita o job
job.toggle_job()     # Alterna entre ativado/desativado

# Executa o script manualmente
scripts_manager.execute(job)

# Executa como subprocesso
scripts_manager.execute(job, use_subprocess=True)

# Remove o agendamento
scripts_manager.remove_job(job)
```

## 📜 Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.


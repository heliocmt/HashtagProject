{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "cd2aa8b8",
   "metadata": {},
   "outputs": [],
   "source": [
    "import json, requests\n",
    "import random\n",
    "import string\n",
    "import time\n",
    "\n",
    "def criar_email_aleatorio():\n",
    "    dominio = 'exemplo.com'\n",
    "    caracteres = string.ascii_letters + string.digits\n",
    "    \n",
    "    nome_aleatorio = ''.join(random.choice(caracteres) for _ in range(10))\n",
    "    email_aleatorio = f\"{nome_aleatorio}@{dominio}\"\n",
    "    \n",
    "    return email_aleatorio\n",
    "i=0\n",
    "while i<10:\n",
    "    email = criar_email_aleatorio()\n",
    "\n",
    "    nomes = ['João', 'Maria', 'Pedro', 'Ana', 'Lucas','Giulia', 'Augusto', 'Lina', 'Matheus', 'Helena','Igor', 'Joana', 'Guilherme', 'Nathalia', 'Jorge',]\n",
    "    nome = random.choice(nomes)\n",
    "\n",
    "    status_list = ['aprovado', 'recusado', 'reembolsado']\n",
    "    status = random.choice(status_list)\n",
    "\n",
    "    valor = random.randint(1, 1000)\n",
    "\n",
    "    forma_pagamento = ['boleto', 'pix', 'cartao de credito']\n",
    "    forma_pagamento = random.choice(forma_pagamento)\n",
    "\n",
    "    if forma_pagamento == 'cartao de credito':\n",
    "        parcelas = random.randint(1, 12)\n",
    "    else:\n",
    "        parcelas = 1\n",
    "\n",
    "    webhook_url = 'http://127.0.0.1:5000/webhook'\n",
    "\n",
    "    data = {  'nome': nome,\n",
    "              'email': email,\n",
    "              'status': status,\n",
    "              'valor': valor,\n",
    "              'forma_pagamento': forma_pagamento,\n",
    "              'parcelas': parcelas\n",
    "          }\n",
    "\n",
    "    r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})\n",
    "    i += 1\n",
    "    time.sleep(2)\n",
    "    "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

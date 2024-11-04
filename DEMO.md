# Demonstração Faber - Alice - ACME   

### Este é um roteiro de demonstração de agentes Aries com objetivo de observar a emissão e validação de credenciais verificáveis na stack hyperledger assim como a interação dos agentes com a blockchain indy.  
  

### Os Agentes; Faber, Alice e ACME são adaptações dos agentes de mesmo nome fornecidos pela aca-py.org. Para mais informações verificar https://aca-py.org/latest/aca-py.org/  
  

### Faber  

Emissor de credencial: emitirá credencial para Alice contendo formação acadêmica. A implementação do agente Faber também permite a validação de credenciais, no entanto esta função não será explorada nesta demo.  
  

### Alice  
Estudante formada na Faber University. Alice solicitará uma credencial verificavel a Faber contendo prova de sua formação acadêmica. Essa será apresentada a ACME como requisito para uma candidatura de emprego.  


### ACME  
Verificador/Emissor de credencial: ACME solicitará de Alice uma apresentação verificável onde Alice apresentará a credencial gerada por Faber contendo prova de sua formação acadêmica. ACME será capaz de verificar a credencial e como resultado emitir uma nova credencial contendo o cargo de Alice.  


## SETUP  


A demonstração proposta requer a realização dos passos contidos no arquivo [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md). Caso ainda não tenha os executado, pare aqui, acesse [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md) e retorne após cumprir as etapas lá elencadas.   

02 - Copiando os agentes demo para a pasta lab: Como descrito no arquivo [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md) a maquina virtual possui um diretório "lab" que está mapeado para o nível acima do diretório do projeto. O diretório "lab" permite interação de elementos da máquina host, como IDEAs, com elementos que podem ser vistos da máquina virtual. Copiaremos os agentes providos para o diretório "lab" e os executaremos de lá. Podemos fazer isto de duas formas: 

01a - Copiar a pasta 'runners' através do navegador de arquivos da máquina host 
- 01a.1 - Através do navegador de arquivos da máquina host, localize o diretório do projeto.  
- 01a.2 - Acessando o diretório do projeto localize a pasta "runners" 
- 01a.3 - Copie a pasta "runners" para o nível acima da pasta do projeto.  

	Exemplo: se a pasta do projeto está salva em  
	C:/media/user/projetos/indy_dev_env/ 
	copie a pasta "runners" para 
	C:/media/user/projetos/ 

### OU 

01b - Copiar a pasta 'runners' através da linha de comando da máquina virtual: 
- 01b.1 - Na máquina virtual certifique-se que está no diretório home/vagrant. Digite: 

```bash  
cd ~ 
```  

- 01b.2 - Informe o seguinte comando 
```bash  
cp -r ../../lab/indy_dev_env/runners/ ../../lab/runners 
```  


02 - Obtendo LEDGER_URL: os agentes fornecidos pela aca-py foram idealizados para serem executados em localhost, e, portanto, procurar a blockchain von-network em localhost:9000. No entanto, como estaremos os executando de uma máquina virtual, e como vimos em [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md) a blockchain não estará escutando em localhost:9000, logo devemos informar o ip correto para que os agentes possam encontrar o gênesis file de nossa von-network. 

02.1 - Na máquina virtual certifique-se que a von-network esteja up. Instruções para o mesmo estão em [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md) 


02.2 - Com a von-network up, obtenha o seu endereço, novamente com as instruções em [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md). Para este exemplo, o ip onde se encontra a von-network é 192.168.178.172:9000 



## INICIANDO OS AGENTES

01 - Abra um terminal de linha de comando na pasta principal do projeto, a que contém o arquivo "Vagrant file" 

02 - Acesse a máquina virtual através do comando: 
```bash 
vagrant ssh 
```   
03 - Verifique se os containers nós da von-network e postgres estão rodando através do comando  
```bash   
sudo docker ps 
```   
que deve listar os containers rodando: 
```bash 
CONTAINER ID   IMAGE              COMMAND                  CREATED        STATUS        PORTS                                                           NAMES 
b52d061ec5db   von-network-base   "./scripts/start_nod…"   24 hours ago   Up 24 hours   0.0.0.0:9707-9708->9707-9708/tcp, :::9707-9708->9707-9708/tcp   von-node4-1 
212f7587dde3   von-network-base   "./scripts/start_nod…"   24 hours ago   Up 24 hours   0.0.0.0:9701-9702->9701-9702/tcp, :::9701-9702->9701-9702/tcp   von-node1-1 
07f02a4e8827   von-network-base   "./scripts/start_nod…"   24 hours ago   Up 24 hours   0.0.0.0:9705-9706->9705-9706/tcp, :::9705-9706->9705-9706/tcp   von-node3-1 
3261605956b9   von-network-base   "bash -c 'sleep 10 &…"   24 hours ago   Up 24 hours   0.0.0.0:9000->8000/tcp, :::9000->8000/tcp                       von-webserver-1 
b1591e3c60e2   von-network-base   "./scripts/start_nod…"   24 hours ago   Up 24 hours   0.0.0.0:9703-9704->9703-9704/tcp, :::9703-9704->9703-9704/tcp   von-node2-1 
2ff0aac77b96   postgres           "docker-entrypoint.s…"   24 hours ago   Up 24 hours   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp                       some-postgres 
```   

04 - Acesse a pasta "lab/runners" através do comando: 
```bash   
cd ../../lab/runners  
```   

05 - Uma vez na pasta runners execute o agente Alice através do comando: 
```bash   
LEDGER_URL=http://192.168.178.172:9000 DEFAULT_POSTGRES=true python3 -m alice --port 8030 
```   

06 - Acesse a von-netwrok no browser e localize no canto inferior direito a seção "Ledger State" e acesse o link "Domain". Note que como Alice é um agente do tipo "holder" nenhuma interação é feita com a blockchain, sendo que Alice ainda está aguardando comunicação com Faber e ACME que registrarão seus esquemas na blockchain. 

07 - De volta ao terminal, verifique que o agente Alice está rodando e aguardando conexão 
```bash   
#9 Input faber.py invitation details 
Invite details:            
```   

08 - Para subir o agente Faber repita os passos 01,02 e 04 Uma vez na pasta runners execute o agente Faber através do comando: 
```bash   
LEDGER_URL=http://192.168.178.172:9000 DEFAULT_POSTGRES=true python3 -m faber --port 8020 
```   

09 - Observe que no processo de inicialização, o agente Faber exibirá o esquema de credencial que registrará na blockchain. Ele deve se parecer com isso: 
```bash   
#3/4 Create a new schema/cred def on the ledger 
Schema: 
  { 
    "sent": { 
      "schema_id": "HhcefS5SXBKbdqRRMr9wXd:2:degree schema:42.48.62", 
      "schema": { 
        "ver": "1.0", 
        "id": "HhcefS5SXBKbdqRRMr9wXd:2:degree schema:42.48.62", 
        "name": "degree schema", 
        "version": "42.48.62", 
        "attrNames": [ 
          "timestamp", 
          "name", 
          "date", 
          "degree", 
          "birthdate_dateint" 
        ], 
        "seqNo": 8 
      } 
    }, 
    "schema_id": "HhcefS5SXBKbdqRRMr9wXd:2:degree schema:42.48.62", 
    "schema": { 
      "ver": "1.0", 
      "id": "HhcefS5SXBKbdqRRMr9wXd:2:degree schema:42.48.62", 
      "name": "degree schema", 
      "version": "42.48.62", 
      "attrNames": [ 
        "timestamp", 
        "name", 
        "date", 
        "degree", 
        "birthdate_dateint" 
      ], 
      "seqNo": 8 
    } 
  } 
```   

10 - Acesse a von-netwrok no browser e localize no canto inferior direito a seção "Ledger State" e acesse o link "Domain". Note que diferentemente de Alice, Faber gerou entradas na blockchain, já que é um agente com a capacidade de emitir credenciais verificáveis. Verifique os campos: 

- Message wrapper 
- Metadata 
- Transaction 
O campo Transaction conterá o atributo "Alias: faber.agent" 

Expanda o campo "raw data" para verificar a estrutura do esquema. 

11 - De volta ao terminal, verifique que o agente Faber está rodando e gerou dados para estabelecer uma conexão, eles devem parecer como o do exemplo:
* ### Não copie os dados aqui apresentados para conexões, utilize os gerados no terminal da própria máquina.

```bash   
Invitation Data: 
{"@type": "https://didcomm.org/out-of-band/1.1/invitation", "@id": "8226a8df-58b3-4abd-9659-c97e784ae6ed", "handshake_protocols": ["https://didcomm.org/didexchange/1.0"], "services": [{"id": "#inline", "type": "did-communication", "recipientKeys": ["did:key:z6MksZo11N7Wz9hHnBNtk2krbNguNC4AHTk8SJ6hSmBVMwid"], "serviceEndpoint": "http://localhost:8020"}], "label": "faber.agent"} 
```   

12 - Utilize apenas a parte depois de Data: 
```bash   
{"@type": "https://didcomm.org/out-of-band/1.1/invitation", "@id": "8226a8df-58b3-4abd-9659-c97e784ae6ed", "handshake_protocols": ["https://didcomm.org/didexchange/1.0"], "services": [{"id": "#inline", "type": "did-communication", "recipientKeys": ["did:key:z6MksZo11N7Wz9hHnBNtk2krbNguNC4AHTk8SJ6hSmBVMwid"], "serviceEndpoint": "http://localhost:8020"}], "label": "faber.agent"} 
``` 

Cole no terminal do agente Alice, pressione ENTER para estabelecer uma sessão entre os 2 agentes, liberando os menus de operação em ambos. 

13 -  O menu do agente Alice deve se parecer com: 
```bash   
Alice      | Connected 
Alice      | Check for endorser role ... 
Connect duration: 0.35s 
    (3) Send Message 
    (4) Input New Invitation
    (5) Display All Credentials 
    (X) Exit?                                                                                                                                                                                                                               

[3/4/X]                          
```   

14 - O menu do agente Faber deve se parecer com: 
```bash   
Faber      | Connected 
Faber      | Check for endorser role ... 
    (1) Issue Credential 
    (1a) Set Credential Type (indy) 
    (2) Send Proof Request 
    (2a) Send *Connectionless* Proof Request (requires a Mobile client) 
    (3) Send Message 
    (4) Create New Invitation 
    (T) Toggle tracing on credential/proof exchange 
    (X) Exit?                                                                                                                                                                                                                                  

[1/2/3/4/T/X]        
```   

15 - Para testar a comunicação entre agentes, podemos enviar mensagens de alice para Faber ou vice e versa. No exemplo mandaremos um "Hellow from Alice" de Alice para Faber, escolhendo a opção 3 em Alice, informando a mensagem e verificando a chegada dela em Faber. 
```bash  
Alice      | Connected 
Alice      | Check for endorser role ... 
Connect duration: 0.27s 
    (3) Send Message 
    (4) Input New Invitation
    (5) Display All Credentials
    (X) Exit?                                                                                                                                                                                                                                  
[3/4/X] 3                                                                                                                                                                                                                                      
Enter message: Hellow from Alice                                                                                                                                                                                                               
Alice      | Received message: faber.agent received your message 
```   

em Faber observa-se: 

```bash  
Faber      | Connected 
Faber      | Check for endorser role ... 
Faber      | Received message: Hellow from Alice 

    (1) Issue Credential 
    (1a) Set Credential Type (indy) 
    (2) Send Proof Request 
    (2a) Send *Connectionless* Proof Request (requires a Mobile client) 
    (3) Send Message 
    (4) Create New Invitation 
    (T) Toggle tracing on credential/proof exchange 
    (X) Exit?                                                                                                                                                                                                                                  

[1/2/3/4/T/X]                                      
```   

16 - Em Faber emitiremos uma credencial para Alice, que conterá prova de que Alice possui uma graduação em Faber. No agente Faber escolha a opção 1. Observe em Faber: 
```bash  
#13 Issue credential offer to X 
Faber      | Credential: state = offer-sent, cred_ex_id = 868b3e3d-e2d4-4164-99d1-f7827f23c095 
Faber      | Credential: state = request-received, cred_ex_id = 868b3e3d-e2d4-4164-99d1-f7827f23c095 
#17 Issue credential to X 
Faber      | Credential: state = credential-issued, cred_ex_id = 868b3e3d-e2d4-4164-99d1-f7827f23c095 
Faber      | Credential: state = done, cred_ex_id = 868b3e3d-e2d4-4164-99d1-f7827f23c095 
```   

17 - Em Alice, observe que o agente foi informado do recebimento de uma credencial: 
```bash  
Alice      | Credential: state = offer-received, cred_ex_id = 4ec19496-c196-4ce7-abf3-e047901445bb 
#15 After receiving credential offer, send credential request 
Alice      | No 'by_format' in message: {'connection_id': 'de667020-f894-44bd-a25b-bb27aff9f6bb', 'role': 'holder', 'initiator': 'external', 'auto_offer': False, 'auto_issue': False, 'auto_remove': False, 'thread_id': '27b8f515-9287-4a87-b79a-5eca6b07f5f9', 'state': 'offer-received', 'trace': False, 'created_at': '2024-10-30T06:36:18.851434Z', 'updated_at': '2024-10-30T06:36:18.851434Z', 'cred_ex_id': '4ec19496-c196-4ce7-abf3-e047901445bb'} 
Alice      | Credential: state = request-sent, cred_ex_id = 4ec19496-c196-4ce7-abf3-e047901445bb 
Alice      | Credential: state = credential-received, cred_ex_id = 4ec19496-c196-4ce7-abf3-e047901445bb 
#18.1 Stored credential a75f3d8f-b97e-4e35-9621-ecbb4f4cf3cb in wallet 
Alice      | Credential: state = done, cred_ex_id = 4ec19496-c196-4ce7-abf3-e047901445bb 
Credential details: 
  { 
    "referent": "a75f3d8f-b97e-4e35-9621-ecbb4f4cf3cb", 
    "schema_id": "HhcefS5SXBKbdqRRMr9wXd:2:degree schema:42.48.62", 
    "cred_def_id": "HhcefS5SXBKbdqRRMr9wXd:3:CL:8:faber.agent.degree_schema", 
    "rev_reg_id": null, 
    "cred_rev_id": null, 
    "attrs": { 
      "degree": "Maths", 
      "date": "2018-05-28", 
      "name": "Alice Smith", 
      "birthdate_dateint": "20001030", 
      "timestamp": "1730270178" 
    } 
  } 
Alice      | credential_id a75f3d8f-b97e-4e35-9621-ecbb4f4cf3cb 
Alice      | cred_def_id HhcefS5SXBKbdqRRMr9wXd:3:CL:8:faber.agent.degree_schema 
Alice      | schema_id HhcefS5SXBKbdqRRMr9wXd:2:degree schema:42.48.62 
```   

18 - Verifique no agente Alice o recibemento da nova credencial. Agora a opção 5 listará uma credencial que deve parecer como a seguinte:
```bash
All credentials: {'results': [{'referent': '743bd53a-6a4e-4220-8372-9a86a455359b', 'schema_id': 'Aj3WVTqSoLpEwEHJnENwqv:2:degree schema:62.15.36', 'cred_def_id': 'Aj3WVTqSoLpEwEHJnENwqv:3:CL:99:faber.agent.degree_schema', 'rev_reg_id': None, 'cred_rev_id': None, 'attrs': {'timestamp': '1730755630', 'name': 'Alice Smith', 'birthdate_dateint': '20001104', 'date': '2018-05-28', 'degree': 'Maths'}}]}
``` 

19 - Mesmo tendo a capacidade de verificar a própria credencial, faremos uma solicitação de apresentação de credencial com o agente ACME. Para subir o agente ACME repita os passos 01,02 e 04 Uma vez na pasta runners execute o agente ACME através do comando: 
```bash   
LEDGER_URL=http://192.168.178.172:9000 DEFAULT_POSTGRES=true python3 -m acme --port 8040 
```   

20 - Observe que no processo de inicialização, o agente ACME exibirá esquemas de credenciais que registrará na blockchain. Ele deve se parecer com isso: 
```bash   
#3/4 Create a new schema/cred def on the ledger 
Schema: 
  { 
    "sent": { 
      "schema_id": "7eB7xGuxATC2UyF589kk1n:2:employee id schema:13.29.17", 
      "schema": { 
        "ver": "1.0", 
        "id": "7eB7xGuxATC2UyF589kk1n:2:employee id schema:13.29.17", 
        "name": "employee id schema", 
        "version": "13.29.17", 
        "attrNames": [ 
          "employee_id", 
          "date", 
          "position", 
          "name" 
        ], 
        "seqNo": 12 
      } 
    }, 
    "schema_id": "7eB7xGuxATC2UyF589kk1n:2:employee id schema:13.29.17", 
    "schema": { 
      "ver": "1.0", 
      "id": "7eB7xGuxATC2UyF589kk1n:2:employee id schema:13.29.17", 
      "name": "employee id schema", 
      "version": "13.29.17", 
      "attrNames": [ 
        "employee_id", 
        "date", 
        "position", 
        "name" 
      ], 
      "seqNo": 12 
    } 
  } 
Schema ID: 7eB7xGuxATC2UyF589kk1n:2:employee id schema:13.29.17 
Cred def ID: 7eB7xGuxATC2UyF589kk1n:3:CL:12:acme.agent.employee_id_schema 
Publish schema/cred def duration: 9.75s 
Schema: 
  { 
    "sent": { 
      "schema_id": "7eB7xGuxATC2UyF589kk1n:2:employee id schema:18.18.18", 
      "schema": { 
        "ver": "1.0", 
        "id": "7eB7xGuxATC2UyF589kk1n:2:employee id schema:18.18.18", 
        "name": "employee id schema", 
        "version": "18.18.18", 
        "attrNames": [ 
          "name", 
          "position", 
          "date", 
          "employee_id" 
        ], 
        "seqNo": 14 
      } 
    }, 
    "schema_id": "7eB7xGuxATC2UyF589kk1n:2:employee id schema:18.18.18", 
    "schema": { 
      "ver": "1.0", 
      "id": "7eB7xGuxATC2UyF589kk1n:2:employee id schema:18.18.18", 
      "name": "employee id schema", 
      "version": "18.18.18", 
      "attrNames": [ 
        "name", 
        "position", 
        "date", 
        "employee_id" 
      ], 
      "seqNo": 14 
    } 
  } 
Schema ID: 7eB7xGuxATC2UyF589kk1n:2:employee id schema:18.18.18 
Cred def ID: 7eB7xGuxATC2UyF589kk1n:3:CL:14:acme.agent.employee_id_schema 
Publish schema and cred def duration: 14.54s 
```   

21 - Acesse a von-netwrok no browser e localize no canto inferior direito a seção "Ledger State" e acesse o link "Domain". Note que assim como Faber, ACME gerou entradas na blockchain, já que é um agente com a capacidade de emitir credenciais verificáveis. Verifique os campos: 

- Message wrapper 
- Metadata 
- Transaction 
O campo Transaction conterá o atributo "Alias: acme.agent" 

Expanda o campo "raw data" para verificar a estrutura do esquema. 

22 - Para estabelecer comunicação entre Alice e ACME, em Alice escolha a opção 4 para informar um novo convite de conexão 

23 - Em ACME, assim como com Faber, copie os dados de conexão e informe em Alice. Alice exibirá os dados da resposta do convite. 

22 -  O menu do agente ACME deve se parecer com: 
```bash   
Acme       | Connected 
acme.agent handle_connections completed completed 
    (1) Issue Credential 
    (2) Send Proof Request 
    (3) Send Message 
    (X) Exit?                                                                                                                                                                                                                                  

[1/2/3/X]              
```   

No cenário proposto, ACME solicitará de Alice uma apresentação onde está deve prover uma credencial com prova de sua graduação, que foi gerada anteriormente por Faber. Uma vez feita a solicitação, Alice irá responder automaticamente com a credencial apropriada que será validada por ACME. Em seguida, o operador de ACME por sua vez emitirá uma segunda credencial verificável para Alice, através da opção 1, com o cargo de CEO. Podemos observar no código do agente ACME: 

```python   
                agent.cred_attrs[cred_def_id] = { 
                    "employee_id": "ACME0009", 
                    "name": "Alice Smith", 
                    "date": date.isoformat(date.today()), 
                    "position": "CEO" 
                } 
                cred_preview = { 
                    "@type": CRED_PREVIEW_TYPE, 
                    "attributes": [ 
                        {"name": n, "value": v} 
                        for (n, v) in agent.cred_attrs[cred_def_id].items() 
                    ], 
                } 
                offer_request = { 
                    "connection_id": agent.connection_id, 
                    "comment": f"Offer on cred def id {cred_def_id}", 
                    "credential_preview": cred_preview, 
                    "filter": {"indy": {"cred_def_id": cred_def_id}}, 
                } 
                await agent.admin_POST( 
                    "/issue-credential-2.0/send-offer", offer_request 
                ) 
```   

23 - Em ACME selecione a opção 2 

24 - Alice responderá com a credencial de Faber: 

```bash   
#24 Query for credentials in the wallet that satisfy the proof request 
Alice      | No 'by_format' in message: {'connection_id': '678489c3-e4ff-4700-aec9-acd7eccbd101', 'role': 'prover', 'initiator': 'external', 'auto_verify': False, 'thread_id': '2d99ba53-f113-4434-a49d-2f2608bf8194', 'state': 'request-received', 'trace': False, 'created_at': '2024-10-30T06:55:01.257315Z', 'updated_at': '2024-10-30T06:55:01.257315Z', 'pres_ex_id': '837ce7ea-a06c-48c6-aff7-1dae9a92eb79'} 
```
25 - Após a verificação e a emissão da nova credencial verifique no agente Alice o recibemento da mesma. Agora a opção 5 listará duas credenciais que deve parecer como a seguinte:
```bash
All credentials: {'results': [{'referent': '743bd53a-6a4e-4220-8372-9a86a455359b', 'schema_id': 'Aj3WVTqSoLpEwEHJnENwqv:2:degree schema:62.15.36', 'cred_def_id': 'Aj3WVTqSoLpEwEHJnENwqv:3:CL:99:faber.agent.degree_schema', 'rev_reg_id': None, 'cred_rev_id': None, 'attrs': {'timestamp': '1730755630', 'date': '2018-05-28', 'name': 'Alice Smith', 'birthdate_dateint': '20001104', 'degree': 'Maths'}}, {'referent': 'a89f3d49-9bd7-4135-bd3e-e3a85b2acd55', 'schema_id': 'EuCjY2Cbt7WYyVGp4ch3AT:2:employee id schema:10.88.8', 'cred_def_id': 'EuCjY2Cbt7WYyVGp4ch3AT:3:CL:108:acme.agent.employee_id_schema', 'rev_reg_id': None, 'cred_rev_id': None, 'attrs': {'name': 'Alice Smith', 'date': '2024-11-04', 'employee_id': 'ACME0009', 'position': 'CEO'}}]}
``` 

Todos os agentes disponibilizam uma API que pode ser acessada pelo webrowser da máquina host. As portas desta demonstração são sempre 8021 para Faber, 8031 para Alice e 8041 para ACME ou caso tenha passado para os agentes portas diferentes das indicadas na demonstração a API estará diponível na porta +1, exemplo, se Alice estiver ouvindo em 8050 a API estará em 8051. 
Para este exemplo a URL  do localhost é http://192.168.178.172

http://192.168.178.172:8021/api/doc - FABER

http://192.168.178.172:8031/api/doc - ALICE

http://192.168.178.172:8041/api/doc - ACME


![image](https://github.com/user-attachments/assets/90722dd6-5afa-47e5-ace3-63cf9d1fc600)

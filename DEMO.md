# Demonstração Health Institute - Alice Patient - Imunization Center   

### Este é um roteiro de demonstração de agentes Aries com objetivo de observar a emissão e validação de credenciais verificáveis na stack hyperledger assim como a interação dos agentes com a blockchain indy.  
  

### Os Agentes; Health Institute(healthInst), Alice Patient(alice_patient), Bob Patient(bob_patient) e Imunization Center(ImmuCent) são adaptações dos agentes Faber, Alice e ACME fornecidos pela aca-py.org. Para mais informações verificar https://aca-py.org/latest/aca-py.org/  
  

### Health Institute  

Emissor de credenciais: emitirá credenciais para Alice e Bob contendo informações que os classificarão ou não para uma campanha de vacinação, onde Alice será maior de 18 anos e portadora de uma condição especial, simbolizada pelo status 1 e Bob será menor de 18 anos e não portador da condição, simbolizado pelo número 0. A implementação do agente Health Institute também possui um método que permite a validação de credenciais emitidas por ele, no entanto esta função não será explorada nesta demo.  
  

### Alice Patient e Bob Patient 
Pacientes candidatos a uma campanha de vacinação. Tanto Alice quanto Bob solicitarão uma credencial verificavel ao Health Institute contendo prova de sua condição de saúde e idade. Essa será apresentada ao Immunization Center como requisito para uma campanha experimental de vacinação.  


### Immunization Center  
Verificador/Emissor de credencial: Immunization Center solicitará de Alice e Bob uma apresentação verificável onde ambos apresentarão a credencial gerada pelo Health Institute contendo prova de sua idade e condição. Immunization Center também é capaz de emitir uma credencial uma nova credencial contendo a aprovação para a campanha.  


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
LEDGER_URL=http://192.168.178.172:9000 DEFAULT_POSTGRES=true python3 -m alice_patient --port 8030 
```   

06 - Acesse a von-netwrok no browser e localize no canto inferior direito a seção "Ledger State" e acesse o link "Domain". Note que como Alice é um agente do tipo "holder" nenhuma interação é feita com a blockchain, sendo que Alice ainda está aguardando comunicação com Health Institute e Immunization Center que registrarão seus esquemas na blockchain. 

07 - De volta ao terminal, verifique que o agente Alice está rodando e aguardando conexão 
```bash   
#9 Input invitation details 
Invite details:            
```   
08 - Para subir o agente Bob repita os passos 01,02 e 04 Uma vez na pasta runners execute o agente Bob através do comando: 
```bash   
LEDGER_URL=http://192.168.178.172:9000 DEFAULT_POSTGRES=true python3 -m bob_patient --port 8050 
```   

09 - Para subir o agente Health Institution repita os passos 01,02 e 04 Uma vez na pasta runners execute o agente Health Institution através do comando: 
```bash   
LEDGER_URL=http://192.168.178.172:9000 DEFAULT_POSTGRES=true python3 -m healthInst --port 8020 
```   
10 - Observe que no processo de inicialização, o agente Health Institution exibirá o esquema de credencial que registrará na blockchain. Ele deve se parecer com isso: 
```bash   
#3/4 Create a new schema/cred def on the ledger
Schema:
  {
    "sent": {
      "schema_id": "6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27",
      "schema": {
        "ver": "1.0",
        "id": "6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27",
        "name": "health schema",
        "version": "83.72.27",
        "attrNames": [
          "name",
          "date",
          "timestamp",
          "birthdate_dateint",
          "condition"
        ],
        "seqNo": 20
      }
    },
    "schema_id": "6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27",
    "schema": {
      "ver": "1.0",
      "id": "6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27",
      "name": "health schema",
      "version": "83.72.27",
      "attrNames": [
        "name",
        "date",
        "timestamp",
        "birthdate_dateint",
        "condition"
      ],
      "seqNo": 20
    }
  }
  
Schema ID: 6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27
Cred def ID: 6jMNVK6f3WCY31ZL9ZXn5F:3:CL:20:healthInstitute.agent.health_schema
```   

11 - Acesse a von-netwrok no browser e localize no canto inferior direito a seção "Ledger State" e acesse o link "Domain". Note que diferentemente de Alice Patient, Health Institute gerou entradas na blockchain, já que é um agente com a capacidade de emitir credenciais verificáveis. Verifique os campos: 

- Message wrapper 
- Metadata 
- Transaction 
O campo Transaction conterá o atributo "Alias: healthInstitute.agent" 

Expanda o campo "raw data" para verificar a estrutura do esquema. 

12 - De volta ao terminal, verifique que o agente Health Institute está rodando e gerou dados para estabelecer uma conexão, eles devem parecer como o do exemplo:
* ### Não copie os dados aqui apresentados para conexões, utilize os gerados no terminal da própria máquina.

```bash   
Invitation Data: 
{"@type": "https://didcomm.org/out-of-band/1.1/invitation", "@id": "d7036e77-455d-4c37-b6a1-8852dfac8640", "handshake_protocols": ["https://didcomm.org/didexchange/1.0"], "services": [{"id": "#inline", "type": "did-communication", "recipientKeys": ["did:key:z6MkegshLyXJRnyYTCirvPR81J725UBNpJUN9sNZGjpdDY8d"], "serviceEndpoint": "http://localhost:8020"}], "label": "healthInstitute.agent"}
 
```   

13 - Utilize apenas a parte depois de Data: 
```bash   
{"@type": "https://didcomm.org/out-of-band/1.1/invitation", "@id": "d7036e77-455d-4c37-b6a1-8852dfac8640", "handshake_protocols": ["https://didcomm.org/didexchange/1.0"], "services": [{"id": "#inline", "type": "did-communication", "recipientKeys": ["did:key:z6MkegshLyXJRnyYTCirvPR81J725UBNpJUN9sNZGjpdDY8d"], "serviceEndpoint": "http://localhost:8020"}], "label": "healthInstitute.agent"}
 
``` 

Cole no terminal do agente Alice Patient, pressione ENTER para estabelecer uma sessão entre os 2 agentes, liberando os menus de operação em ambos. 

14 -  O menu do agente Alice deve se parecer com: 
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

15 - O menu do agente Health Institute deve se parecer com: 
```bash   
HealthInstitute | Check for endorser role ...
    (1g) Issue Good Credential
    (1b) Issue Bad Credential
    (1a) Set Credential Type (indy)
    (2) Send Proof Request
    (2a) Send *Connectionless* Proof Request (requires a Mobile client)
    (3) Send Message
    (4) Create New Invitation
    (T) Toggle tracing on credential/proof exchange
    (X) Exit?                                                                                                                                                                                                     
[1/2/3/4/T/X]                              
```   

16 - Para testar a comunicação entre agentes, podemos enviar mensagens de Alice para Health Institute ou vice e versa. No exemplo mandaremos um "Hello from Alice" de Alice para Health Institute, escolhendo a opção 3 em Alice, informando a mensagem e verificando a chegada dela em Health Institute. 
```bash  
Alice      | Connected 
Alice      | Check for endorser role ... 
Connect duration: 0.27s 
    (3) Send Message 
    (4) Input New Invitation
    (5) Display All Credentials
    (X) Exit?                                                                                                                                                                                                                                  
[3/4/X] 3                                                                                                                                                                                                                                      
Enter message: Hello from Alice                                                                                                                                                                                                               
Alice      | Received message: health institue.agent received your message 
```   

em Health Institute observa-se: 

```bash  
HealthInstitute      | Connected 
HealthInstitute      | Check for endorser role ... 
HealthInstitute      | Received message: Hello from Alice 

    (1g) Issue Good Credential
    (1b) Issue Bad Credential
    (1a) Set Credential Type (indy)
    (2) Send Proof Request
    (2a) Send *Connectionless* Proof Request (requires a Mobile client)
    (3) Send Message
    (4) Create New Invitation
    (T) Toggle tracing on credential/proof exchange
    (X) Exit?                                                                                                                                                                                                                                                 

[1/2/3/4/T/X]                                      
```   

17 - Em Health Institute emitiremos uma credencial para Alice, que conterá prova de que Alice é maior de idade e possui uma condição especial. No agente Health Institute escolha a opção 1g. Observe em Health Institute: 
```bash  
#13 Issue good credential offer to X
HealthInstitute | Credential: state = offer-sent, cred_ex_id = 1cb8b5b6-7904-4fa1-884f-666681216997
HealthInstitute | Credential: state = request-received, cred_ex_id = 1cb8b5b6-7904-4fa1-884f-666681216997

#17 Issue credential to X
HealthInstitute | Credential: state = credential-issued, cred_ex_id = 1cb8b5b6-7904-4fa1-884f-666681216997
HealthInstitute | Credential: state = done, cred_ex_id = 1cb8b5b6-7904-4fa1-884f-666681216997

```   

18 - Em Alice, observe que o agente foi informado do recebimento de uma credencial: 
```bash  
#15 After receiving credential offer, send credential request
Alice      | No 'by_format' in message: {'connection_id': 'f727d1eb-dc4f-46c3-aac2-e1ec4e0e4d80', 'role': 'holder', 'initiator': 'external', 'auto_offer': False, 'auto_issue': False, 'auto_remove': False, 'thread_id': '53c2a14b-a8ef-4e77-9741-7d3105cc436a', 'state': 'offer-received', 'trace': False, 'created_at': '2024-11-08T15:13:38.449673Z', 'updated_at': '2024-11-08T15:13:38.449673Z', 'cred_ex_id': 'a216a6ee-49de-4197-be9a-39f48b28d0c0'}
Alice      | Credential: state = request-sent, cred_ex_id = a216a6ee-49de-4197-be9a-39f48b28d0c0
Alice      | Credential: state = credential-received, cred_ex_id = a216a6ee-49de-4197-be9a-39f48b28d0c0

#18.1 Stored credential 2cb8fa7d-fcd9-4c79-a398-cfe080ac696e in wallet
Alice      | Credential: state = done, cred_ex_id = a216a6ee-49de-4197-be9a-39f48b28d0c0
Credential details:
  {
    "referent": "2cb8fa7d-fcd9-4c79-a398-cfe080ac696e",
    "schema_id": "6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27",
    "cred_def_id": "6jMNVK6f3WCY31ZL9ZXn5F:3:CL:20:healthInstitute.agent.health_schema",
    "rev_reg_id": null,
    "cred_rev_id": null,
    "attrs": {
      "birthdate_dateint": "20001108",
      "date": "2018-05-28",
      "timestamp": "1731078818",
      "condition": "1",
      "name": "Alice Smith"
    }
  }
  
Alice      | credential_id 2cb8fa7d-fcd9-4c79-a398-cfe080ac696e
Alice      | cred_def_id 6jMNVK6f3WCY31ZL9ZXn5F:3:CL:20:healthInstitute.agent.health_schema
Alice      | schema_id 6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27
```   

19 - Verifique no agente Alice o recibemento da nova credencial. Agora a opção 5 listará uma credencial que deve parecer como a seguinte:
```bash
All credentials: {'results': [{'referent': '2cb8fa7d-fcd9-4c79-a398-cfe080ac696e', 'schema_id': '6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27', 'cred_def_id': '6jMNVK6f3WCY31ZL9ZXn5F:3:CL:20:healthInstitute.agent.health_schema', 'rev_reg_id': None, 'cred_rev_id': None, 'attrs': {'date': '2018-05-28', 'birthdate_dateint': '20001108', 'name': 'Alice Smith', 'timestamp': '1731078818', 'condition': '1'}}]}

```
20 - Em Alice escolha a opção 4 para preparar o agente para futura conexão com o agente Immunization Office

21 - No agente Health Institute escolha a opção 4, usaremos este novo convite para nos conectarmos a Bob

22 - Repita os passos de conexão 13 e 14 para o agente Bob

22 - Novamente o menu do agente Health Institute deve se parecer com: 
```bash   
HealthInstitute | Check for endorser role ...
    (1g) Issue Good Credential
    (1b) Issue Bad Credential
    (1a) Set Credential Type (indy)
    (2) Send Proof Request
    (2a) Send *Connectionless* Proof Request (requires a Mobile client)
    (3) Send Message
    (4) Create New Invitation
    (T) Toggle tracing on credential/proof exchange
    (X) Exit?                                                                                                                                                                                                     
[1/2/3/4/T/X]                              
```   
23 - Em Health Institute emitiremos uma credencial para Bob, que conterá prova de que Bob é menor de idade e não possui uma condição especial. No agente Health Institute escolha a opção 1b. Observe em Health Institute: 
```bash  
#13 Issue bad credential offer to X
HealthInstitute | Credential: state = offer-sent, cred_ex_id = 23da3f78-ad5a-42ca-b89d-8c813c934839
HealthInstitute | Credential: state = request-received, cred_ex_id = 23da3f78-ad5a-42ca-b89d-8c813c934839

#17 Issue credential to X
HealthInstitute | Credential: state = credential-issued, cred_ex_id = 23da3f78-ad5a-42ca-b89d-8c813c934839
HealthInstitute | Credential: state = done, cred_ex_id = 23da3f78-ad5a-42ca-b89d-8c813c934839

```   

24 - Em Bob, observe que o agente foi informado do recebimento de uma credencial: 
```bash  
#15 After receiving credential offer, send credential request
Bob      | No 'by_format' in message: {'connection_id': 'f727d1eb-dc4f-46c3-aac2-e1ec4e0e4d80', 'role': 'holder', 'initiator': 'external', 'auto_offer': False, 'auto_issue': False, 'auto_remove': False, 'thread_id': 'ec4f3c83-e6c8-4a8d-9da8-fdebc39c9480', 'state': 'offer-received', 'trace': False, 'created_at': '2024-11-08T15:22:43.217552Z', 'updated_at': '2024-11-08T15:22:43.217552Z', 'cred_ex_id': 'd3ea0881-43bb-4727-a881-5b5851a633a6'}
Bob      | Credential: state = request-sent, cred_ex_id = d3ea0881-43bb-4727-a881-5b5851a633a6
Bob      | Credential: state = credential-received, cred_ex_id = d3ea0881-43bb-4727-a881-5b5851a633a6

#18.1 Stored credential f7d3ec56-8b47-4154-9501-3659ebf76e47 in wallet
Credential details:
  {
    "referent": "f7d3ec56-8b47-4154-9501-3659ebf76e47",
    "schema_id": "6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27",
    "cred_def_id": "6jMNVK6f3WCY31ZL9ZXn5F:3:CL:20:healthInstitute.agent.health_schema",
    "rev_reg_id": null,
    "cred_rev_id": null,
    "attrs": {
      "name": "Bob Smith",
      "birthdate_dateint": "20141108",
      "date": "2018-05-28",
      "condition": "0",
      "timestamp": "1731079363"
    }
  }
  
Bob      | credential_id f7d3ec56-8b47-4154-9501-3659ebf76e47
Bob      | cred_def_id 6jMNVK6f3WCY31ZL9ZXn5F:3:CL:20:healthInstitute.agent.health_schema
Bob      | schema_id 6jMNVK6f3WCY31ZL9ZXn5F:2:health schema:83.72.27
Bob      | Credential: state = done, cred_ex_id = d3ea0881-43bb-4727-a881-5b5851a633a6

```   
25 - Mesmo tendo a capacidade de verificar a própria credencial, faremos uma solicitação de apresentação de credencial com o agente Immunization Center. Para subir o agente Immunization Center repita os passos 01,02 e 04 Uma vez na pasta runners execute o agente Immunization Center através do comando: 
```bash   
LEDGER_URL=http://192.168.178.172:9000 DEFAULT_POSTGRES=true python3 -m immuCent --port 8040 
```   

26 - Observe que no processo de inicialização, o agente Immunization Center exibirá esquemas de credenciais que registrará na blockchain. Ele deve se parecer com isso: 
```bash   
#3/4 Create a new schema/cred def on the ledger
Schema:
  {
    "sent": {
      "schema_id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:47.13.59",
      "schema": {
        "ver": "1.0",
        "id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:47.13.59",
        "name": "immunization id schema",
        "version": "47.13.59",
        "attrNames": [
          "date",
          "position",
          "patient_id",
          "name"
        ],
        "seqNo": 24
      }
    },
    "schema_id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:47.13.59",
    "schema": {
      "ver": "1.0",
      "id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:47.13.59",
      "name": "immunization id schema",
      "version": "47.13.59",
      "attrNames": [
        "date",
        "position",
        "patient_id",
        "name"
      ],
      "seqNo": 24
    }
  }
  
Schema ID: 4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:47.13.59
Cred def ID: 4BNtF7ULEegATHDPq5qF2F:3:CL:24:immunization.agent.immunization_id_schema
Publish schema/cred def duration: 9.23s
Schema:
  {
    "sent": {
      "schema_id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:16.22.94",
      "schema": {
        "ver": "1.0",
        "id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:16.22.94",
        "name": "immunization id schema",
        "version": "16.22.94",
        "attrNames": [
          "name",
          "patient_id",
          "date",
          "position"
        ],
        "seqNo": 26
      }
    },
    "schema_id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:16.22.94",
    "schema": {
      "ver": "1.0",
      "id": "4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:16.22.94",
      "name": "immunization id schema",
      "version": "16.22.94",
      "attrNames": [
        "name",
        "patient_id",
        "date",
        "position"
      ],
      "seqNo": 26
    }
  }

Schema ID: 4BNtF7ULEegATHDPq5qF2F:2:immunization id schema:16.22.94
Cred def ID: 4BNtF7ULEegATHDPq5qF2F:3:CL:26:immunization.agent.immunization_id_schema
Publish schema and cred def duration: 6.49s

```   

27 - Acesse a von-netwrok no browser e localize no canto inferior direito a seção "Ledger State" e acesse o link "Domain". Note que assim como Health Institute, Immunization Center gerou entradas na blockchain, já que é um agente com a capacidade de emitir credenciais verificáveis. Verifique os campos: 

- Message wrapper 
- Metadata 
- Transaction 
O campo Transaction conterá o atributo "Alias: immunization.agent" 

Expanda o campo "raw data" para verificar a estrutura do esquema. 

28 - Para estabelecer comunicação entre Alice e Immunization Center, em Alice escolha a opção 4 para informar um novo convite de conexão 

29 - Em Immunization Center, assim como com Health Institute, copie os dados de conexão e informe em Alice. Alice exibirá os dados da resposta do convite. 

30 -  O menu do agente Immunization Center deve se parecer com: 
```bash   
Immunization | Connected
immunization.agent handle_connections completed completed
    (1) Issue Credential
    (2) Send Proof Request
    (3) Send Message
    (4) Create New Invitation
    (X) Exit?                                                                                                                                                                                                     
[1/2/3/X]                       
```   

No cenário proposto, Immunization Center solicitará de Alice uma apresentação onde está deve prover uma credencial com prova de sua idade e condição especial, que foi gerada anteriormente por Healt Institute. Uma vez feita a solicitação, Alice irá responder automaticamente com a credencial apropriada que será validada. Em seguida, o operador de Immunization Center por sua vez emitirá uma segunda credencial verificável para Alice, através da opção 1, com o identificação positiva para a campanha. Podemos observar no código do agente Immunization Center: 

```python   
                agent.cred_attrs[cred_def_id] = {
                    "patient_id": "IMMUN0009",
                    "name": "Alice Smith",
                    "date": datetime.date.today().strftime("%Y-%m-%d"),
                    "position": "APPROVED"
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

31 - Em Immunization Center selecione a opção 2 

32 - Alice responderá com a credencial gerada por Health Institute: 

```bash   
Presentation: message =  {'connection_id': '3864de0e-5e87-44b2-b103-d182b9548e33', 'role': 'prover', 'initiator': 'external', 'auto_verify': False, 'thread_id': '284e5599-52f5-421d-84c3-3791b9fc23d4', 'state': 'request-received', 'trace': False, 'created_at': '2024-11-08T16:40:38.917609Z', 'updated_at': '2024-11-08T16:40:38.917609Z', 'pres_ex_id': 'faf8e561-16b3-496a-9bb1-90cb5c421714'}
Presentation: state =  request-received
Presentation: pres_ex_id =  faf8e561-16b3-496a-9bb1-90cb5c421714
Alice      | Presentation: state = request-received, pres_ex_id = faf8e561-16b3-496a-9bb1-90cb5c421714

#24 CONTAINER Query for credentials in the wallet that satisfy the proof request
Alice      | No 'by_format' in message: {'connection_id': '3864de0e-5e87-44b2-b103-d182b9548e33', 'role': 'prover', 'initiator': 'external', 'auto_verify': False, 'thread_id': '284e5599-52f5-421d-84c3-3791b9fc23d4', 'state': 'request-received', 'trace': False, 'created_at': '2024-11-08T16:40:38.917609Z', 'updated_at': '2024-11-08T16:40:38.917609Z', 'pres_ex_id': 'faf8e561-16b3-496a-9bb1-90cb5c421714'}
Presentation: state = request-received, pres_ex_id = faf8e561-16b3-496a-9bb1-90cb5c421714

```
33 - Com a verificação realizada, o operador de Immunization Center pode gerar uma nova credencial para Alice selecionando a opção 1
```bash
#13 Issue credential offer to X
Immunization | Credential: state = offer-sent, cred_ex_id = 80f31de8-950f-4e84-a722-3f33a08c677c
Immunization | Credential: state = request-received, cred_ex_id = 80f31de8-950f-4e84-a722-3f33a08c677c
Immunization | Credential: state = credential-issued, cred_ex_id = 80f31de8-950f-4e84-a722-3f33a08c677c
Immunization | Credential: state = done, cred_ex_id = 80f31de8-950f-4e84-a722-3f33a08c677c
``` 

34 - Após a verificação e a emissão da nova credencial verifique no agente Alice o recibemento da mesma: 
```bash
#15 After receiving credential offer, send credential request
Alice      | No 'by_format' in message: {'connection_id': '3864de0e-5e87-44b2-b103-d182b9548e33', 'role': 'holder', 'initiator': 'external', 'auto_offer': False, 'auto_issue': False, 'auto_remove': False, 'thread_id': '6da284c4-66fa-4ccd-89ac-dfbbc6308021', 'state': 'offer-received', 'trace': False, 'created_at': '2024-11-08T16:47:05.516422Z', 'updated_at': '2024-11-08T16:47:05.516422Z', 'cred_ex_id': 'fac740df-dfc1-43b6-8d40-32be7a85e2b3'}
Alice      | Credential: state = request-sent, cred_ex_id = fac740df-dfc1-43b6-8d40-32be7a85e2b3
Alice      | Credential: state = credential-received, cred_ex_id = fac740df-dfc1-43b6-8d40-32be7a85e2b3

#18.1 Stored credential 65134589-ed80-4343-ad53-ed9ac82774cd in wallet
Credential details:
  {
    "referent": "65134589-ed80-4343-ad53-ed9ac82774cd",
    "schema_id": "BAjHxoChwzMvdogdRyrvaf:2:immunization id schema:98.76.68",
    "cred_def_id": "BAjHxoChwzMvdogdRyrvaf:3:CL:42:immunization.agent.immunization_id_schema",
    "rev_reg_id": null,
    "cred_rev_id": null,
    "attrs": {
      "name": "Alice Smith",
      "date": "2024-11-08",
      "position": "APPROVED",
      "patient_id": "IMMUN0009"
    }
  }
  

``` 

Agora a opção 5 listará duas credenciais que deve parecer como a seguinte:

```bash
All credentials: {'results': [{'referent': '74429c6c-93ad-457a-b8fc-89ec5e07ece5', 'schema_id': 'VeBrp2W8QMaiCeqsVzxpwS:2:health schema:39.2.95', 'cred_def_id': 'VeBrp2W8QMaiCeqsVzxpwS:3:CL:36:healthInstitute.agent.health_schema', 'rev_reg_id': None, 'cred_rev_id': None, 'attrs': {'timestamp': '1731083813', 'date': '2018-05-28', 'condition': '1', 'name': 'Alice Smith', 'birthdate_dateint': '20001108'}}, {'referent': '65134589-ed80-4343-ad53-ed9ac82774cd', 'schema_id': 'BAjHxoChwzMvdogdRyrvaf:2:immunization id schema:98.76.68', 'cred_def_id': 'BAjHxoChwzMvdogdRyrvaf:3:CL:42:immunization.agent.immunization_id_schema', 'rev_reg_id': None, 'cred_rev_id': None, 'attrs': {'position': 'APPROVED', 'date': '2024-11-08', 'patient_id': 'IMMUN0009', 'name': 'Alice Smith'}}]}

```
* Repita os passos 28,29,30,31 e 32 com a agente Bob e verifique que por não atender as condiçãoes desejadas este não será verificado

Todos os agentes disponibilizam uma API que pode ser acessada pelo webrowser da máquina host. As portas desta demonstração são sempre 8021 para Health Institute, 8031 para Alice, 8051 para Bob e 8041 para Immunization Center ou caso tenha passado para os agentes portas diferentes das indicadas na demonstração a API estará disponível na porta +1, exemplo, se Alice estiver ouvindo em 8050 a API estará em 8051. 
Para este exemplo a URL  do localhost é http://192.168.178.172

http://192.168.178.172:8021/api/doc - HEALTH INSTITUTE

http://192.168.178.172:8031/api/doc - ALICE

http://192.168.178.172:8051/api/doc - BOB

http://192.168.178.172:8041/api/doc - IMMUNIZATION CENTER

![image](https://github.com/user-attachments/assets/04834245-62ea-4e60-bdc9-dddccfd7fdfa)



Vejamos um exemplo de como podemos consultaR as credenciais armazenadas de Alice:

1 - Acesse http://192.168.178.172:8031/api/doc

2 - Localize a opção: "GET / credentials" e informe os campos para o número de credenciais o índice de procura e deixe WQL no terceiro campo
![image](https://github.com/user-attachments/assets/342d155b-7cf6-42ba-8e04-e7a952b3baa0)

3 - Clique em "EXECUTE"

4 - Role a página e confira as credenciais no corpo da resposta:

![image](https://github.com/user-attachments/assets/b07d92b4-234c-478b-a092-048e27bc83dc)


* Mais informações de como utilizar a API podem ser encontradas nos links acima das opções da mesma:
![image](https://github.com/user-attachments/assets/cdb89631-aeab-4722-b81e-3620d0a10223)







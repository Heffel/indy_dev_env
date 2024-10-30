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

Para a realização desta demonstração, algumas modificações devem ser aplicadas a bibliotecas e agentes. O roteiro a seguir contém os passos para execução dela.  

01 - Modificando aiohttp: A lib aiohttp instalada durante o setup da máquina virtual conta com um parâmetro extra de entrada que não é esperado pela implementação do aca-py e deve ser removido para a demonstração. Para isto usaremos a ferramenta vi contida na instalação do ubunto OS.  

01.1 - Do diretório home/vagrant da máquina virtual informe:  
```bash  
sudo vi /home/vagrant/.local/lib/python3.8/site-packages/aiohttp/client_reqrep.py  
```  

01.2 - Uma vez visualizando a lib digite  
```bash  
/@attr.s  
```  

'/' é o comando de busca  

'@attr.s' é o texto que estamos procurando dentro da lib, uma vez encontrado veremos o trecho de código:  

```python  
	@attr.s(auto_attribs=True, frozen=True, slots=True, cache_hash=True)  
	class ContentDisposition:  
    	type: Optional[str]  
    	parameters: "MappingProxyType[str, str]"  
    	filename: Optional[str]  
```  

01.3 - Aperte a tecla ENTER para sair do modo localização. Navegue com o direcional até ', cache_hash=True' e apague o parâmetro, resultando em:  

```python  
	@attr.s(auto_attribs=True, frozen=True, slots=True)  
	class ContentDisposition:  
    	type: Optional[str]  
    	parameters: "MappingProxyType[str, str]"  
    	filename: Optional[str]  
```  

uma vez feita e edição, para salvar as modificações digite:  
```bash  
:wq  
```  

':' informar função ao vi  

'w' write/escrever  

'q' quit/sair  

* acesse novamente o arquivo da lib e navegue até o trecho modificado para verificar se o arquivo foi de fato alterado. Para simplesmente sair do arquivo informe:  
```bash  
:q  
```  

02 - Copiando os agentes demo para a pasta lab: Como descrito no arquivo [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md) a maquina virtual possui um diretório "lab" que está mapeado para o nível acima do diretório do projeto. O diretório "lab" permite interação de elementos da máquina host, como IDEAs, com elementos que podem ser vistos da máquina virtual. Copiaremos os agentes providos para o diretório "lab" e os executaremos de lá. Podemos fazer isto de duas formas: 

2a - Copiar a pasta 'runners' através do navegador de arquivos da máquina host 
- 02a.1 - Através do navegador de arquivos da máquina host, localize o diretório do projeto.  
- 02a.2 - Acessando o diretório do projeto localize a pasta "runners" 
- 02a.3 - Copie a pasta "runners" para o nível acima da pasta do projeto.  

	Exemplo: se a pasta do projeto está salva em  
	C:/media/user/projetos/indy_dev_env/ 
	copie a pasta "runners" para 
	C:/media/user/projetos/ 

###OU 

2b - Copiar a pasta 'runners' através da linha de comando da máquina virtual: 
- 02b.1 - Na máquina virtual certifique-se que está no diretório home/vagrant. Digite: 

```bash  
cd ~ 
```  

- 02b.2 - Informe o seguinte comando 
```bash  
cp -r ../../lab/indy_dev_env/runners/ ../../lab/runners 
```  


03 - Modificando os agentes aca-py.org: os agentes fornecidos pela aca-py foram idealizados para serem executados em localhost, e, portanto, procurar a blockchain von-network em localhost:9000. No entanto, como estaremos os executando de uma máquina virtual, e como vimos em [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md) a blockchain não estará escutando em localhost:9000, logo devemos informar o ip correto para que os agentes possam encontrar o gênesis file de nossa von-network. 

- 03.1 - Na máquina virtual certifique-se que a von-network esteja up. Instruções para o mesmo estão em [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md) 


- 03.2 - Com a von-network up, obtenha o seu endereço, novamente com as instruções em [README.md](https://github.com/Heffel/indy_dev_env/blob/master/README.md). Para este exemplo, o ip onde se encontra a von-network é 192.168.178.172:9000 

- 03.3 - Na máquina virtual, do diretório home/vagrant navegue até 'lab' informando: 

```bash  
cd ../../lab/ 
```  

- 03.4 - Uma vez em 'lab' acesse o arquivo support/agent.py: 
```bash  
sudo vi runners/support/agent.py 
```  

Localize a variável LEDGER_URL 

```bash  
/LEDGER_URL 
```  

Uma vez localizada a variável LEDGER_URL o trecho de código encontrado deve se parecer com o seguinte: 

```python  
GENESIS_URL = os.getenv("GENESIS_URL") 
LEDGER_URL = os.getenv("LEDGER_URL") 
GENESIS_FILE = os.getenv("GENESIS_FILE")	 
```  

- 03.4 - Aperte a tecla ENTER para sair do modo localização. Navegue com o direcional até o valor passado. Aperte a tecla "i" para iniciar o modo "insert" identificado pelo valor "-- INSERT --" mostrado no rodapé do arquivo. Acrescente o ip obtido para a von-network, para este exemplo 192.168.178.172:9000. Após a modificação, aperte a tecla ESC para encerrar o modo "insert", verifique que "-- INSERT --" não mais aparece no rodapé da página. Agora o código deve parecer com: 
```python  
GENESIS_URL = os.getenv("GENESIS_URL") 
LEDGER_URL = os.getenv("LEDGER_URL", "http://192.168.178.172:9000") 
GENESIS_FILE = os.getenv("GENESIS_FILE")	 
```  

uma vez feita e edição, para salvar as modificações digite:  

```bash  
:wq  
```  
* acesse novamente o arquivo da lib e navegue até o trecho modificado para verificar se o arquivo foi de fato alterado. Para simplesmente sair do arquivo informe:  
```bash  
:q  
```  
Com esses passos realizados estamos prontos para executar a demonstração. 
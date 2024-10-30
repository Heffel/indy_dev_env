# Demonstração Faber - Alice - ACME 

## Este é um roteiro de demonstração de agentes Aries com objetivo de observar a emissão e validação de credenciais verificaveis na stack hyperledger assim como a interação dos agente com a blockchain indy.

## Os Agentes; Faber, Alice e Acme são adaptações dos agentes de mesmo nome fornecidos pela aca-py.org. Para mais informações verificar https://aca-py.org/latest/aca-py.org/

### Faber - Emissor de credencial: emitirá credencial para Alice contendo formação academica. A implementação do agente Faber também permite a validação de credenciais, no entanto esta função não será explorada nesta demo.

### Alice - Estudante formada na Faber University. Alice solicitará uma credencial verificavel a Faber contendo prova de sua formação acadêmica. Essa será apresentada a ACME como requisito para uma candidatura de emprego.

### ACME - Verificador/Emissor de credencial: ACME solicitará de Alice uma apresentação verificavel onde Alice apresentará a credencial gerada por Faber contendo prova de sua formação acadêmica. ACME será capaz de verificar a credencial e como resultado emitir uma nova credencial contendo o cargo de Alice.

## SETUP

Para a realização desta demonstração, algumas modificações devem ser aplicadas a bibliotecas e agentes. O roteiro a seguir contém os passos para execução do mesmo.

01 - Modificando aiohttp: A lib aiohttp instalada durante o setup da maquina virtual conta com um parâmetro extra de entrada que não é esperada pela implementação do aca-py e deve ser removido para a demonstração. Para isto usaremos a ferramenta vi contida na instalçaão do ubunto OS.
	01.1 - Do dirtório home da máquina virtual informe:
```bash
sudo vi /home/vagrant/.local/lib/python3.8/site-packages/aiohttp/client_reqrep.py
```
	01.2 - uma vez visualizando a lib digite

```bash
/@attr.s
```

	'/' é o comando de busca
	'@attr.s' é o texto que estamos procurando dentro da lib
	uma vez encontrado @attr.s veremos o trecho de código:

```python

	@attr.s(auto_attribs=True, frozen=True, slots=True, cache_hash=True)
	class ContentDisposition:
    	type: Optional[str]
    	parameters: "MappingProxyType[str, str]"
    	filename: Optional[str]
```
	navegue com o direcional até ', cache_hash=True' e apague o parâmtro, resultando em:

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

	* acesse novamente o arquivo da lib e navegue até o trecho modiificado para verificar se o arquivo foi de fato alterado. Para simplesmente sair do arquivo informe:

```bash
:wq
```


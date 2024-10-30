# indy_dev_env 

## Virtual Machine Based Environment for Hyperledger Indy SDK ZKP experimentation

Esse ambiente é contruído baseado em Vagrant 2.2.19 | Virtualbox 6.1.50   

Uma vez que o download do repo tenha sido efetuado: 

01 - Instalar vagrant na máquina host: https://www.vagrantup.com/ 

02 - Instalar virtual box: https://www.virtualbox.org/wiki/Download_Old_Builds_6_1 (vagrant ainda não possui suporte para versões 7.x) 

03 - Abra uma linha de comando na pasta principal do projeto, onde se encontra o arquivo "Vagrantfile" 

04 - No terminal informe "vagrant up" para iniciar a criação da VM que pode ser monitorado pela interface do Virtual Box 

```bash
vagrant up
```

05 - A máquina virtual será criada com a placa de rede em modo bridge, o que significa que ela pegará um IP próprio e as portas ocupadas por aplicações rodando nela ocuparão as portas da máquina host. No caso de a máquina host possuir mais de uma interface de rede, o vagrant solicitará que o usuário escolha qual ele deve usar enquanto instala ou inicia a máquina, como demonstrado abaixo. Escolha aquela com conexão á internet.
```bash
==> indy-dev-env: Available bridged network interfaces:
1) eth0
2) virbr0
3) docker0
4) br-dd197467ceff
==> indy-dev-env: When choosing an interface, it is usually the one that is
==> indy-dev-env: being used to connect to the internet.
``` 

06 - Uma vez criada a máquina virtual, o vagrant fara através do ansible o download de todas os SDKs (Indy-SDK), dependencias, libs python como o ares-askar e o indy-crypto, além da instalação de ferramentas como docker, docker-compose-plugin, pip, python 3.8, whois, curl, acesso ao sistema de arquivos da máquina host e mais todo o ferramental contido em uma instalação ubunto. 

07 - Uma vez terminada a instalação, cerca de 8 minutos, informe no terminal o comando "vagrant ssh" para acessar a máquina virtual.
```bash
vagrant ssh
``` 

08 - O ambiente da máquina virtual trata-se de um ubuntu/bionic64 e o desenvolvedor estará pode verificar que está no diretório "/home/vagrant" com comando pwd
```bash
pwd
```
09 - O comando "ls -l" mostrará a pasta "von-network" que se trata de uma blockchain experimental Hyperledger Indy constituída de 4 nós que roda localmente e estará acessível na porta 9000 quando estiver rodando. Para mais informações sobre von-network consulte: https://github.com/bcgov/von-network e https://github.com/bcgov/von-network/blob/main/docs/UsingVONNetwork.md 

10 - Acesse a pasta "von-network". 
```bash
cd von-network
```

11 - Na pasta "von-network" informe o comando seguinte para iniciar o download de componentes da imagem. 
```bash
sudo ./manage build
```
12 - Uma vez concluído o download, para subir a rede local informe o comando 
```bash 
sudo ./manage start --logs
``` 
Caso alertas de incompatibilidade sejam logados, estes podem ser considerados, versões mais recentes das libs estão já instaladas no sistema e são retrocompatíveis. 

13 - Ao fim do processo, o terminal continuará a exibir logs dos nós, aperte as teclas "Ctrl C" para recuperar o acesso ao terminal. A rede continuará rodando em modo destacado. Para voltar a ver logs informe "sudo ./manage logs" na pasta "von-network".  

14 - Para interagir com a interface da rede "von-network" informe o comando:
 ```bash 
ip --color a 
``` 
para mostrar o ip o qual será o local host da máquina virtual. Lembre-se, mesmo informando localhost:9000 no browser, ele não mostrará a von-network, esta escutará na porta 9000 porém no ip da máquina virtual, como por exemplo em 192.168.178.172:9000. O ip da sua máquina virtual geralmente será o terceiro listado na opção inet. Informe o ip obtido, com a porta 9000 como no exemplo previamente citado. 

15 - Na interface von-network é possível obter o JSON Genesis da blockchain, registrar DIDs, etc. As transações também podem ser observadas no link "Domain" em "Ledger State" 

16 - Para parar a von network, retorne ao terminal e informe 
```bash 
sudo ./manage stop
``` 
Para reiniciar informe
```bash 
sudo ./manage start 
``` 
Para parar a rede e apagar todos os registros informe
```bash 
sudo ./manage down
``` 
Para mais informações consulte: https://github.com/bcgov/von-network e https://github.com/bcgov/von-network/blob/main/docs/UsingVONNetwork.md. 

17 - Caso o desenvolvedor resolva não utilizar o von-network local, uma versão da rede roda permanentemente no endereço http://test.bcovrin.vonx.io/ . No entanto essa versão é periodicamente limpa, sendo que seus registros são apagados semanalmente.  

18 - Uma vez verificado a von network, retorne ao home informando
```bash 
cd ~
``` 
19 - Na home, liste todos os containers docker ativos com o comando: 
```bash 
sudo docker ps
``` 
20 - Identifique o container portgres "some-postgres", este é o container contendo a imagem default postgres disponibilizado pelo docker. Ele é usado pelo aries-askar como "wallet", lembrando que neste contexto, a hyperledger refere-se a wallet como onde qualquer agente aries guarda informações sensíveis e não necessariamente a um aplicativo "wallet" de acordo com o mapeamento fornecido no arquivo playbook ele escutará na porta 5432. Para mais sobre docker acesse: https://docs.docker.com/reference/cli/docker/ 

21 - Para verificar a instalação com sucesso das libs contidas pelo Indy SDK, assim como lib python importantes e outras dependências verifique o arquivo "checklist" no diretório principal do projeto. Informe os comandos individualmente no terminal para s libs. 

22 - Verifique a versão ativa do python com o comando
```bash 
python3 --version
``` 
que deve retornar a versão ativa do python "3.8". Esta instalação também contém as versões 3.6 e 2.7 para uso caso necessário.

23 - Instale a lib python ares-cloudagent através do seguinte comando
```bash 
pip install aries-cloudagent
```  
Devido a limitações da ferramenta de automação, ela deve ser instalada uma vez que a maquina virtual já esteja rodando. A versão instalada do aries-cloudagent deve ser 0.8.2.

24 - Para listar todas as libs python instaladas com sucesso informe:
```bash 
pip freeze
```  
Verifique que todas as libs python contidas no arquivo checklist devem estar instaladas e na versão informada. 

25 - Ainda em home navegue até o diretório "lab" informand o comando
```bash 
cd ../../lab
```  
Uma vez em lab informe o comando "ls -l" e verifique que todos os diretórios acima do diretório do projeto git na máquina host serão listados. O diretório "lab" é o acesso da VM a máquina host, qualquer arquivo pode ser copiado para dentro e fora da VM através dele. 

26 - Por fim, o ambiente roda sobre um linux ubunto com todas as capacidades, sendo possível instalar qualquer biblioteca, programa, dependência suportada pelo sistema. A VM criada é listada no Virtual Box e pode ser modificado por lá, aumentando RAM, armazenagem, processamento etc. Caso o desenvolvedor tenha conhecimento de vagrant + ansible os arquivos de ambos podem ser modificados para se adequarem a necessidade dele. 

27 - O comando "exit" retira o desenvolvedor da máquina vagrant, que continuará rodando. Uma vez fora, "vagrant halt" para a máquina virtual, assim como os serviços dela. O comando “vagrant up” sobe a VM novamente. O comando "vagrant reload" roda novamente a instalação e por fim "vagrant destroy" destrói a VM. Para uma lista de comandos acesse: https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4 
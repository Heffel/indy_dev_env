# indy\_dev\_env

## Virtual Machine Based Environment for Hyperledger Indy SDK ZKP Experimentation

This environment is built based on Vagrant 2.2.19 | VirtualBox 6.1.50

Once the repository download has been completed:

01 - Install Vagrant on the host machine: [https://www.vagrantup.com/](https://www.vagrantup.com/)

02 - Install VirtualBox: [https://www.virtualbox.org/wiki/Download\_Old\_Builds\_6\_1](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1) (Vagrant does not yet support version 7.x)

03 - Open a command line in the project's root folder, where the "Vagrantfile" is located.

04 - In the terminal, enter "vagrant up" to start creating the VM, which can be monitored through the VirtualBox interface.

```bash
vagrant up
```

05 - The virtual machine will be created with the network adapter in bridge mode, meaning it will obtain its own IP, and applications running on it will occupy the host machine's ports. If the host machine has multiple network interfaces, Vagrant will prompt the user to choose one during installation or startup, as shown below. Choose the one with an internet connection.

```bash
==> indy-dev-env: Available bridged network interfaces:
1) eth0
2) virbr0
3) docker0
4) br-dd197467ceff
==> indy-dev-env: When choosing an interface, it is usually the one that is
==> indy-dev-env: being used to connect to the internet.
```

06 - Once the virtual machine is created, Vagrant, through Ansible, will download all SDKs (Indy-SDK), dependencies, Python libraries such as ares-askar and indy-crypto, as well as install tools like Docker, docker-compose-plugin, pip, Python 3.8, whois, curl, access to the host machine’s file system, and all necessary tools in an Ubuntu installation.

07 - Once installation is complete, which takes about 8 minutes, enter the following command in the terminal to access the virtual machine:

```bash
vagrant ssh
```

08 - The virtual machine environment is based on Ubuntu/Bionic64. The developer can verify they are in the "/home/vagrant" directory by using the command:

```bash
pwd
```

09 - The command "ls -l" will display the "von-network" folder, which is an experimental Hyperledger Indy blockchain consisting of four nodes running locally. It will be accessible on port 9000 when active. For more information about von-network, visit: [https://github.com/bcgov/von-network](https://github.com/bcgov/von-network) and [https://github.com/bcgov/von-network/blob/main/docs/UsingVONNetwork.md](https://github.com/bcgov/von-network/blob/main/docs/UsingVONNetwork.md)

10 - Access the "von-network" folder:

```bash
cd von-network
```

11 - In the "von-network" folder, enter the following command to start downloading the image components:

```bash
sudo ./manage build
```

12 - Once the download is complete, start the local network using:

```bash
sudo ./manage start --logs
```

If incompatibility warnings appear, they can be ignored as newer versions of the libraries are installed and are backward compatible.

13 - At the end of the process, the terminal will continue displaying node logs. Press "Ctrl + C" to regain terminal access. The network will keep running in detached mode. To view logs again, enter "sudo ./manage logs" in the "von-network" folder.

14 - To interact with the "von-network" interface, enter:

```bash
ip --color a
```

This will display the IP, which serves as the virtual machine's localhost. Even if "localhost:9000" is entered in the browser, it will not display the von-network. Instead, it listens on port 9000 but at the virtual machine's IP, such as 192.168.178.172:9000. The virtual machine’s IP is usually the third listed under "inet." Use the obtained IP with port 9000 as previously mentioned.

15 - The von-network interface allows obtaining the Genesis JSON of the blockchain, registering DIDs, etc. Transactions can also be observed under the "Domain" link in "Ledger State."

16 - To stop the von-network, return to the terminal and enter:

```bash
sudo ./manage stop
```

To restart it, enter:

```bash
sudo ./manage start
```

To stop the network and delete all records, enter:

```bash
sudo ./manage down
```

For more information, visit: [https://github.com/bcgov/von-network](https://github.com/bcgov/von-network) and [https://github.com/bcgov/von-network/blob/main/docs/UsingVONNetwork.md](https://github.com/bcgov/von-network/blob/main/docs/UsingVONNetwork.md).

17 - If the developer chooses not to use the local von-network, a version of the network runs permanently at [http://test.bcovrin.vonx.io/](http://test.bcovrin.vonx.io/). However, this version is periodically reset, with records deleted weekly.

18 - Once the von-network is verified, return to "home/vagrant" by entering:

```bash
cd ~
```

19 - In the home directory, list all active Docker containers with:

```bash
sudo docker ps
```

20 - Identify the "some-postgres" container, which is the default PostgreSQL image provided by Docker. It is used by Aries-Askar as a "wallet"—in this context, Hyperledger refers to a wallet as where any Aries agent stores sensitive information rather than a typical "wallet" application. According to the playbook file mapping, it listens on port 5432. For more on Docker, visit: [https://docs.docker.com/reference/cli/docker/](https://docs.docker.com/reference/cli/docker/)

21 - To verify the successful installation of Indy SDK libraries, important Python libraries, and other dependencies, check the "checklist" file in the project's root directory. Enter the listed commands individually in the terminal.

22 - Check the active Python version with:

```bash
python3 --version
```

This should return "3.8" as the active Python version. The installation also includes versions 3.6 and 2.7 for use if needed.

23 - Install the Python library "aries-cloudagent" using the following command:

```bash
pip install aries-cloudagent==0.8.2
```

Due to automation tool limitations, it must be installed after the virtual machine is running. The installed version of aries-cloudagent should be 0.8.2.

24 - To list all successfully installed Python libraries, enter:

```bash
pip freeze
```

Ensure that all Python libraries listed in the "checklist" file are installed and match the specified versions.

25 - Still in the home directory, navigate to the "lab" directory by entering:

```bash
cd ../../lab
```

Once inside "lab," enter "ls -l" and verify that all directories above the Git project directory on the host machine are listed. The "lab" directory provides VM access to the host machine, allowing file transfers in and out of the VM.

26 - The environment runs on an Ubuntu Linux system with full capabilities, allowing the installation of any supported libraries, programs, or dependencies. The created VM is listed in VirtualBox and can be modified there, including increasing RAM, storage, and processing power. If the developer is familiar with Vagrant and Ansible, their configuration files can be modified to suit specific needs.

27 - The "exit" command logs the developer out of the Vagrant machine, which will keep running. Once outside, "vagrant halt" stops the virtual machine and its services. The "vagrant up" command restarts the VM, "vagrant reload" reruns the installation, and "vagrant destroy" deletes the VM. For a list of commands, visit: [https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4](https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4)


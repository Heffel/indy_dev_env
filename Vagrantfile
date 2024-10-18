# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  config.vm.define "indy_dev_env"
  config.vm.hostname = "indy_dev_env"
  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/bionic64"
  config.vm.provider :virtualbox do |vb|
        vb.name = "indy_dev_env"
    end

  config.vm.synced_folder "../", "/lab", type: "virtualbox"

  #config.vm.network "forwarded_port", guest: 9000, host: 9000
  #config.vm.network "forwarded_port", guest: 8010, host: 8010
  #config.vm.network "forwarded_port", guest: 8011, host: 8011
  #config.vm.network "forwarded_port", guest: 8012, host: 8012
  #config.vm.network "forwarded_port", guest: 8013, host: 8013
  #config.vm.network "forwarded_port", guest: 8014, host: 8014
  #config.vm.network "forwarded_port", guest: 8015, host: 8015
  #config.vm.network "forwarded_port", guest: 8016, host: 8016
  #config.vm.network "forwarded_port", guest: 8017, host: 8017
  #config.vm.network "forwarded_port", guest: 8018, host: 8018
  #config.vm.network "forwarded_port", guest: 8019, host: 8019
  #config.vm.network "forwarded_port", guest: 8020, host: 8020
  #config.vm.network "forwarded_port", guest: 8021, host: 8021
  #config.vm.network "forwarded_port", guest: 8022, host: 8022
  #config.vm.network "forwarded_port", guest: 8023, host: 8023
  #config.vm.network "forwarded_port", guest: 8024, host: 8024
  #config.vm.network "forwarded_port", guest: 8025, host: 8025
  #config.vm.network "forwarded_port", guest: 8026, host: 8026
  #config.vm.network "forwarded_port", guest: 8027, host: 8027
  #config.vm.network "forwarded_port", guest: 8028, host: 8028
  #config.vm.network "forwarded_port", guest: 8029, host: 8029
  #config.vm.network "forwarded_port", guest: 8030, host: 8030
  #config.vm.network "forwarded_port", guest: 8031, host: 8031
  #config.vm.network "forwarded_port", guest: 8032, host: 8032
  #config.vm.network "forwarded_port", guest: 8033, host: 8033
  #config.vm.network "forwarded_port", guest: 8034, host: 8034
  #config.vm.network "forwarded_port", guest: 8035, host: 8035
  #config.vm.network "forwarded_port", guest: 8036, host: 8036
  #config.vm.network "forwarded_port", guest: 8037, host: 8037
  #config.vm.network "forwarded_port", guest: 8038, host: 8038
  #config.vm.network "forwarded_port", guest: 8039, host: 8039
  #config.vm.network "forwarded_port", guest: 8040, host: 8040
  #config.vm.network "forwarded_port", guest: 8041, host: 8041
  #config.vm.network "forwarded_port", guest: 8042, host: 8042
  #config.vm.network "forwarded_port", guest: 8043, host: 8043
  #config.vm.network "forwarded_port", guest: 8044, host: 8044
  #config.vm.network "forwarded_port", guest: 8045, host: 8045
  #config.vm.network "forwarded_port", guest: 8046, host: 8046
  #config.vm.network "forwarded_port", guest: 8047, host: 8047
  #config.vm.network "forwarded_port", guest: 8048, host: 8048
  #config.vm.network "forwarded_port", guest: 8049, host: 8049
  #config.vm.network "forwarded_port", guest: 8050, host: 8050
  config.ssh.insert_key = false
  config.ssh.forward_agent = true

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
   config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   sudo apt-get update
  #   sudo apt-get install -y apache2
  # SHELL

  config.vm.provision "shell", inline: 
    #"sudo yum install -y epel-release; 
    #sudo yum install -y ansible;
    #sudo yum install -y kernel-headers;
    #sudo yum install -y kernel-devel;
    #sudo yum install -y elfutils-libelf-devel"
    "sudo apt update; 
    sudo apt-get install -y unzip; 
    sudo apt-get install -y ansible"
    #mount -t vboxsf -o uid=`id -u vagrant`,gid=`id -g vagrant` vagrant /vagrant"
 
  config.vm.provision "ansible_local" do |ansible|
    ansible.verbose = true
    ansible.playbook = "playbook.yml"
    #ansible.inventory_path = "ansible_hosts"
  end
end

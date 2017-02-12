# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "forwarded_port", guest: 9200, host: 9200
  config.vm.network "forwarded_port", guest: 5601, host: 5601
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
  end

config.vm.provision "shell", run: "once", inline: <<-SHELL
    apt-get update && apt-get -y upgrade
    curl https://get.docker.com | sh
    usermod -aG docker ubuntu
    systemctl restart docker
    docker network create esnet
#    docker volume create --name data1
#    docker volume create --name data2
    cd /vagrant/elasticsearch
    docker build -t elasticsearch_with_plugins:2.4.4 .
    cd /vagrant/kibana
    docker build -t kibana_with_plugins:4.6.4 .
SHELL

config.vm.provision "shell", run: "always", inline: <<-SHELL
    docker run -d --rm --name es1 --net esnet -v  /vagrant/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml -p9200:9200 elasticsearch_with_plugins:2.4.4 -Des.node.name="es1"
    docker run -d --rm --name es2 --net esnet -v  /vagrant/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml elasticsearch_with_plugins:2.4.4 -Des.node.name="es2"
    docker run -d --rm --name kibana --net esnet -p5601:5601 -e ELASTICSEARCH_URL=http://es1:9200 kibana_with_plugins:4.6.4
SHELL

end

Vagrant.configure("2") do |config|
    config.ssh.keys_only = true
    config.ssh.insert_key = false
    config.ssh.private_key_path = 'vagrant_key'

    config.vm.define "ubuntu32" do |ubuntu32|

    ubuntu32.vm.box = "ubuntu/trusty32"
    # ubuntu32.vm.hostname = 'ubuntu32'
    ubuntu32.vm.box_url = "ubuntu/trusty32"

    # ubuntu32.vm.network :private_network, ip: "192.168.56.101"
    ubuntu32.vm.provision :shell, path: 'vagrant/linux.sh'

    ubuntu32.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 512]
      v.customize ["modifyvm", :id, "--name", "ubuntu32"]
    end
  end

  config.vm.define "debian32" do |debian32|
    debian32.vm.box = "puppetlabs/debian-7.8-32-puppet"
    debian32.vm.hostname = 'debian32'
    debian32.vm.box_url = "puppetlabs/debian-7.8-32-puppet"

    debian32.vm.network :private_network, ip: "192.168.56.102"

    debian32.vm.provision :shell, path: 'vagrant/linux.sh'

    debian32.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 512]
      v.customize ["modifyvm", :id, "--name", "debian32"]
    end
  end
end

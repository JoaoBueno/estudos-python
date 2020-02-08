sudo -i

apt-get update

apt-get install git -y
apt-get install python3-pip -y
apt-get install pyqt5-dev-tools -y

git clone https://github.com/aq1/Hospital-Helper-2.git /home/vagrant/hh
cd /home/vagrant/hh

pip3 install -r requirements.txt

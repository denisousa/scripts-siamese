sudo apt update -y &&
sudo apt upgrade -y &&
sudo apt-get install trash-cli -y &&
sudo apt-get install maven -y &&
sudo apt-get install openjdk-8-jdk -y &&
sudo apt purge openjdk-11-* -y &&
python3 -m venv env &&
source env/bin/activate &&
pip install -r requirements.txt
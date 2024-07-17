sudo apt update -y &&
sudo apt upgrade -y &&
sudo apt-get install trash-cli -y &&
sudo apt-get install maven -y &&
sudo apt-get install openjdk-8-jdk -y &&
sudo apt purge openjdk-11-* -y &&
udo apt install python3-pip &&
sudo apt install python3-pip && 
python3 -m venv env &&
source env/bin/activate &&
pip3 install -r requirements.txt

# sudo apt install python3-pip
# only python3 main_grid.py works
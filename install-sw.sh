curl -sSL -C- -o install-poetry.py  https://install.python-poetry.org
python install-poetry.py
rm install-poetry.py
echo export PATH=~/.local/bin:$PATH > ~/.bashrc
source ~/.bashrc

apt update > /dev/null 2>&1
apt install byobu -y > /dev/null 2>&1
byobu-enable
byobu

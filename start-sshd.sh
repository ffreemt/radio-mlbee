apt update && apt-get install openssh-server -y
/etc/init.d/ssh restart && mkdir -p ~/.ssh && echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOl+SiDFL1ZUh1QJ0454eYKtamkMCVs2hhuv3cWN1LU7 id_ed25519_colab > ~/.ssh/authorized_keys
echo cd /usr/src/app >> ~/.bashrc
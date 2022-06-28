# poo_pal










# Reload the poo_pal.service from file


sudo cp ./poo_pal.service /lib/systemd/system/poo_pal.service

sudo chmod 644 /lib/systemd/system/poo_pal.service

sudo systemctl daemon-reload

sudo systemctl enable poo_pal.service

sudo systemctl stop poo_pal.service

sudo systemctl start poo_pal.service

sudo systemctl status poo_pal.service

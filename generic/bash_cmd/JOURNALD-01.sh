#! /bin/bash

du -hsc /var/log/journal/
journalctl --disk-usage

grep -E '^SystemMaxUse=' /etc/systemd/journald.conf  
# OR: 
grep -E '^RuntimeMaxUse=' /etc/systemd/journald.conf 

cp spam.service /etc/systemd/system/spam.service
journalctl --rotate --vacuum-size=8M

systemctl start spam

watch -n 1 " \
   journalctl  --flush; \
   journalctl --disk-usage; echo; \
   du -hs /var/log/journal/; echo; \
   ls -hla /var/log/journal/$(cat /etc/machine-id); \
 "

systemctl stop spam 
rm /etc/systemd/system/spam.service
remoot

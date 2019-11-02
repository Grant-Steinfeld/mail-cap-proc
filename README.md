# Mail Capture on Linux via POSTFIX

> Capture emails, parse out the text, add them to a Neo4j Graph Database.
> [Add a Python Flask REST API](https://github.com/Grant-Steinfeld/gandalahar) 

![POSTFIX Neo4j Python CentOS RedHat Logos](https://github.com/Grant-Steinfeld/mail-cap-proc/blob/master/resources/git-hub-header.jpg)

## Does your server have POSTFIX Mail Transport Agent Running?
```sh
sudo systemctl status postfix
```

you should see output similar to this:

```sh
[root@agentidea developer]# systemctl status postfix
● postfix.service - Postfix Mail Transport Agent
   Loaded: loaded (/usr/lib/systemd/system/postfix.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2019-08-10 23:22:53 UTC; 2 months 22 days ago
 Main PID: 988 (master)
   CGroup: /system.slice/postfix.service
           ├─ 988 /usr/libexec/postfix/master -w
           ├─ 994 qmgr -l -t unix -u
           └─8134 pickup -l -t unix -u
```

if you don't have postfix running or installed try,
``` sh
sudo yum install postfix
```
if you need help with installing or configuring POSTFIX?
go [here](https://www.digitalocean.com/community/tutorials/how-to-install-postfix-on-centos-6)

you'll also need to setup mx records on your domain name (DNS) settings to recieve mail to POSTFIX's
Mail Transport Agent



## Login to your unix server ( tested on Red Hat and CentOS )
```sh
sudo su
vim /etc/aliases
```

add line(s) for each email endpoint you want.  For example my server has a hostname of agentidea.com
and is setup to recieve email via POSTFIX

``` text
weather:       "|/home/developer/newdev/breakingnews weather"
```

if you want to reload the aliases for email without a reboot of your server, run as root/sudo
```sh
newaliases
```

so when an email is recived to weather@agentidea.com it will run the script called breakingnews in
the /home/developer/newdev/ directory.  Of course adapt the hostname and path to be specific to your system setup.

breakingnews is a shell script with a python directive
check it out in this repo




### History of POSTFIX
``` text
Originally written in 1997 by Wietse Venema at the IBM Thomas J. Watson Research Center
in New York, and first released in December 1998

 Postfix continues as of 2019 to be actively developed by its creator and other contributors. 
The software is also known by its former names VMailer and IBM Secure Mailer. 
```
[read more on POSTFIX on Wikipedia](https://en.wikipedia.org/wiki/Postfix_(software))

# /etc/cron.d/logcheck: crontab entries for the logcheck package

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

##ENABLED_IN_POSTINST## @reboot         logcheck    if [ -x /usr/sbin/logcheck ]; then nice -n10 /usr/sbin/logcheck -R; fi
##ENABLED_IN_POSTINST## 2 * * * *       logcheck    if [ -x /usr/sbin/logcheck ]; then nice -n10 /usr/sbin/logcheck; fi

# EOF

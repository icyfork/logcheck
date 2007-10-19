#!/usr/bin/make -f

CONFDIR = etc/logcheck
BINDIR = usr/sbin
SHAREDIR = usr/share/logtail/detectrotate

install:
	# Create the directories
	install -m 750 -d $(DESTDIR)/$(CONFDIR)
	install -d $(DESTDIR)/var/lib/logcheck
	install -d $(DESTDIR)/$(BINDIR)
	install -d $(DESTDIR)/var/lock/logcheck
	install -d $(DESTDIR)/$(SHAREDIR)

	install -m 2750 -d $(DESTDIR)/$(CONFDIR)/ignore.d.paranoid
	install -m 2750 -d $(DESTDIR)/$(CONFDIR)/ignore.d.workstation
	install -m 2750 -d $(DESTDIR)/$(CONFDIR)/ignore.d.server
	install -m 2750 -d $(DESTDIR)/$(CONFDIR)/cracking.d
	install -m 2750 -d $(DESTDIR)/$(CONFDIR)/cracking.ignore.d
	install -m 2750 -d $(DESTDIR)/$(CONFDIR)/violations.d
	install -m 2750 -d $(DESTDIR)/$(CONFDIR)/violations.ignore.d

	# Install the scripts
	install -m 755 src/logcheck $(DESTDIR)/$(BINDIR)/
	install -m 755 src/logtail $(DESTDIR)/$(BINDIR)/
	install -m 755 src/logtail2 $(DESTDIR)/$(BINDIR)/
	install -m 755 src/detectrotate/10-savelog.dtr $(DESTDIR)/$(SHAREDIR)/
	install -m 755 src/detectrotate/20-logrotate.dtr $(DESTDIR)/$(SHAREDIR)/
	install -m 755 src/detectrotate/30-logrotate-dateext.dtr $(DESTDIR)/$(SHAREDIR)/

	# Install the config files
	install -m 640 etc/logcheck.logfiles $(DESTDIR)/$(CONFDIR)
	install -m 640 etc/logcheck.conf $(DESTDIR)/$(CONFDIR)

	# Install the rulefiles
	install -m 640 rulefiles/linux/ignore.d.paranoid/* \
		$(DESTDIR)/$(CONFDIR)/ignore.d.paranoid/
	install -m 640 rulefiles/linux/ignore.d.server/* \
		$(DESTDIR)/$(CONFDIR)/ignore.d.server/
	install -m 640 rulefiles/linux/ignore.d.workstation/* \
		$(DESTDIR)/$(CONFDIR)/ignore.d.workstation/
	install -m 640 rulefiles/linux/violations.d/* \
		$(DESTDIR)/$(CONFDIR)/violations.d/
	install -m 640 rulefiles/linux/violations.ignore.d/* \
		$(DESTDIR)/$(CONFDIR)/violations.ignore.d/
	install -m 640 rulefiles/linux/cracking.d/* \
		$(DESTDIR)/$(CONFDIR)/cracking.d/

clean:
	# Remove the scripts
	-rm -f  $(DESTDIR)/$(BINDIR)/logcheck
	-rm -f  $(DESTDIR)/$(BINDIR)/logtail
	# Remove the configfiles
	-rm -f $(DESTDIR)/$(CONFDIR)/logcheck.logfiles
	-rm -f $(DESTDIR)/$(CONFDIR)/logcheck.conf
	# Remove the rulesfiles
	-rm -rf $(DESTDIR)/$(CONFDIR)/ignore.d.paranoid/
	-rm -rf $(DESTDIR)/$(CONFDIR)/ignore.d.server/
	-rm -rf $(DESTDIR)/$(CONFDIR)/ignore.d.workstation/
	-rm -rf $(DESTDIR)/$(CONFDIR)/violations.d/
	-rm -rf $(DESTDIR)/$(CONFDIR)/violations.d/
	-rm -rf $(DESTDIR)/$(CONFDIR)/violations.ignore.d/
	-rm -rf $(DESTDIR)/$(CONFDIR)/cracking.d/
	# Remove the statedir and it's contents
	-rm -rf $(DESTDIR)/var/lib/logcheck 

	# Finally remove the config directory
	-rmdir $(DESTDIR)/$(CONFDIR)

distclean:
	-find . -name "*~" | xargs -r --no-run-if-empty rm -vf

check:
	#cd test; python test.py

system-test:
	cd test; rm -fv state/*; \
		../src/logcheck -c ../etc/logcheck.conf \
				-l ../etc/logcheck.logfiles \
				-r ../rulefiles/linux \
				-S state/ -o

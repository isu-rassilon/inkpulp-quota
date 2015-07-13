#
# InkPulp-Quota Makefile
#

# The VERSION string is used for building a tarball
VERSION=$(shell grep "^VERSION" inkpulp-quota.py | gawk -F= '{print $$2}' | tr -d "'")

# Why compile? Actually, there isn't a good reason
# for this. We're doing it to make it slighly more 
# difficult for users to abuse the server.
inkpulp-quota.pyo: inkpulp-quota.py
	python -O -m py_compile inkpulp-quota.py

all: inkpulp-quota.pyo

install: inkpulp-quota.pyo

tarball: clean all
	mkdir inkpulp-quota-$(VERSION)
	cp inkpulp-quota.* inkpulp-quota-$(VERSION)/
	cp Makefile inkpulp-quota-$(VERSION)/
	tar -czvf inkpulp-quota-$(VERSION).tar.gz inkpulp-quota-$(VERSION)/
	rm -rf inkpulp-quota-$(VERSION)/

clean:
	rm -f inkpulp-quota.pyo inkpulp-quota-*.tar.gz
	rm -rf inkpulp-quota-$(VERSION)/

# EOF

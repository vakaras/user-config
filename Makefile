waf: env configure
	echo '#!/bin/bash' > waf
	echo 'env/bin/python bin/waf "$$@"' >> waf
	chmod 755 waf

env: bin/waf
	python3 bin/waf virtualenv --python=python3

configure: env
	env/bin/python bin/waf configure

bin:
	mkdir bin

WAF_EXISTS := $(wildcard bin/waf)
ifeq ($(strip $(WAF_EXISTS)),)
bin/waf: bin
	wget http://waf.googlecode.com/files/waf-1.7.2 -O bin/waf
else
bin/waf:
	@echo "WAF have been already downloaded."
endif

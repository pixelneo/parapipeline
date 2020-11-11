all: down build
down:
	wget -c ftp://ftp.mokk.bme.hu/Hunglish/src/hunalign/latest/hunalign-1.1.tgz
	tar zxvf hunalign-1.1.tgz
	mv hunalign-1.1 hunalign
build:
	cd hunalign/src/hunalign && make
	echo > hunalign/data/null.dic  # empty dict

clean:
	rm -rf hunalign/
	rm -rf hunalign-1.1.tgz


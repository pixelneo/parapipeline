all: down pars build setupka
down:
	wget -c https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tagger-scripts.tar.gz
	wget -c https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-linux-3.2.3.tar.gz
	wget -c https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/install-tagger.sh

pars:
	#wget -c http://corpus.leeds.ac.uk/serge/mocky/ka.par  # georgian
	wget -c https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/english.par.gz  # english, just to try functionality

build:
	sh install-tagger.sh

setupka:
	cp ka.par lib/
	echo "" > lib/ka-abbreviations
	cat cmd/tree-tagger-czech | sed -e 's/czech/ka/g' > cmd/tree-tagger-ka
	chmod +x cmd/tree-tagger-ka

clean:
	rm -rf tagger-scripts.tar.gz
	rm -rf tree-tagger-linux-3.2.3.tar.gz
	rm -rf install-tagger.sh
	rm -rf english.par.gz
	rm -rf lib
	rm -rf COPYRIGHT
	rm -rf README
	rm -rf bin
	rm -rf FILES
	rm -rf README.script
	rm -rf cmd
	rm -rf doc
	rm -rf lib

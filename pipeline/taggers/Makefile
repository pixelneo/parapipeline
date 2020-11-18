TAGGERS = treetagger udpipe classla

all: reqs btagger
	for t in $(TAGGERS); do cd "$$t" && make; cd ..; done

btagger:
	unzip btagger.zip

reqs: 
	pip3 install -r requirements.txt

clean:
	rm -rf btagger
	for t in $(TAGGERS); do cd "$$t" && make clean; cd ..; done


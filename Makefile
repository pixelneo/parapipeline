all: | setup taggers aligners transl

setup:
	pip install -r pipeline/requirements.txt
taggers:
	cd pipeline/taggers && make
aligners:
	cd pipeline/aligners && make
transl:
	cd pipeline/transliterators && make
clean:
	cd pipeline/taggers && make clean
	cd pipeline/aligners && make clean
	cd pipeline/transliterators && make clean


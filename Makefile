all: taggers aligners transl
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


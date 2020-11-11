all: taggers aligners transl
taggers:
	cd pipeline/taggers && make
aligners:
	cd pipeline/aligners && make
transl:
	cd pipeline/transliterators && make

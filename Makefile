all: pipeline taggers aligners transl
pipeline:
	cd pipeline && pip install -r requirements.txt
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


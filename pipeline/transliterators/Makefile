all: reqs down

down:
	mkdir -p polyglot_data
	polyglot download --dir polyglot_data TASK:transliteration2
reqs:
	pip3 install -r requirements.txt

clean:
	rm -rf polyglot_data

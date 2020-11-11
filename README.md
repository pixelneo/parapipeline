# jena-parapipeline 
**In development, all of this can (and will) change.**
## Installation
Make sure you have following programs installed
- Python 3.8 or later (not tested on Python 3.7 and earlier)
- `wget`
- All prerequisites for Hunalign
- Polyglot for transliteration requires `python-numpy` `libicu-dev`. (`apt-get python-numpy libicu-dev`)

Run `make` to install necessary packages, compile taggers, aligners, download models, ...


## Usage
There are scripts `tag`, `transliterate`, `align` and `run`

### Tagging only
Help of `tag` utility
~~~ 
usage: tag.py [-h] -l LANGUAGE [-e ENCODING] [-d OUTPUT_DIR | --print] (-f INPUT_FILE | -i N [N ...])

Tag files.

optional arguments:
  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        ISO-693-3 code of language.
  -e ENCODING, --encoding ENCODING
                        Encoding of the files
  -d OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory to which to write output files
  --print               Instead of saving to file, print.
  -f INPUT_FILE, --input_file INPUT_FILE
                        Files specifying input file..
  -i N [N ...], --input N [N ...]
                        List of files to be tagged.
~~~

### Transliterate only
Help of `transliterate` utility
~~~
transliterate.py [-h] -l LANGUAGE [-e ENCODING] [-d OUTPUT_DIR | --print] (-f INPUT_FILE | -i N [N ...])

Transliterate files.

optional arguments:
  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        ISO-693-3 code of language.
  -e ENCODING, --encoding ENCODING
                        Encoding of the files
  -d OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory to which to write output files
  --print               Instead of saving to file, print.
  -f INPUT_FILE, --input_file INPUT_FILE
                        Files specifying input file..
  -i N [N ...], --input N [N ...]
                        List of files to be tagged.
~~~

### Align only
Help of `align` utility
~~~
align.py [-h] src tgt

Align files.

positional arguments:
  src         Source file.
  tgt         Target file

optional arguments:
  -h, --help  show this help message and exit
~~~

### Run all
Does not work yet: `run` will take a json file with structure similar to the following example and it will run transliteration if needed, and tagging


### Structure for transliteration and tagging
~~~
{
    "files": [
        {
            "path": "/home/user/file1.txt",
            "lang": "eng",
            "enc": "utf-8"
        },
        {
            "path": "/home/user/file2.txt",
            "lang": "ces",
            "enc": "iso-8859-2"
        },
        ...
    ]
}
~~~


### Structure for alignment
~~~
{
    "texts": [
        { 
            "name": "alice-in-wonderland",
            "files": [
                {
                    "path": "/home/user/alice-file-english.txt",
                    "lang": "eng",
                    "enc": "utf-8"
                },
                {
                    "path": "/home/user/alice-file-cs.txt",
                    "lang": "ces",
                    "enc": "iso-8859-2"
                }
            ]
        },
        {
            "name": "winnie-the-pooh",
            ... 
        },
        ... 
    ]
}
~~~


## Adding new languages
- Edit `.config/config.json`, follow the structure of the other languages in the file to add a new one.
    * For treetagger, `.par` file has to be in `./pipeline/taggers/treetagger/lib/`.
    * For UDPipe, `.udpipe` file has to be in `./pipeline/taggers/udpipe/models/`. Note that this uses UDPipe version 1, UDPipe version 2 models will not work.

## Upgrading
This section is about upgrading models

### UDPipe
In order to update UDPipe models, change `./pipeline/taggers/Makefile`, section `models` to download desired models (and extract them ...). 
Then change `config/config.json` so that each language which uses UDPipe points to correct filename.

### Treetagger
Change `./pipeline/taggers/treetagger/Makefile` to download version of treetagger you wish to use. 
You can also add scripts to download more models and so on.

# Acknoledgements
TODO cite UDPipe, treetagger, hunalign. 

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

All scripts have the same arguments as `run`.

~~~
run.py [-h] [-o OUTPUT_DIR] N [N ...]

Run pipeline.

positional arguments:
  N                     List of files to be processed. Format: NAME_LANG[_ID][.ext], for example Hobbit_eng.txt

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory to which to write the output files.
~~~

### Run all
Does not work yet: `run` will take a json file with structure similar to the following example and it will run transliteration if needed, and tagging


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

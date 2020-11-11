# parapipeline 
**In development, all of this can (and will) change.**

Parapipeline is a pipeline for POS tagging of texts in multiple languages, sentence alignment, and transliteration.

## Installation
Make sure you have following programs installed
- Python 3.8 or later (not tested on Python 3.7 and earlier)
- `wget`
- All prerequisites for Hunalign
- Polyglot for transliteration requires `python-numpy` `libicu-dev`. (`apt-get python-numpy libicu-dev`)
- `git-lfs`

Run `git lfs install`.
Run `make` to install necessary packages, compile taggers, aligners, download models, ...

## Usage
There are scripts `tag`, `transliterate`, `align` and `run`

All scripts have the same arguments as `run`.

### Input
All scripts expect line delimited sentences in nutf-8 encoded files.

The name of these files is `NAME_LANG_[_ID][.ext]`, where `NAME` is arbitrary text not containing `_`, `LANG` is iso-639-3 language code, 
optional `ID` distinguished between more variants of the same text (e.g. different translations), `.ext` is also optional.

### Output
`run` script outputs tagged texts in XML files. 

And when possible also sentence alignment file in XML. 
This file contains the alignment.

 **TODO**: finish

### Help 
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


## Languages

**TODO**

### Adding new languages
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
- UDPipe: Straka Milan, Hajič Jan, Straková Jana. UDPipe: Trainable Pipeline for Processing CoNLL-U Files Performing Tokenization, Morphological Analysis, POS Tagging and Parsing. In Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016), Portorož, Slovenia, May 2016
- Treetagger: Helmut Schmid (1994): Probabilistic Part-of-Speech Tagging Using Decision Trees. Proceedings of International Conference on New Methods in Language Processing, Manchester, UK
- Hunalign: D. Varga, L. Németh, P. Halácsy, A. Kornai, V. Trón, V. Nagy (2005). Parallel corpora for medium density languages In Proceedings of the RANLP 2005, pages 590-596.
- BTagger: https://github.com/agesmundo/BTagger
- Georgian Treetagger model comes from here: http://corpus.leeds.ac.uk/serge/mocky/ka.par

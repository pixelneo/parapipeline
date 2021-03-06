# parapipeline 
**In development, all of this can change.**

Parapipeline is a pipeline for POS tagging of texts in multiple languages, sentence alignment, word alignment, and transliteration.

## Installation
Make sure you have following programs installed
- Python 3.8 or later (not tested on Python 3.7 and earlier)
- `wget`
- All prerequisites for Hunalign
- Polyglot for transliteration requires `python-numpy` `libicu-dev`. (`apt-get python-numpy libicu-dev`)
- `git-lfs`

Run `git lfs install`.
Run `make` to install necessary packages, compile taggers, aligners, download models, ...

The installation process is not thoroughly tested on various systems (it should work on Ubuntu 18.04), if you encounter an error it's likely caused by a missing prerequisite.

## Usage
There are scripts `tag`, `transliterate`, `align`, `wordalign` and `run`

All scripts have the same arguments as `run`.

### Input
All scripts expect line delimited sentences in utf-8 encoded files.

The name of these files is `NAME_LANG[_ID][.ext]`, where `NAME` is arbitrary text not containing `_`, `LANG` is iso-639-3 language code, 
optional `ID` distinguished between more variants of the same text (e.g. different translations), `.ext` is also optional.

Inputs have to be case insensitive (if you have file NAME and Name, it will cause errors).

See files in `examples` folder for some example input files.

### Output
`run` script outputs tagged texts in XML files. 

And when possible also sentence and word alignment files in XML. 

See `examples/outputs` for example output of this pipeline.
#### Sentence alignment

Aligned sentences are represented by `link` tag.

- Attribute `type` denotes the number of sentences from source and target text.
- Attribute `xtargets` is the alignment itself: `6 7;5` meaning sentences `6`,`7` from source are aligned with sentence `5` from target.

#### Word alignment
Each `link` represents an "aligned block" - aligned sentences.

Attribute `xtargets` contains is a space-separated list of alignments... `1:2;3:4` means that word `2` from sentence `1` in source text is aligned with word `4` in sentence `3` in the target text.

### Help 
~~~
usage: run.py [-h] [-o OUTPUT_DIR] N [N ...]

Run pipeline.

positional arguments:
  N                     List of files to be processed. Format: NAME_LANG[_ID][.ext], for example Hobbit_eng.txt

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory to which to write the output files.
~~~


## Languages

| Done| Language | Done| Language | Done| Language |
|:------------------|:--------------| :------------------|:---------------| :------------------|:-----------------|
|:white_check_mark: | Afrikaans     | :white_check_mark: | French         |:white_check_mark: | Norwegian | 
|:white_check_mark: | Albanian      | :white_check_mark: | Georgian       |:white_check_mark: | Polish | 
|:white_check_mark: | Armenian      | :white_check_mark: | German         |:white_check_mark: | Portuguese | 
|:white_check_mark: | Belarusian    | :white_check_mark: | Hebrew         |:white_check_mark: | Romanian | 
|:x:                | Bosnian       | :white_check_mark: | Hungarian      |:white_check_mark: | Russian | 
|:white_check_mark: | Bulgarian     | :white_check_mark: | Italian        |:white_check_mark: | Serbian | 
|:white_check_mark: | Catalan       | :white_check_mark: | Japanese       |:white_check_mark: | Slovak | 
|:white_check_mark: | Chinese       | :x:                | Kashubian      |:white_check_mark: | Slovenian | 
|:white_check_mark: | Croatian      | :white_check_mark: | Korean         |:white_check_mark: | Spanish | 
|:white_check_mark: | Czech         | :white_check_mark: | Latvian        |:white_check_mark: | Swedish | 
|:white_check_mark: | Danish        | :white_check_mark: | Lithuanian     |:white_check_mark: | Turkish | 
|:white_check_mark: | Dutch         | :x:                | Lower Sorbian  |:white_check_mark: | Ukrainian | 
|:white_check_mark: | English       | :white_check_mark: | Macedonian     |:white_check_mark: | Upper Sorbian | 
|:white_check_mark: | Estonian      | :white_check_mark: | Modern Greek   |:x:                | Yiddish |
|:white_check_mark: | Finnish       | :x:                | Molise Slavic  |                   |         |


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
- Eflomal: https://github.com/robertostling/eflomal

# License
CC BY-NC-SA

This work mainly depends on trained UDPipe models which are licesed under CC BY-NC-SA.

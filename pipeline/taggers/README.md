# plain text tagger

## Requirements
1. Install Python 3 (preferably 3.8+)
2. run `pip install -r requirements.txt`

## Running

Run `python3 udpipe.py --enc=iso-8859-2 short-hobbit-eng.txt` to tag the file short-hobbit-eng.txt

Result will be saved to `filename`.conllu

Generally, `python3 udpipe.py file1.txt file2.txt ....` works. Default encoding is `utf-8`.


## What is not done

- For now, only English model is downloaded (dir `models/`) and only English has assigned a model in `config/lang2model.json`. 
- **How to extract language code?** This is important. How will the input files have language code encoded in them? eng.txt, eng-1984.txt, 1984-eng.txt ???



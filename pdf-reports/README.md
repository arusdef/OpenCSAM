# PDF Documents - Set of Scripts to Download and Process

***

## Prepare the Environment

Run the command `pip3 install -r requirements.txt` which will install all required Python packages for you.

***

## Script download.py

The script downloads pdf documents from a remote resource and saves them locally.

Run the script `./download.py` from the command line. It will create a `documents` folder and pull all available documents into it.

***

## Script tags.py

The script obtains topics and keywords from the ENISA web page.

Run the script `./tags.py` from the command line. It will create a file called `tags.csv`.

***

## Script plaintext.py

Parses PDF documents and extract data and metadata in a plain text format. The parsing is done using the Tika parser [tika-python](https://github.com/chrismattmann/tika-python).

Although no Word documents were ingested during the prototype phase, parsing these follows a similar process as outlined [here](https://tika.apache.org/0.5/formats.html). 

Run the script `./plaintext.py` from the command line. It will create a `plaintext` folder and save the parsed text from the PDF documents into it.

***

## Script index.py

Run the script `./index.py` to upload the documents to Elasticsearch. The script first loads the parsed plaintext documents including the metadata, adds the topics and keywords from the `tags.csv` file and extracts further document structure using the python methods from the `enisa-nlp` package.

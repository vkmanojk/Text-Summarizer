# Text Summarizer

Text Summarizer is a flask based web application. It uses NLTK, Gensim, Sumy and Spacy to summarize. The application is built using Flask, HTML5, CSS3 and Javascript. 

You can watch the live demo [here](https://youtu.be/hwuZ0nQHTfo)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
The prerequisites are already mentioned in [requirements.txt](requirements.txt)
```
beautifulsoup4
bs4
Flask
nltk
spacy
sumy
thinc
urllib3
gensim
gensim-sum-ext
https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.0.0/en_core_web_md-2.0.0.tar.gz
gunicorn
```

### Installing

Run the command below to install the the prerequirements

```
pip install -r requirements.txt
```

In case of errors, check that the python version you're using is 64-bit. Delete the github link in the [requirements.txt](requirements.txt). Install it again using pip. Now enter the command below 

```
python -m spacy download en
```
Also make sure to run the terminal / command prompt as root.
## Running the application

Simply type 

```
python app.py
```
in the terminal


## Built With

* Flask
* HTML
* CSS
* Spacy
* NLTK
* Gensim

 

## Author

**Manojkumar V K**  - [Web](https://vkmanojk.github.io) 

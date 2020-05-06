from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request, session
from flask import *
from spacy_summarization import text_summarizer
from gensim.summarization import summarize
from nltk_summarization import nltk_summarizer
import time
import spacy
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from datetime import date

nlp = spacy.load('en')
app = Flask(__name__)
app.secret_key = 'Random String '
 
def sumy_summary(docx):
	session['value']+=1
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result

def readingTime(mytext):
	session['value']+=1
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime


def get_text(url):
	try:
		session['value']+=1
		req = Request(url,headers={'User-Agent' : "Magic Browser"})
		page = urlopen(req)
		soup = BeautifulSoup(page,'html.parser')
		soup.prettify()
		fetched_text = ''.join(map(lambda p:p.text,soup.find_all('p',href=False)))  
		if fetched_text == '':
			return 0
		return fetched_text
	except:
		return 0

@app.route('/')
def index():
	session['value'] = 0
	s = session['value']
	if not request.cookies.get('Date'):
		resp = make_response(render_template('index.html',count = s))
		resp.set_cookie('Date',str(date.today()))
		#print('Setting cookie')
	else:
		#print('Accessing cookie')
		resp = make_response(render_template('index1.html',count = s, date = request.cookies.get('Date')))
		resp.set_cookie('Date',str(date.today()))
	return resp


@app.route('/analyze',methods=['GET','POST'])
def analyze():
	start = time.time()
	session['value']+=1
	if request.method == 'POST':
		s = session['value']
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',count = s,ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)
	

@app.route('/analyze_url',methods=['GET','POST'])
def analyze_url():
	start = time.time()
	session['value']+=1
	if request.method == 'POST':
		s = session['value']
		raw_url = request.form['raw_url']
		rawtext = get_text(raw_url)
		if rawtext == 0 or rawtext is None:
			flash('The website does not contain texts or it does not allow texts to be extracted.', category='alert')
			rawtext = 'Error'
			return render_template('index.html',count = session['value'],ctext=rawtext,final_summary=' ',final_time=0,final_reading_time=0,summary_reading_time=0)
		final_reading_time = readingTime(rawtext)
		final_summary = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',count = session['value'],ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)



@app.route('/compare_summary')
def compare_summary():
	return render_template('compare_summary.html',count = session['value'])

@app.route('/comparer',methods=['GET','POST'])
def comparer():
	start = time.time()
	session['value']+=1
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary_spacy = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary_spacy)
		# Gensim Summarizer
		final_summary_gensim = summarize(rawtext)
		summary_reading_time_gensim = readingTime(final_summary_gensim)
		# NLTK
		final_summary_nltk = nltk_summarizer(rawtext)
		summary_reading_time_nltk = readingTime(final_summary_nltk)
		# Sumy
		final_summary_sumy = sumy_summary(rawtext)
		summary_reading_time_sumy = readingTime(final_summary_sumy) 

		end = time.time()
		final_time = end-start
	return render_template('compare_summary.html',count = session['value'],ctext=rawtext,final_summary_spacy=final_summary_spacy,final_summary_gensim=final_summary_gensim,final_summary_nltk=final_summary_nltk,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,summary_reading_time_gensim=summary_reading_time_gensim,final_summary_sumy=final_summary_sumy,summary_reading_time_sumy=summary_reading_time_sumy,summary_reading_time_nltk=summary_reading_time_nltk)
	



@app.route('/about')
def about():
	session['value'] = 0
	return render_template('index.html',count = session['value'])

if __name__ == '__main__':
	app.run(debug=True)

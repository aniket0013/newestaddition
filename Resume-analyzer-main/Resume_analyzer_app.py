import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
# from PIL import Image 
from PyPDF2 import PdfFileReader
import pdfplumber
import streamlit as st
import streamlit.components.v1 as components
import re
import spacy
import os
import fitz
from werkzeug.utils import secure_filename
import pickle
import nltk 
import numpy as np                                 
import pandas as pd
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer     
import pdb
import logging
from PIL import Image
import urllib
nltk.download('stopwords')

#    _____ __                            ___ __       _       __     __                         
#   / ___// /_________  ____ _____ ___  / (_) /_     | |     / /__  / /_  ____ _____  ____      
#   \__ \/ __/ ___/ _ \/ __ `/ __ `__ \/ / / __/     | | /| / / _ \/ __ \/ __ `/ __ \/ __ \     
#  ___/ / /_/ /  /  __/ /_/ / / / / / / / / /_       | |/ |/ /  __/ /_/ / /_/ / /_/ / /_/ /     
# /____/\__/_/   \___/\__,_/_/ /_/ /_/_/_/\__/       |__/|__/\___/_.___/\__,_/ .___/ .___/      
#                                                                           /_/   /_/       




# urllib.request.urlretrieve("https://i.ibb.co/jV1BRxN/Pics-Art-Crop.png","ra.png")				#TO CHANGE THE WEBAPP FABICON
# img = Image.open('ra.png')  #IMP (FOR PAGE ICON CHANGE) 
st.beta_set_page_config(page_title='Resume analyzer',page_icon="👨‍💻")							#CONFIG WEB PAGE ICON AND TITLE


#PDF READER FUNC
def read_pdf_with_pdfplumber(file):
	with pdfplumber.open(file) as pdf:
	    page = pdf.pages[0]
	    return page.extract_text()


#RESUME SUMMERIZATION / CUSTOM NER FUNC
def custom_NER(text): 
    model = spacy.load('resume_sum1')
    txt=text
    doc = model(txt)
    abc = doc.ents
    return abc
    

#DATA PRE-PROCESSING FUNC
def gen_test_data_for_pred(text):
    test = text
    snow = nltk.stem.SnowballStemmer('english')
    corpus_test = []
    review = re.sub('[^a-zA-Z]', ' ', test)
    review = review.lower()
    review = review.split()
        
    review = [snow.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    corpus_test.append(review)

    final_tf_test = corpus_test
    tf_idf = pickle.load(open('data/tfidf_vectorizer.pkl','rb'))
    test_data = tf_idf.transform(final_tf_test)
    return test_data

# SCORE GENERATION/ML MODEL FUNC    
def prediction(text):
    clf_model = pickle.load(open('data/rf_score_model.pkl','rb'))
    result = clf_model.predict(gen_test_data_for_pred(text))
    return result


#ENGINE FUNC
def main():

	page_bg_img = '''
	<style>
	body {
	background: linear-gradient(0deg, rgba(34,193,195,1) 0%, rgba(253,45,249,1) 100%);
	background-repeat:no-repeat;
	background-size: 1900px 800px;
	
	}
	</style>
	'''

	st.markdown(page_bg_img, unsafe_allow_html=True)          						#THIS IS TO CHANGE THE WEB PAGE COLOR(CURRENTLY BLUE-MAGENTA GRADIENT)

	st.markdown(																	                        #THIS IS TO CHANGE THE NAVBAR COLOR(CURRENTLY WHITE)
		"""																	
	<style>
	.sidebar .sidebar-content {
	    background: #ffffff;
	    color: white;
	}
	</style>
	""",
	    unsafe_allow_html=True,
	)
	nav_bar_img_html = """<img src='https://i.ibb.co/jV1BRxN/Pics-Art-Crop.png' width="300" height="100">""" #THIS IS THE RESUME ANALYZER IMG AT NAV
	
	st.sidebar.markdown(nav_bar_img_html, unsafe_allow_html=True)

	st.sidebar.markdown("""<br>""",unsafe_allow_html=True)
	
	st.sidebar.markdown("""<h2 style="color:black;">Navigation Bar:</h2>""",unsafe_allow_html=True)			#NAVBAR HEADING
	
	st.markdown("""<br><br><br>""",unsafe_allow_html=True)
	
	menu = ["About🧾","Resume Score Generator📊","Resumme Summarizer📋"]
	
	choice = st.sidebar.radio("",menu)

	if choice == "About🧾":

		nav_bar_img_html = """<img src='https://i.ibb.co/jV1BRxN/Pics-Art-Crop.png' width="690" height="160">""" 
		
		st.markdown(nav_bar_img_html, unsafe_allow_html=True)
		
		about_section = """
			This project is called **Resume Analyzer**. Currently, it has only two features,
				
			** 1. Resume Score Generator **
			<br>
			** 2. Resume Summarizer **

			### 1. Resume Score Generator: 
			It's a Machine Learning based model that is getting executed whenever you are clicking the Process button. It gives you a score, 
			which is generated by the model. This score might be helpful for recruiters or an HR person to shortlist a candidate for an interview. 
			Except that a candidate also can use it to check his/her score and according to that they can make changes to their resume. (The ML 
			model which is been developed is not so much accurate, because it is trained on randomly generated score data.)


			### 2. Resume Summarizer:  
			It's a Custom NER(Named Entity Recognition) model which helps to summarize the resume. This is also important, because when the number 
			of applications increases, it gets difficult for higher-ups (recruiters) to look through each and every resume and analyze it. So, this 
			summarizer helps to see the skills and projects of that candidate at a glance.


			Target people of this project is recruiter or HR person of any company who will be shortlisting the candidate based on their applications. 
			But, candidates also can use it to, get a score for their resume, and improve further.

			Visit the GitHub [reposetory](https://github.com/soumya997/Resume-analyzer) to know more. 
			If you like the project don't forget to star the repository 😇.

		"""
		st.markdown(about_section,unsafe_allow_html=True)					 #ABOUT PAGE		


	elif choice == "Resume Score Generator📊":

		web_page_img_html = """<img src='https://i.ibb.co/jV1BRxN/Pics-Art-Crop.png' width="690" height="160">"""        #WEB PAGE RESUME ANALYZER IMG
		st.markdown(web_page_img_html, unsafe_allow_html=True)

		html_title = """<h2 style="color:black;text-align:center;">Upload a resume to get resume score</h2>"""
		st.markdown(html_title,unsafe_allow_html=True)

		docx_file = st.file_uploader("",type=['pdf'])
		button_clicked = st.button("Process")
		if button_clicked:
			if docx_file is not None:
				file_details = {"Filename":docx_file.name,"FileType":docx_file.type,"FileSize":docx_file.size}
				if docx_file.type == "application/pdf":
					txt = read_pdf_with_pdfplumber(docx_file)
					result = prediction(txt)
					int_result = int(result)+1
					st.title("your Score is {}".format(int_result)) 
					if int_result>=8:
						st.markdown("""## Wow! He has good skills 💪""")
						st.balloons()
					else:
						st.markdown("""## Poor One 🥴""")

	else:
		web_page_img_html = """<img src='https://i.ibb.co/jV1BRxN/Pics-Art-Crop.png' width="690" height="160">"""
		st.markdown(web_page_img_html, unsafe_allow_html=True)

		html_title = """<h2 style="color:black;text-align:center;">Summarize the Resume</h2>"""
		st.markdown(html_title,unsafe_allow_html=True)

		docx_file = st.file_uploader("",type=['pdf'])
		if st.button("Process"):
			if docx_file is not None:
				file_details = {"Filename":docx_file.name,"FileType":docx_file.type,"FileSize":docx_file.size}
				if docx_file.type == "application/pdf":
					txt = read_pdf_with_pdfplumber(docx_file)
					doc = custom_NER(txt)
					st.title("summary of the Resume: ")
					for ent in doc:
						st.subheader(f'{ent.label_.upper():{30}}- {ent.text}')
					st.balloons()



if __name__ == '__main__':
	main()

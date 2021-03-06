import numpy as np
import pandas as pd
import requests, re
import datetime
import json
import time
from selenium import webdriver

from bs4 import BeautifulSoup as BS
from urllib.request import urljoin

from flashtext import KeywordProcessor
keyword_processor = KeywordProcessor()

#from pytablewriter import MarkdownTableWriter

from krs import niramai,locus, oneorigin, alphasense, sayint, casetext
from manoj import zebra, episource, vicarious, uipath
from vinod import greenhouse_platform, workday_cognex, kla_tencor, hp
from jagadeesh import Haptik_AI, Gramener, Boost_AI, Lumiq_FreshTeam, neurala, honeywell, IHSMarkit, x_ai
from sitaram import abto,kritikal,atlas_elektronik,tobii,philips,tno


executable_path=r'chromedriver_win32\chromedriver.exe'

companies_md_url='https://github.com/colearninglounge/co-learning-lounge/blob/master/Technology/Artificial%20Intelligence/companies.md'

fields_needed=['Company Name',
                 'Job Title',
                 'Job Description',
                 'Job Location',
                 'Job Type',
                 'Years of Experience',
                 'Job Department',
                 'Job Specific URL',
                 'Career Page URL',
                 'Market/Sector']

key_words_list=['deep learning', 'dl', 'machine learning', 'ml', 'nlp', 'natural language processing', 'computer vision',
           'cv', 'data scientist', 'ds', 'business analyst', 'data engineer', 'research engineer', 'data visualization',
           'data analyst', 'database administrator', 'database admin','data architect', 'statistician', 'data and analytics',
           'chatbot', 'conversational AI', 'artificial intelligence', 'AI', 'quantitative analyst', 'data warehouse',
           'business intelligence analyst','python', 'data operations', 'financial analyst']

keyword_processor.add_keywords_from_list(key_words_list)

#companies_md_df=pd.read_excel(r'outputs/companies_md_df as on May 28, 2020 at 10 PM.xlsx',sheet_name='company career page urls')

def companiesmd_to_dict(companies_md_url):

    html = requests.get(companies_md_url).text

    soup = BS(html, 'lxml')

    allh2s = soup.find(id="readme").find_all('h2')

    alluls = soup.find(id="readme").find_all('ul')

    dictionary={}

    for allh2, allul in zip(allh2s, alluls):

        sector = allh2.get_text()

        allls = allul.find_all('li')

        for alll in allls:

            career_page_url = alll.a.get('href')

            company_name = alll.a.get_text()

            dictionary[f'{company_name}']={'sector':sector,'career_page_url':career_page_url}

    return dictionary

def in_key_words_list(item):

    found = keyword_processor.extract_keywords(item)

    if found:
        return found, 'Yes'
    else:
        return "No"

# def to_markdown(df,date):
#     writer = MarkdownTableWriter()
#     writer.table_name = "Jobs Info as on "+ date
#     writer.headers = ['Index']+df.columns.to_list()
#     writer.value_matrix=[]
#     for row in df.itertuples():
#         writer.value_matrix.append([*row])
#
#     writer.write_table()
#     writer.dump(r'outputs/'+'jobs as on ' + date + '.md')

if __name__=='__main__':

    frames = []
    date=datetime.datetime.today().strftime('%B %d, %Y at %I %p')

    companies_details = companiesmd_to_dict(companies_md_url)
    print(companies_details)

    for index,func in enumerate([locus('locus.sh',companies_details),
                                 niramai('niramai',companies_details),
                                 oneorigin('oneorigin',companies_details),
                                 alphasense('alphaSense',companies_details),
                                 zebra('Zebra medical vision',companies_details),
                                 episource('Episource LLC',companies_details),
                                 vicarious('vicarious',companies_details),
                                 uipath('UI path',companies_details),
                                 greenhouse_platform('immersive labs', companies_details),
                                 #workday_cognex('COGNEX', companies_details),
                                 kla_tencor('Kla Tencor', companies_details),
                                 hp('hp labs',companies_details),
                                 Haptik_AI('haptik.ai',companies_details),
                                 Gramener('Gramener',companies_details),
                                 Boost_AI('boost.ai',companies_details),
                                 Lumiq_FreshTeam('lumiq.ai',companies_details),
                                 sayint('sayint.ai',companies_details),
                                 casetext('casetext',companies_details),
                                 greenhouse_platform('tempus', companies_details),
                                 greenhouse_platform('soundhound', companies_details),
                                 greenhouse_platform('rasa', companies_details),
                                 greenhouse_platform('clarifai', companies_details),
                                 greenhouse_platform('freenome', companies_details),
                                 greenhouse_platform('nauto', companies_details),
                                 neurala('neurala',companies_details),
                                 #honeywell('honeywell',companies_details),
                                 IHSMarkit('IHS Markit',companies_details),
                                 x_ai('x.ai',companies_details),
                                 abto('abto software',companies_details),
                                 kritikal('KritiKal Solutions',companies_details),
                                 atlas_elektronik('atlas elektronik',companies_details),
                                 tobii('tobii',companies_details),
                                 philips('philips',companies_details),
                                 tno('TNO',companies_details)],1):

        print(index,func.shape)
        frames.append(func)

    jobs_df = pd.concat(frames, axis=0, ignore_index=True)

    #jobs_df = jobs_df.merge(companies_md_df[['Company Name','Market/Sector']],on='Company Name')

    jobs_df['in_key_words_list'] = jobs_df['Job Title'].apply(lambda s: in_key_words_list(str(s).strip()))

    jobs_df.to_excel(r'outputs//'+'all jobs.xlsx', sheet_name=f'{date}',index=False)

    jobs_df = jobs_df[jobs_df['in_key_words_list' ]!='No'].drop(columns=['in_key_words_list']).reset_index()

    jobs_df['Company Name'] = "[" + jobs_df['Company Name'].astype(str) + "]" + "(" + jobs_df['Career Page URL'].astype(str) + ")"

    jobs_df['Job Title' ] = "[" +jobs_df['Job Title'].astype(str ) +"]" +"(" +jobs_df['Job Specific URL'].astype(str ) +")"

    jobs_df = jobs_df[['Market/Sector','Company Name','Job Title','Job Location']].sort_values(by=['Market/Sector','Company Name'], ascending=True).reset_index(drop=True)

    jobs_df.to_excel(r'outputs//'+'filtered jobs in required format.xlsx', sheet_name=f'{date}',index=False)

    # to_markdown_format(jobs_df,date)

    print('end')

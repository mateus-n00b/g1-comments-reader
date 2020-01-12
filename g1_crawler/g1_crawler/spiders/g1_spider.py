#coding: utf-8
import scrapy
import re
from urllib.parse import quote
from ast import literal_eval
import freq_words
from utils import *

class g1Spyder(scrapy.Spider):
    name = "crawler"

    def start_requests(self):
        # Put your URLs here 
        urls = ['https://g1.globo.com/df/distrito-federal/noticia/2020/01/11/zoologico-de-brasilia-recebe-maior-especie-de-cobra-do-mundo.ghtml']
        # URL for get comments (Do not change)
        self.comments_url = "https://comentarios.globo.com/comentarios/{0}/{1}/{2}/shorturl/{3}/"        
        # Iterates for each URL
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        try:
            # Find "#SETTINGS" script that contains the comments ID
            content = response.css('#SETTINGS').get()
            # Filter the response
            # The replace('/','@@') is needed for url encode
            external_id = re.search('COMENTARIOS_IDEXTERNO: "(.*)"', content).group(1).replace("/","@@")
            external_id = quote(external_id)
            comments_uri = re.search('COMENTARIOS_URI: \"(.*)\"(,[A-Z])', content).group(1).replace("/","@@")
            comments_uri = quote(comments_uri)
            title = response.css('head > meta:nth-child(68)').get()
            title =  re.search('content=\"(.*)"', title).group(1)
            title = quote(title)
            cannonical_url = quote(response.url.replace("/","@@"))
        except Exception as err:
            print(err)
            exit(1)
        # /numero endpoint returns the number of comments in the page. 
        self.comments_url = self.comments_url.format(comments_uri, external_id, cannonical_url, title)+"numero"        
        yield response.follow(self.comments_url, self.get_comments)        

    def get_comments(self,response):
        ori_body = response.body.decode()
        jsonObj = body_to_json(ori_body)

        number_of_comments = jsonObj['numeroDeComentarios']
        number_of_pages = jsonObj['limitePaginas']

        if number_of_pages == 0:
            print("Nothing to do here! Exiting...")
            exit(0)
        self.log("Found {} pages".format(number_of_pages))
        # Request url comments for each page        
        for i in range(1,number_of_pages+1): 
            self.log("Crawling...")
            # Follow url comments link
            yield response.follow(self.comments_url.replace('numero',"{}.json".format(i)), 
            self.do_comments_analysis)

    def do_comments_analysis(self,response):
        received_file = response.url.split('/')[-1]
        self.log("Received file {}".format(received_file))
        ori_body = response.body.decode()
        jsonObj = body_to_json(ori_body)
        
        # String for save 
        word_token = ""
        for i in range(len(jsonObj['itens'])):
            replies = jsonObj['itens'][i]['replies']
            userObj = jsonObj['itens'][i]['Usuario']
            text = jsonObj['itens'][i]['texto']        
            for rep in replies:
                text = rep['texto']
                if text:
                    word_token += text.lower()+"\n"    
            word_token += text.lower()
        save_in(received_file, word_token)
        # Show words frequency 
        freq_words.freq_words(word_token.split())
    
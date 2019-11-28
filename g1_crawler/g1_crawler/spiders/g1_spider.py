#coding: utf-8
import scrapy
import re
from urllib.parse import quote
from ast import literal_eval
class g1Spyder(scrapy.Spider):
    name = "crawler"

    def start_requests(self):
        # Define your URLs here 
        urls = ['https://g1.globo.com/rs/rio-grande-do-sul/noticia/2019/11/27/relator-do-processo-sobre-sitio-de-atibaia-no-trf-4-vota-por-condenacao-de-lula-por-corrupcao-e-lavagem-de-dinheiro.ghtml']
        self.comments_url = "https://comentarios.globo.com/comentarios/{0}/{1}/{2}/shorturl/{3}/"
        #SETTINGS
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        try:
            content = response.css('#SETTINGS').get()
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

        self.comments_url = self.comments_url.format(comments_uri, external_id, cannonical_url, title)+"numero"
        
        yield response.follow(self.comments_url, self.get_comments)        

    def get_comments(self,response):
        ori_body = response.body.decode()
        jsonObj = self.body_to_json(ori_body)

        number_of_comments = jsonObj['numeroDeComentarios']
        number_of_pages = jsonObj['limitePaginas']

        if number_of_pages == 0:
            print("Nothing to do here! Exiting...")
            exit(0)

        number_of_pages = 2
        # Request url comments for each page
        for i in range(1,number_of_pages): 
            self.log("Crawling...")
            yield response.follow(self.comments_url.replace('numero',"{}.json".format(i)), self.do_comments_analysis)

    def do_comments_analysis(self,response):
        received_file = response.url.split('/')[-1]
        self.log("Received file {}".format(received_file))
        ori_body = response.body.decode()
        jsonObj = self.body_to_json(ori_body)

        # print(jsonObj)

    def body_to_json(self,body):
        body = body.split('(')[1].split(')')[0]
        body = literal_eval(body.replace('false', 'False')
        .replace('true','True')
        .replace('null',"False")
        .replace(" ","").rstrip())

        return body

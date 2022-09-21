from csv import DictWriter
import scrapy
import os
import csv
import json

class SpiderAjSpider(scrapy.Spider):
    name = 'spider_criticas_jn'
    
    ## Página com as críticas de séries e filmes
    ## https://jovemnerd.com.br/bunker/categoria/criticas/
    
    ## API utilizada pelo site para consultar as notícias, devido ao uso de JavaScript dentro do site para carregar mais notícias
    ## https://api.jovemnerd.com.br/wp-json/jovemnerd/v1/nerdbunker?per_page=28&page=2&category=Críticas
    base_url = 'https://api.jovemnerd.com.br/wp-json/jovemnerd/v1/nerdbunker?per_page=28&page=%d&category=Críticas'
    page = 1
    start_urls = [base_url % page]

    if os.path.exists("jovemnerd-criticas.csv"):
        os.remove
     
    # função que interpreta a página que exibe as criticas de filmes e séries no site JovemNerd
    def parse(self, response):
        json_data = json.loads(response.text)
        
        for link in json_data:
            yield scrapy.Request(link['url'], callback=self.parse_movie)
        if json_data:
            # if que é executado enquanto a página tem noticias para serem exibidas. Quando tudo é carregado, o json_data vem vazio e não entra mais na condição
            next_page = self.base_url % (self.page + 1)
            yield scrapy.Request(next_page, callback=self.parse)
    
    # função que consulta as criticas dos filmes e séries
    def parse_movie(self, response):
        content = ""
        content = content + ' '.join(line.strip() for line in response.css('div.content-left p ::text').extract()).strip()
        
        post = {
            "titulo": response.css("main.site-main").css("h1::text").get().split(' | ')[0],
            "publicado_por": response.css("main.site-main").css("div.author").css("a::text").get()[1:],
            "critica": content
        }
        
        with open("jovemnerd-criticas.csv", 'a', newline='', encoding='utf8') as output_file:
            dict_writer = csv.DictWriter(output_file, post.keys())
            dict_writer.writerows([post])
from csv import DictWriter
import scrapy
import os
import csv


class SpiderAjSpider(scrapy.Spider):
    name = 'spider_criticas_jn'
    
    ## https://jovemnerd.com.br/bunker/categoria/criticas/
    ## https://api.jovemnerd.com.br/wp-json/jovemnerd/v1/nerdbunker?per_page=28&page=2&category=Críticas
    start_urls = ['https://jovemnerd.com.br/bunker/categoria/criticas/']

    if os.path.exists("jovemnerd-criticas.csv"):
        os.remove
     
    # função que interpreta a página que exibe 250 filmes com as maiores notas
    def parse(self, response):
        for link in response.css("h2.title").css("a::attr(href)").getall():
            print(link)
            yield scrapy.Request(link, callback=self.parse_movie)
    
    # função que consulta as informações dos filmes
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
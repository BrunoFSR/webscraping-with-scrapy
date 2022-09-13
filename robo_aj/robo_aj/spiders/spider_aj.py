from csv import DictWriter
import scrapy
import os
import csv


class SpiderAjSpider(scrapy.Spider):
    name = 'spider_aj'
    
    start_urls = ['https://jovemnerd.com.br/bunker/categoria/criticas/']

    if os.path.exists("imdb_top_250_movies.csv"):
        os.remove
     
    # função que interpreta a página que exibe 250 filmes com as maiores notas
    def parse(self, response):
        for link in response.css("h2.title").css("a::attr(href)").getall():
            yield scrapy.Request(link, callback=self.parse_movie)
    
    # função que consulta as informações dos filmes
    def parse_movie(self, response):
        content = ""
        content = content + ' '.join(line.strip() for line in response.css('div.content-left p ::text').extract()).strip()
        
        # titulo
        # print(response.css("main.site-main").css("h1::text").get().split(' | ')[0])
        
        # publicado_por
        # print(response.css("main.site-main").css("div.author").css("a::text").get()[1:])
        
        # content
        # print(content)
        
        post = {
            "titulo": response.css("main.site-main").css("h1::text").get().split(' | ')[0],
            "publicado_por": response.css("main.site-main").css("div.author").css("a::text").get()[1:],
            "critica": content
        }
        
        with open("imdb_top_250_movies.csv", 'a', newline='', encoding='utf8') as output_file:
            dict_writer = csv.DictWriter(output_file, post.keys())
            dict_writer.writerows([post])
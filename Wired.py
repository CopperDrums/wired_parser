import urllib
import urllib.request
from bs4 import BeautifulSoup
import datetime
import html
import sys
import datetime
import lxml

main_url="https://wired.com"
categories=["business", "culture", "design", "gear", "science", "security", "transportation"]
pagesLoaded=4;


class Article:
    def __init__(self, title, author, date, content,description,category,url, tags=None, listicle=False):
            self.title=title
            self.author=author
            self.date=date   #type datime.datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
            self.content=content
            self.description=description
            self.category=category
            self.tags=tags
            self.url=url
            self.listicle=listicle
            
    
    def show(self):
            print("title: "+str(self.title.encode("utf-8")))
            print("description: "+str(self.description.encode("utf-8")))
            print("author: "+self.author)
            print("date: "+str(self.date))
            print("tags: ")
            for i in self.tags:
                print(i)
            print("url: "+str(self.url))
            

            
            
            
            
def getArticles(url, category):
    articleCategory=category
    #parsing the main category's page
    soup=BeautifulSoup(url, "html.parser")
    leftBar=soup.findChildren("div", {"class":"pagination-container"})
    articles=leftBar[0].findAll("a", {"class":"clearfix pad"})
    
       
    result=[]
    for article in articles:
        articleUrl=article['href']
        articleTitle=article.find("h2", {"class":"title"}).text  
        articleDescription=article.find("p", {"class":"exchange-sm"}).text
       
        #PARSING THE ARTICLE'S PAGE
        soupArticle=BeautifulSoup(urllib.request.urlopen(articleUrl), "html5lib")
        
          
        articleDateTime=datetime.datetime.strptime(soupArticle.find("meta",{"name":"DisplayDate"})["content"], "%Y-%m-%d").date()
        articleAuthor=soupArticle.find("meta", {"name":"Author"})["content"]
       
        articleTags=[]
        try:
            tags=soupArticle.find("ul", {"id":"article-tags"}).findChildren("li")
            
            for tag in tags:
                articleTags.append(tag.find("a").text)
        except:
            articleTags.append(None)
            
            
        #GETTING ARTICLE'S CONTENT FROM THE ARTICLE'S PAGE
        
        try:
            
            articleBody=soupArticle.find("article", {"itemprop":"articleBody"})   #if that fails, it's "post" article
       
            wt=articleBody.findAll("div", {"id":"wired-tired"})
            if (len(wt)!=0):
                    soupArticle=BeautifulSoup(urllib.request.urlopen(articleUrl), "html.parser")
                    articleBody=soupArticle.find("article", {"itemprop":"articleBody"})   
                    wt2=articleBody.findAll("div", {"id":"wired-tired"})
                    
                    for i in wt2:
                            i.extract()
                            
                            
             #LISTICLE TEST
            articleDivContentTags=articleBody.findAll("div", {"class":"sm-col-9 med-col-18 big-col-6 col marg-t-med marg-r-none "})
            #if the article is listicle, each div contains headers and one of the double texts
            articleListicle=False  #don't know yet
            
            #FOR LISTICLES
            if len(articleDivContentTags)!=0:  #the article is listicle and has no direct text children
                articleListicle=True
                
                #listicles have intros
                articleIntroList=articleBody.find("div", {"id":"listicle-intro"}).findAll("p")
                articleIntro=""
                for p in articleIntroList:
                        articleIntro+=p.text
                
                
                articleContentTagsTemp=[]
                for i in range(0, len(articleDivContentTags)):
                    articleContentTagsTemp.append(articleDivContentTags[i].findChildren(["h1","h2","h3","h4","p"]))
                articleContentTags=[]
                for textTagsList in articleContentTagsTemp:
                    for textTag in textTagsList:
                        articleContentTags.append(textTag) 
                
            #FOR NON-LISTICLES
            else:
                articleContentTags=articleBody.findChildren(["h1", "h2","h3", "p"], recursive=False)
            
        #for "post" articles
        except:
            articleBody=soupArticle.find("div",{"class":"post"})
            
            articleContentTags=articleBody.findChildren(["h1", "h2","h3", "p"])

        #finished with article types, that executes for all articles:
        articleContent=""
        
        #for listicles
        if articleListicle:
            articleContent+=articleIntro
            articleContent+="\n"
        
        #for all articles
        for textTag in articleContentTags:
                articleContent+="\n"
                articleContent+=textTag.text
                
        result.append(Article(articleTitle, articleAuthor, articleDateTime,articleContent,articleDescription, articleCategory, articleUrl, articleTags,articleListicle))

        
    return result
    

          
    
class Wired:
        def __init__(self, pages=4):
            #self.category - after data is parsed, consists of n(=self.pages) lists of Article objects
            self.business=[]
            self.culture=[]
            self.design=[]
            self.gear=[]
            self.science=[]
            self.security=[]
            self.transportation=[]
            
            self.pages=pages
            self.categories=["business", "culture", "design", "gear", "science", "security", "transportation"]
            
            self.articlesNumber=0
            self.categoriesParsed=[]
            
            
            self.attributes=[self.business, self.culture, self.design, self.gear, self.science, self.security, self.transportation]

            
        def parse(self, category=None):
                url="http://www.wired.com/category/"
                #headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' }
                
                #FOR A SELECTED CATEGORY
                if category and category in self.categories:
                    self.categoriesParsed.append(category)
                    
                    url+=category
                    url+="/page/"
                    categoryIndex=self.categories.index(category)
                    for page in range(1,self.pages+1): 
                        print(url+str(page))
                        finalUrl=urllib.request.urlopen(url+str(page), timeout=4)
                        self.attributes[categoryIndex].append(getArticles(finalUrl, category))
                        self.articlesNumber+=10
                        
                        
                #FOR ALL CATEGORIES
                else:
                    self.articlesNumber=0
                    self.categoriesParsed=self.categories[:]
                    #if constructor is empty or there's a mistake - take data for all categories
                    for categoryId in range(0, len(self.categories)):
                         for page in range(1, self.pages+1):
                            print(url+self.categories[categoryId]+"/page/"+str(page))
                            finalUrl=urllib.request.urlopen(url+self.categories[categoryId]+"/page/"+str(page))
                            self.attributes[categoryId].append(getArticles(finalUrl, self.categories[categoryId]))
                            self.articlesNumber+=10
                            
                            
        def show(self):
                print("articles total: "+str(self.articlesNumber))
                
                print("present categories: ")
                for i in self.categoriesParsed:
                        print(i, end="; ")
                print()
                
                print("articles per category: "+str(self.pages*10))
                                
                                
                
           


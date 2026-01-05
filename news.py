import requests
import os
import time
class FetchNews:
    #url 1 for the top headlines endpoint and url2 for the everything endpoint
    url1="https://newsapi.org/v2/top-headlines"
    url2="https://newsapi.org/v2/everything"
    #constructor for ch variable to assign the url based on the input
    def __init__(self,ch):
        if ch==1:
            self.__url=FetchNews.url1
        else:
            self.__url=FetchNews.url2
        if os.path.exists("apikey.txt"):
            with open("apikey.txt","r")as f:
                self.__api_key=f.readline().strip()
        else:
            print("Please Make an apikey.txt file and enter the api key in it")
            quit()
        #list of parameters to get the news
        self.__parameters={"apiKey":self.__api_key,"language":"en"}
    #get news function which gets a response from news api using the url and parameters, checks if the status is ok then prints the news else displays the error
    def get_news(self):
        response=requests.get(self.__url,params=self.__parameters)
        raw_news=response.json()
        if raw_news["status"] == "ok":
            return raw_news
        else:
            print(f"Status : {raw_news["status"]}")
            print(f"Error Code: {raw_news["code"]}")
            print(f"Description : {raw_news["message"]}")
            self.clear_parameters()
    #function to add a parameter to the parameters dictionary
    def add_parameter(self,key,value):
        self.__parameters[key]=value
    #function to remove parameter except the api key
    def delete_parameter(self,parameter):
        if parameter in self.__parameters:
            if parameter!="apiKey":
                del self.__parameters[parameter]
            else:
                print("Cannot Delete The Api Key. To Change the api key remove the previous api key and insert new api in the apikey.txt file")
    def clear_parameters(self):
        self.__parameters={k:v for k,v in self.__parameters.items() if k=="apiKey"or k=="language"}
#a class to format the raw news into displayable format
class FormatNews:
    def __init__(self,news):
        self.raw_news=news
    #to display news based on the count variable if count not equals to 0 else print all the news
    def display(self,count):
        if count:
            for c,news in enumerate(self.raw_news["articles"]):
                if c<count:
                    print(f"{'-'*64}")
                    if news["title"]:
                        print(f"Title : {news["title"]}")
                    else:
                        print("Title: No Title Available")
                    if news["description"]:
                        print(f"Description : {news["description"]}")
                    else:
                        print("Description : No Description Available")
                    print(f"{'-'*64}\n")
        else:
            for news in self.raw_news["articles"]:
                print(f"{'-'*64}")
                if news["title"]:
                        print(f"Title : {news["title"]}")
                else:
                    print("Title: No Title Available")
                if news["description"]:
                    print(f"Description : {news["description"]}")
                else:
                    print("Description : No Description Available")
                print(f"{'-'*64}\n")
#a Menu class to handle user input and command line
class Menu:
    #A dictionary of available languages with their language code
    languages={"ar":"Arabic","de":"German","en":"English","es":"Spanish","fr":"Frech","it":"Italian","nl":"Dutch","pt":"Portuguese","ru":"Russian"}
    
    @staticmethod
    def clear_screen():
        os.system("cls") if os.name=="nt" else os.system("clear")
    #a static method to make a function to sort news it takes an obj parameter which is an instance of the news class
    @staticmethod
    def sorting(obj,ch):
        if ch==1:
            obj.add_parameter("sortBy","relevancy")
        elif ch==2:
            obj.add_parameter("sortBy","popularity")
        elif ch==3:
            obj.add_parameter("sortBy","publishedAt")
        else:
            obj.add_parameter("sortBy",None)
    #A function to display news based on the source
    def news_source(self,obj):
        try:
            print(f"\n{"-"*64}\n")
            opt=int(input("1. BBC News\n2. ABC News\n3. CNN News\n4. Fox News\n5. Exit: "))
            if opt==1:
                self.display_news(obj,"sources","bbc-news")
                
            elif opt==2:
                self.display_news(obj,"sources","abc-news")
                
            elif opt==3:
                self.display_news(obj,"sources","cnn")
                
            elif opt==4:
                self.display_news(obj,"sources","fox-news")
                
            elif opt==5:
                return
            else:
                print("Invalid Choice!")
        except ValueError:
            print("Please Enter A Number")
    #A function to display news based on category
    def news_category(self,obj):
        try:
            print(f"\n{"-"*64}\n")
            opt=int(input("1. Business\n2. Entertainment\n3. General\n4. Health\n5. Science\n6. Sports\n7. Technology\n8. Exit: "))
            if opt==1:
                self.display_news(obj,"category","business")
            elif opt==2:
                self.display_news(obj,"category","entertainment")
            elif opt==3:
                self.display_news(obj,"category","general")
            elif opt==4:
                self.display_news(obj,"category","health")
            elif opt==5:
                self.display_news(obj,"category","science")
            elif opt==6:
                self.display_news(obj,"category","sports")
            elif opt==7:
                self.display_news(obj,"category","technology")
            elif opt==8:
                return
            else:
                print("Invalid Choice!")
        except ValueError :
            print("Please Enter A Number")
    #A function for utility 
    def news_utility(self,obj):
        try:
            print(f"\n{"-"*64}\n")
            n=int(input("1. Clear All Parameters\n2. Clear Screen\n3. Change Language\n4. Exit: "))
            if n==1:
                obj.clear_parameters()
            elif n==2:
                Menu.clear_screen()
            elif n==3:
                for k,v in Menu.languages.items():
                    print(f"{k}:{v}")
                lang=input("\nEnter The Language Code: ")
                if lang in Menu.languages:
                    obj.add_parameter("language",lang)
                else:
                    print("Please Enter A Valid Language")
            elif n==4:
                return
            else:
                print("Invalid Choice!")
        except ValueError  :
            print("Please Enter A Number")
    #it displays the news options and does operations based on user input, this also takes an newsobj parameter as an instance to call the instance methods
    def news_Options(self,newsobj):
        while True:
            try:
                print(f"\n{"-"*64}\n")
                n=int(input("1. Get News Based On Source\n2. Get News Based On Category\n3. Get News Based On Keyword\n4. Utilities\n5. Exit: "))
                if n==1:
                    #deleting the category parameter because of confliction with sources parameter
                    newsobj.delete_parameter("category")
                    self.news_source(newsobj)
                elif n==2:
                    #deleting the sources parameter because of confliction with category parameter
                    newsobj.delete_parameter("sources")
                    self.news_category(newsobj)
                elif n==3:
                    kw=input("Enter The Keyword: ")
                    self.display_news(newsobj,"q",kw)
                elif n==4:
                    self.news_utility(newsobj)
                elif n==5:
                    return
                else:
                    print("Invalid Choice")
            except ValueError:
                print("Please Enter A Number")
    #function to display news based on the parameter key and parameter value, this also takes a news instance and calls the instance functions
    def display_news(self,news,parameter,val):
        news.add_parameter(parameter,val)
        try:
            count=int(input("\nEnter The Number Of News You Want To Get(0 to get all news): "))
            try:
                sort=int(input("\n1. Sort By Relevancy\n2. Sort By Popularity \n3. Sort By Newest: "))
                Menu.sorting(news,sort)
                raw_news=news.get_news()
                if raw_news["articles"]:
                    displayer=FormatNews(raw_news)
                    displayer.display(count)
                else:
                    print("Sorry No News Found")
            except ValueError:
                print("Please Enter A Number")
        except ValueError:
            print("Please Enter A Number")
        
    
    # a main menu
    def main(self):
        print("-"*32)
        print("News App".center(32,"-"))
        print("-"*32)
        while True:
            print(f"\n{"-"*64}\n")
            try:
                ch=int(input("1. See Top Headline News\n2. See All Global News: "))
                news=FetchNews(ch)
                self.news_Options(news)
            except ValueError or KeyboardInterrupt:
                print("Please Enter A Number")

menu=Menu()
menu.main()

    
    
    

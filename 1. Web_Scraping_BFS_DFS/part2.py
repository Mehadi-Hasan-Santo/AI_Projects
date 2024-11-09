import dis
from operator import contains, is_
import re
import time
import nltk
from selenium import webdriver                   
from sumy.nlp.tokenizers import Tokenizer 
from sumy.parsers.plaintext import PlaintextParser 
from selenium.webdriver.common.by import By 
from prettytable import PrettyTable

table = PrettyTable()


def remove_all_sentence_except_english(text):
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    table.field_names = ["Sentence"]
    #table.add_row([text])
    #table.add_row("Sentence", "text")
    print(text)
    return text
def textSummerize(text):
    text = text.replace("\n", " ")  
    table.field_names = ["Sentence"]
    #table.add_row([text])
    print(text)
    parser = PlaintextParser.from_string(text,Tokenizer("english"))     
    from sumy.summarizers.text_rank import TextRankSummarizer                 
    #table.add_row("Sentence", "text", "text")
    print(parser.document)
    summarizer = TextRankSummarizer()  
    print(parser.document)                
    summary =summarizer(parser.document,2)  
    print(parser.document)
    #table.add_row("Sentence", "text", "text")                 
    text_summary=""                  
    for sentence in summary:                
        text_summary+=str(sentence) 
        print(text_summary)        
        #table.add_row("Sentence", "text", "text")            
    return text_summary   


def fileClearDFS():
    open('textDFS.txt', 'w').close()
    open('textDFS1.txt', 'w').close()
    open('linksDFS.txt', 'w').close()


def fileClearBFS():
    open('textBFS.txt', 'w').close()
    open('textDFS1.txt', 'w').close()
    open('linksBFS.txt', 'w').close()

def fileAddDFS(data):
    file = open("linksDFS.txt", "a")
    file.write(data + "\n")
    open('textDFS1.txt', 'w').close()
    file.close()

def fileAddBFS(data):
    file = open("linksBFS.txt", "a")
    file.write(data + "\n")
    open('textDFS1.txt', 'w').close()
    file.close()


def fileAddTextDFS(data):
    print(data)
    txt=""
    if data["text"]!="\n" and  data["text"] !="" :
        txt += data["text"]
    
    
    txt += "\n\n"
    file = open("textDFS.txt", "a")
    file.write(txt + "\n")
    file.close()

def fileAddTextBFS(data):
    print(data)
    txt = ""
    if data["text"]!="\n" and  data["text"] !="" :
        txt += data["text"]
    txt += "\n\n"
    file = open("textBFS.txt", "a")
    txt += "\n\n"
    file.write(txt + "\n")
    txt += "\n\n"
    file.close()



def is_subset(subset, string):
    string = string.lower()
    subset = subset.lower()
    return subset in string


def scrape_pTag_text(driver):
    pTag = driver.find_elements(By.TAG_NAME, "p")
    text = ""
    for tag in pTag:
        text += tag.text
      
    
    text = remove_all_sentence_except_english(text)
    #table.add_row([text])
    print(text)
    text = textSummerize(text)
    return text


class Search:
    def __init__(self):
        self.Graph = {}
        self.Node ={}
        self.title=""
        self.start_node = ''
        self.targeted_text = ''
        self.description=''


    def get_all_links_with_selenium(self, url, targeted_text, method):
            goal = False
            driver = webdriver.Chrome()
            driver.set_page_load_timeout(30)
            #table.add_row([url])
            print(url)
            driver.get(url)
            #table.add_row([url])
            print(url)
            text = scrape_pTag_text(driver)
            #table.add_row([url])
            print(url)
            data = {"node":self.Node[url], "text":text}
            
            if method == "DFS":
                fileAddTextDFS(data) 
            else:
                fileAddTextBFS(data)
                print("BFS") 
                #table.add_row([url])
            goal = self.is_reach_goal(text=text, targeted_text=targeted_text)
            if goal:
                #table.add_row([url])
                print(url)
                if method == "DFS":
                    BFS(self.start_node, self.targeted_text)
                else:
                    print("Goal reached")
                    quit()
            elements = driver.find_elements(By.TAG_NAME, "a")
            print(elements)
            navbar_links = driver.find_elements(By.XPATH, "//nav//a")
            print(navbar_links)

            non_navbar_links = [link for link in elements if link not in navbar_links]
            elements = non_navbar_links



            urls = []
            i = 0
            for element in elements:
                if i > 10:
                    break
                href = element.get_attribute("href")
                if href:
                    if not (is_subset("google",href) or is_subset("facebook",href) or is_subset("adobe",href)) :
                        if href not in urls:
                            #table.add_row([href])
                            print(href)
                            urls.append(href)
                            if method == "BFS":
                                print("BFS")
                                fileAddBFS(href)
                            else:
                                print("DFS")
                                fileAddDFS(href)
                            i += 1
            time.sleep(2)
            driver.quit()
            return urls, goal
       
        

    def is_reach_goal(self, text, targeted_text):
        for word in targeted_text:
            #table.add_row([word])
            print(word)
            if not is_subset(word, text):
                return False
        return True


    def DFS(self, graph, node, targeted_text,  visited = None, distance=0):
       
        distance += 1 
        if distance > 3:
            return
        if visited is None:
            visited = set()
        if node not in visited:
            #table.add_row(node, distance)
            print(node, distance)
            visited.add(node)
            urls, goal = self.get_all_links_with_selenium(node, targeted_text, "DFS")
            print(node, distance)
            #table.add_row([node, distance])
            print(node, distance)
            if urls:
                print(urls[0])
            graph[node] = urls
            for neighbour in graph[node]:
                #table.add_row([neighbour])
                print(neighbour)
                if neighbour not in visited:
                    #table.add_row([neighbour])
                    print(neighbour)
                    self.Node[neighbour] = {"url":neighbour, "parent":node, "Parent_Distance":distance, "URL":neighbour,"Distance":distance+1}
                    #table.add_row([neighbour])
                    print(neighbour)
                    self.DFS(graph, neighbour,targeted_text, visited, distance)
        return visited
    
    def BFS(self, graph, start, targeted_text, visited = None):
        if visited is None:
            #table.add_row([start])
            print(start)
            visited = set()
        queue = [start]
        #table.add_row([start])
        print(start)
        visited.add(start)
        distance = 0
        #table.add_row([start])
        print(start)
        while queue:
            s = queue.pop(0)
            #table.add_row([s])
            print(s)
            if self.Node[s]["Distance"] > 3:
                pass
            #table.add_row([s])
            print(s)
            distance = self.Node[s]["Distance"]
            urls, goal = self.get_all_links_with_selenium(s, targeted_text, "BFS")
            #table.add_row([s])
            print(s)
            graph[s] = urls
            for neighbour in graph[s]:
                if neighbour not in visited:
                    #table.add_row([neighbour])
                    print(neighbour)
                    self.Node[neighbour] = {"url":neighbour, "parent":s, "Parent_Distance":distance, "URL":neighbour,"Distance":distance+1}
                    #table.add_row([neighbour])
                    print(neighbour)
                    queue.append(neighbour)
                    visited.add(neighbour)
                    #table.add_row([neighbour])
                    print(neighbour)
        return visited


def BFS(start_node, targeted_text):
        my_graph = Search()
        search = start_node
        #table.add_row([start_node])
        print("DFS starting from node", start_node)
        start_node = 'https://www.google.com/search?q=' + start_node
        print("DFS starting from node", start_node)
        #table.add_row([start_node])
        print("DFS starting from node", start_node)
        my_graph.Graph = {start_node: []}

        my_graph.Node[start_node] = {"url":start_node, "parent":"None", "Parent_Distance":0, "URL":start_node,"Distance":1}
        #table.add_row([start_node])
        print("DFS starting from node", start_node)
        fileClearBFS()
        file = open("textBFS.txt", "a")
        #table.add_row([start_node])
        print("DFS starting from node", start_node)
        file.write("Search Term: "+search+"\n"+ "Target: "+targeted_text + "\n\n")
        file.close()
        #table.add_row([start_node])
        print("DFS starting from node", start_node)
        my_graph.BFS(my_graph.Graph, start_node, targeted_text=targeted_text)

def DFS(start_node, targeted_text):
        
        my_graph = Search()
        search = start_node
        #table.add_row([start_node])
        print("DFS starting from node", start_node)
        start_node = 'https://www.google.com/search?q=' + start_node
        print("DFS starting from node", start_node)
        my_graph.start_node = start_node
        #table.add_row([start_node])
        print("DFS starting from node", start_node)

        my_graph.targeted_text = targeted_text
        my_graph.Graph = {start_node: []}
        #table.add_row([start_node])
        print("DFS starting from node", start_node)

        my_graph.Node[start_node] = {"url":start_node, "parent":"None", "Parent_Distance":0, "URL":start_node,"Distance":1}
        #fileClearDFS()

        file = open("textDFS.txt", "a")
        file.write("Search Term: "+search+"\n"+ "Target: "+targeted_text + "\n\n")
        file.close()
        #table.add_row([start_node])
        print("DFS starting from node", start_node)
        my_graph.DFS(my_graph.Graph, start_node, targeted_text=targeted_text)
        

if __name__ == "__main__":
    start_node = input('What would you like to search on Google?\n')
    targeted_text = input('What are you looking for?\n')
    #table.add_row([start_node])
    print("DFS starting from node", start_node)
    DFS(start_node, targeted_text)
    





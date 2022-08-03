import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()                
chrome_options.add_argument("--headless")

URL = input("Enter the URL of the website you want the HTML of:")                   #Input your desired web page
driver = webdriver.Chrome(options=chrome_options)

print("Loading :"+URL+"\n")
driver.get(URL)                                                                     #This will load the web page requested above
time.sleep(2)
URL_HTML = driver.page_source                                                       #This will collect the HTML source code from web page


output_file=open("HTML_SourceCode.txt","w",encoding="utf-8")
print(URL_HTML, file=output_file)                                                   #This will output your desire HTMl source code to a .txt file
driver.close()

print("The HTML source code for "+URL+" has been saved to HTML_SourceCode.txt")     #Lets user know of the completion of the code
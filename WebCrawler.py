import math                                              #This is needed to use the math.floor() function for the final page index
import time                                              #This is needed for the time.sleep() functions needed for giving selenium enough time to load web pages 
import re                                                #This allows for the use of Regular Expressions
#import pyodbc                                            #This allows for database storage
import sqlite3                                           #This allows for .db file - not needed but wanted
from datetime import datetime                            #This allows for time stamps in each loop - not needed, but wanted 
from selenium import webdriver                           #This opens the web page in Google Chrome
from selenium.webdriver.chrome.options import Options    #Needed for Headless
chrome_options = Options()                               #Needed for Headless
chrome_options.add_argument("--headless")                #Headless runs the the program without ever really opening Chrome, and for a big index like the Russell 200 it saves us hours in elapse time


now=datetime.now()                         #Time stamp
current_time = now.strftime("%H:%M:%S")    #Time stamp
print("Program start time:", current_time, "\n") #Time stamp

driver = webdriver.Chrome(options=chrome_options)                         #Initiating ChromeDriver to a variable
desired_URL = input("Enter the FKnol URL of the Market Index or Category you want to analyze:")
FKnolURL_pattern=desired_URL+"?go=b###"  #Pattern of first FKnol web site


num_of_stocks = input("Enter the number of stocks in the Market Index or Category you want to analyze:")                            #Needed for final page index
page_index=math.floor(int(num_of_stocks)/100)*100                                                            #The final page index is the total number of stocks rounded down to the hundred (i.e Total stocks in index is 3529, then final page index is 3500

id_num=0                                                                                                #Primary Key for database
page_num=0                                                                                              #Sets page number on important Milestone print




#Database connections:

''' UNCOMMENT THIS SECTION TO HAVE THE CODE OUTPUT TO SSMS
#Establishing SSMS connection
print("Initiating SSMS database connection...")                     #Milestone print
SSMSconn = pyodbc.connect(driver='{SQL Server}',                    #Creating database connection
                      server='LAPTOP-6T58SDKI\SQLEXPRESS',          #Offline server (We were able to use an AWS server just for fun, but decided to go with the free alternative
                      database='SSMS_Financial_Data')               #Connects to specific database
SSMScursor = SSMSconn.cursor()

try:                                                                #Try is used to let user know id the table has already been created, avoids storing errors
    SSMScursor.execute("CREATE TABLE financial_data (\
                ID INTEGER PRIMARY KEY NOT NULL,\
                STOCK_TICKER varchar (50),\
                COMPANY varchar (50),\
                MARKET_CAP REAL,\
                YTD REAL,\
                PRICE REAL,\
                PE_RATIO REAL,\
                EPS REAL,\
                INDUSTRY_SECTOR varchar (50),\
                SUB_INDUSTRY_SECTOR varchar (70),\
                ANALYST_RECCOMENDATION varchar(50),\
                NUM_ANALYST_RECCOMENDATION varchar(50),\
                PATTERN varchar(50),\
                NUM_PATTERN varchar (50));")                             #Table and Fields have been created
    print("TABLE CREATED! \n")                                           #Milestone print
except:
    print("The table has already been created! \n")                      #Milestone print
'''




#Establishing SQLite3 connection
print("Initiating SQLite 3 database connection...")                      #Milestone print
SQLconn = sqlite3.connect('DB_Financial_Data.db')
SQLcursor = SQLconn.cursor()

#try:                                                                #Try is used to let user know id the table has already been created, avoids storing errors
SQLcursor.execute("CREATE TABLE financial_data (\
        ID INTEGER PRIMARY KEY NOT NULL,\
        STOCK_TICKER varchar (50),\
        COMPANY varchar (50),\
        MARKET_CAP REAL,\
        YTD REAL,\
        PRICE REAL,\
        PE_RATIO REAL,\
        EPS REAL,\
        INDUSTRY_SECTOR varchar (50),\
        SUB_INDUSTRY_SECTOR varchar (70),\
        ANALYST_RECCOMENDATION varchar(50),\
        NUM_ANALYST_RECCOMENDATION varchar(50),\
        PATTERN varchar(50),\
        NUM_PATTERN varchar (50));")            #Table and Fields have been created
    #print("TABLE CREATED! \n")                                              #Milestone print
#except:
    #print("The table has already been created! \n")                         #Milestone print


#Establishing connection to .txt output
print("Initiating .txt file connection...")                              #Milestone print
output_file=open("txt_Financial_Data (For Pandas).txt","w")
print("id_num"+"~"+"ticker"+"~"+"company"+"~"+"mkt_cap"+"~"+"ytd_gains"+"~"+"price"+"~"+"pe"+"~"+"eps"+"~"+"industry"+"~"+"sub_industry"+"~"+"valuation"+"~"+"NUMvaluation"+"~"+"pattern"+"~"+"NUMpattern", file=output_file) #Printing column names
print("The .txt connection has been established! \n")                    #Milestone print


#Main WebCrawler will now start:



for i in range(1,page_index+100,100):                                    #The page index pattern is as such: 0, 100, 200, ..., 2000
    page_num+=1                                                          #Sets page number on important Milestone print
    FKnolURL_new=FKnolURL_pattern.replace("###",str(i-1))                #Replacing pattern URL with page index
    print("Collecting data from page "+str(page_num)+": "+FKnolURL_new)  #Milestone print

    driver.get(FKnolURL_new)      #Opening the new URL with the replaced page index pattern value
    time.sleep(2)                 #Wait command - ensure full page load
    page_HTML=driver.page_source  #Retrieving the HTML source code
    
    page_loop_time=datetime.now()                           #Time stamp
    page_loop_elapse = page_loop_time.strftime("%H:%M:%S")  #Time stamp
    print("Page start time:", page_loop_elapse,"\n")        #Time stamp

    stock_blocks=re.compile(r"(<tr><td>.*?\).<b>.*?\n</td></tr>)",re.S|re.I).findall(page_HTML) #There are 100 chunks per page, each containing a different stock and it's information
    if len(stock_blocks)>0:                                                                     #Regular Expression for each stock chunk
        for single_stock_block in stock_blocks:
            
            id_num+=1                   #Setting the variables to blank at the beginning of each loop, although not necessary
            ticker_v1 = ""              #has proven to decrease the chances of errors in the higher id_num loops
            ticker_v2 = ""
            company_v1 = ""
            company_v2 = ""
            unit_mkt_cap = ""
            mkt_cap_v1 = ""
            mkt_cap_v2 = ""
            ytd_gains = ""
            price = ""
            pe = ""
            eps = ""
            industry = ""
            sub_industry_v1 = ""
            sub_industry_v2 = ""
            sub_industry_v3 = ""
            sub_industry_v4 = ""
            sub_industry_v5 = ""
            sub_industry_v6 = ""
            valuation = ""
            NUMvaluation = ""
            pattern = ""
            NUMpattern = ""
            
            upper_loop_time=datetime.now()                              #Time stamp
            upper_loop_elapse = upper_loop_time.strftime("%H:%M:%S")    #Time stamp
            
            print(id_num,"- Loop start time:", upper_loop_elapse)       #Time stamp
            print("Looking for first set of variables...")              #Milestone print

            
            ticker_v1=re.compile(r"<b>.*?\((.*?)\)</b>",re.I).findall(single_stock_block)                                     #Regular Expression initiated into variable
            if len(ticker_v1)>0:
                ticker_v1=ticker_v1[0]
                ticker_V2=ticker_v1.replace("MindMed) Inc. -  (MNMD","MNMD") #Single instance of failed RegEx
            
            print("- Collecting "+ticker_V2+"'s "+"data.")  #Milestone print

            company_v1=re.compile(r"<tr><td>.*?\) <b>(.*?) \(.*?\)</b>",re.S|re.I).findall(single_stock_block)             #Regular Expression initiated into variable
            if len(company_v1)>0:
                company_v1=company_v1[0]
                company_v2=company_v1.replace("'", "")
            
            mkt_cap_v1=re.compile(r"<td>\$(.*?) .*?</td><td>.*?%",re.I).findall(single_stock_block)                        #Regular Expression initiated into variable
            if len(mkt_cap_v1)>0:
                mkt_cap_v1=round((float(mkt_cap_v1[0])), 4)
                
            unit_mkt_cap=re.compile(r"<td>\$.*? (.*?)</td><td>.*?%",re.I).findall(single_stock_block)                      #Regular Expression initiated into variable
            if len(unit_mkt_cap)>0:
                unit_mkt_cap=unit_mkt_cap[0]
            
            million = 1000000                                                           #Setting variable for calculation
            billion = 1000000000                                                        #Setting variable for calculation
            if unit_mkt_cap == "million":                                               #The variable mkt_cap is a float (i.e 35.62) This will show mkt_cap always in units millions
                mkt_cap_v2 = round((float((mkt_cap_v1*million)/million)), 2)           #The variable unit_mkt_cap is the unit attached to mkt_cap (i.e billion)
            elif unit_mkt_cap == "billion":                                             #This IF block, calculates the integer equivalent of the two previous variables combined
                mkt_cap_v2 = round((float((mkt_cap_v1*billion)/million)), 2)        #i.e 35,620,000,000
            else:                                                                       #The else will serve its purpose in the event of a 'thousand' or 'trillion' mkt_cap (unlikely)
                mkt_cap_v2 = "ERROR"                                                    #Which is unlikely given the constraints of the Russell 2000 Index - but you never know
                
            ytd_gains=re.compile(r"</td><td>.*?</td><td>(.*?)%</td>",re.I).findall(single_stock_block)                      #Regular Expression initiated into variable
            if len(ytd_gains)>0:
                ytd_gains=round((float(ytd_gains[0])/100), 4)
            
            price=re.compile(r"</ul></td><td>\$(.*?)</td><td align=\"center\">",re.S|re.I).findall(single_stock_block)      #Regular Expression initiated into variable
            if len(price)>0:
                price=price[0]
            
            pe=re.compile(r"\$.*?<br>-<br>\$.*?</td><td align=\"center\">(.*?)</td>",re.S|re.I).findall(single_stock_block) #Regular Expression initiated into variable
            if len(pe)>0:
                pe=pe[0]
                
            eps=re.compile(r"\$.*?<br>-<br>\$.*?</td><td align=\"center\">.*?</td><td align=\"center\">.*?</td><td align=\"center\">(.*?)\n</td></tr>",re.S|re.I).findall(single_stock_block)  #Regular Expression initiated into variable
            if len(eps)>0:
                eps=eps[0]
            
            print("- First set of variables for "+ticker_V2+" have been found!")  #Milestone print

            
            print("Looking for "+ticker_V2+"'s industry...")  #Milestone print



            #First inner WebCrawler will now start:
            
            
                            
            try:                                                                 #Try is used here as to not break data collection because of errors
                ind_URL_pattern="https://fknol.com/stock/###.php"                #These web sites have longer load times, and the Try allows the code to 
                ind_starting_URL=ind_URL_pattern.replace("###",str(ticker_V2))      #running in the event of a random long load time
                print("- Checking "+ticker_V2+"'s "+"industry data at: "+ind_starting_URL)  #Milestone print
                try:                                                             #Most common source of error - usually due to long load times
                    driver.get(ind_starting_URL)                #Opening Industry web page
                    time.sleep(5)                               #Wait command - longer than usual to ensure full page load
                    print("- Industry webpage has been opened.")  #Milestone print
                    ind_HTML = driver.page_source               #Retrieving HTML source code
                    time.sleep(2)                               #Wait command - longer than usual to ensure full page load
                    print("- Industry HTML has been found.")      #Milestone print
                    
                    industry=re.compile(r"<tr><td>Primary Industry Sector:</td><td>(.*?)</td></tr>",re.S|re.I).findall(ind_HTML)    #Regular Expression initiated into variable
                    if len(industry)>0:
                        industry=industry[0]
                        if len(industry)<3:
                            industry = ""
                    
                    sub_industry_v1=re.compile(r"<tr><td>Seconday Sub-sector:</td><td>(.*?)</td></tr>",re.S|re.I).findall(ind_HTML) #Regular Expression initiated into variable
                    if len(sub_industry_v1)>0:
                        sub_industry_v1=str(sub_industry_v1[0])
                        sub_idustry_v2=sub_industry_v1.replace("&amp;", "and")
                        sub_industry_v3=sub_idustry_v2.replace("&amp;P", "")
                        sub_industry_v4=sub_industry_v3.replace("  ", " ")  
                        sub_industry_v5=sub_industry_v4.replace("EandP", "")
                        sub_industry_v6=sub_industry_v5.strip()
                        if len(sub_industry_v6)<3:
                            sub_industry_v6 = ""
                        
                    print("- "+ticker_V2+"'s industry data has been found!")                      #Milestone print
                except:
                    print("- There was an error when getting "+ticker_V2+"'s industry data!")  #Milestone print
            except:
                print("- There was an error when accessing YahooFinance!")                  #Milestone print
                           
            
            
            #Second inner WebCrawler will now start:
            
            
            
            print("Looking for "+ticker_V2+"'s valuation and pattern...")                           #Milestone print
            try:                                                                     #Try is used here as to not break data collection because of errors
                YH_URL_pattern="https://finance.yahoo.com/quote/###"                 #These web sites have longer load times, and the Try allows the code to
                YH_starting_URL=YH_URL_pattern.replace("###",str(ticker_V2))            #running in the event of a random long load time
                print("- Checking "+ticker_V2+"'s "+"valuation and pattern at: "+YH_starting_URL)      #Milestone print
                try:
                    driver.get(YH_starting_URL)                                      #Opening Valuation and Pattern web page
                    time.sleep(5)                                                    #Wait command - longer than usual to ensure full page load
                    print("- Valuation and pattern webpage has been opened.")          #Milestone print
                    YH_HTML = driver.page_source
                    time.sleep(2)                                                    #Wait command - longer than usual to ensure full page load
                    print("- Valuation and pattern HTML has been found!")              #Milestone print
                    
                    valuation=re.compile(r"XX\.XX</div><div class=\"Fw\(b\) Fl\(end\)--m Fz\(s\) C\(\$primaryColor\)\">(.*?)</div>",re.S|re.I).findall(YH_HTML) #Regular Expression initiated into variable
                    if len(valuation)>0:
                        valuation=valuation[0].upper()
                        if len(valuation)<4:
                            valuation = ""
                        if valuation == "OVERVALUED":
                            NUMvaluation = -1
                        elif valuation == "UNDERVALUED":
                            NUMvaluation = 1
                        elif valuation == "NEAR FAIR VALUE":
                            NUMvaluation = 0
                        else:
                            NUMvaluation = "" 
                    print("- "+ticker_V2+"'s valuation has been found!")                    #Milestone print
                
                    pattern=re.compile(r"<span class=\"Fw\(b\) D\(b\)--mobp C\(\$.*?\)\"><span>(.*?)</span></span>",re.S|re.I).findall(YH_HTML)   #Regular Expression initiated into variable
                    if len(pattern)>0:
                        pattern=pattern[0].upper()
                        if len(pattern)<3:
                            pattern = ""
                        if pattern == "BEARISH":
                            NUMpattern = -1
                        elif pattern == "BULLISH":
                            NUMpattern = 1
                        elif pattern == "NEUTRAL":
                            NUMpattern = 0
                        else:
                            NUMpattern = ""
                            
                    print("- "+ticker_V2+"'s pattern has been found.")                      #Milestone print
                
                except:
                    print("- There was an error when getting "+ticker_V2+"'s valuation and pattern from Yahoo Finance!")  #Milestone print            
            except:
                print("- There was an error when accessing YahooFinance!")            #Milestone print
               
            
            
            
            #Database storage will now start
            
            
            print("Storing into database...")               #Milestone print
            
            ID = str(id_num)                                #Initializing variables into SQL columns
            STOCK_TICKER = str(ticker_V2)
            COMPANY = str(company_v2)
            MARKET_CAP = str(mkt_cap_v2)
            YTD = str(ytd_gains)
            PRICE = str(price)
            PE_RATIO = str(pe)
            EPS = str(eps)
            INDUSTRY_SECTOR = str(industry)
            SUB_INDUSTRY_SECTOR = str(sub_industry_v6)
            ANALYST_RECCOMENDATION = str(valuation)
            NUM_ANALYST_RECCOMENDATION =str(NUMvaluation)
            PATTERN = str(pattern)
            NUM_PATTERN = str(NUMpattern)

            
            time.sleep(1)                                  #Wait command - Decreases chance of error when saving to database
            
            ''' UNCOMMENT THIS SECTION TO HAVE THE CODE OUTPUT TO SSMS
            #Storing into SSMS
            print("- Storing data into the SSMS database.")     #Milestone print
            try:
                SSMScursor.execute("INSERT INTO financial_data VALUES ('"+ID+"','"+STOCK_TICKER+"','"+COMPANY+"','"+MARKET_CAP+"','"+YTD+"','"+PRICE+"','"+PE_RATIO+"','"+EPS+"','"+INDUSTRY_SECTOR+"','"+SUB_INDUSTRY_SECTOR+"','"+PATTERN+"','"+ANALYST_RECCOMENDATION+"')") #Importing variables into database columns
                SSMSconn.commit()   #In the event of an early termination or error, a commit() inside the main loop allows for a recovery of the database up until the interruption
                                    #An inner-loop commit() also allows for access to a constantly updating database while the code is still running
                print("- "+ticker_V2+"'s data has been stored into the SSMS database!") #Milestone print
            except:
                print("- There was an error when storing "+ticker_V2+"'s data into the SSMS database!")  #Milestone print
            '''
            #Storing into SQLite
            print("- Storing data into the .db file.")     #Milestone print
            try:
                SQLcursor.execute("INSERT INTO financial_data VALUES ('"+ID+"','"+STOCK_TICKER+"','"+COMPANY+"','"+MARKET_CAP+"','"+YTD+"','"+PRICE+"','"+PE_RATIO+"','"+EPS+"','"+INDUSTRY_SECTOR+"','"+SUB_INDUSTRY_SECTOR+"','"+ANALYST_RECCOMENDATION+"','"+NUM_ANALYST_RECCOMENDATION+"','"+PATTERN+"','"+NUM_PATTERN+"')") #Importing variables into database columns
                SQLconn.commit()    #In the event of an early termination or error, a commit() inside the main loop allows for a recovery of the database up until the interruption
                                    #An inner-loop commit() also allows for access to a constantly updating database while the code is still running    
                print("- "+ticker_V2+"'s data has been stored into the .db file!")       #Milestone print
            except:
                print("- There was an error when storing "+ticker_V2+"'s data into the .db file!")  #Milestone print

            #Printing to .txt output - the separator in this case will be ~ instead of a ,
            print("- Storing data into the .txt file.")     #Milestone print
            try: #For consistency with previous connections - no history of errors for .txt storing
                print(str(id_num)+"~"+str(ticker_V2)+"~"+str(company_v2)+"~"+str(mkt_cap_v2)+"~"+str(ytd_gains)+"~"+str(price)+"~"+str(pe)+"~"+str(eps)+"~"+str(industry)+"~"+str(sub_industry_v6)+"~"+str(valuation)+"~"+str(NUMvaluation)+"~"+str(pattern)+"~"+str(NUMpattern), file=output_file)
                print("- "+ticker_V2+"'s data has been stored into the .txt file!")      #Milestone print
                output_file.flush()
            except:
                print("- There was an error when storing "+ticker_V2+"'s data into the .txt file! \n")  #Milestone print

            lower_loop_time=datetime.now()                                  #Time stamp
            lower_loop_elapse = lower_loop_time.strftime("%H:%M:%S")        #Time stamp
            print("Loop end time:", lower_loop_elapse, "\n")

#Code has looped until the final page index and program is now ending:

''' UNCOMMENT THIS SECTION TO HAVE THE CODE OUTPUT TO SSMS
SSMSconn.commit() #Outer loop saving and closing - final time SSMS
SSMSconn.close()
'''
SQLconn.commit() #Outer loop saving and closing - final time SQL
SQLconn.close()
output_file.close()

driver.close()
print("All data has been stored. Collection Complete") #Milestone print


end_program=datetime.now()                             #Time stamp
total_elapse = end_program.strftime("%H:%M:%S")        #Time stamp
print("WebCrawler end time:", total_elapse, "\n")         #Time stamp

print("Starting Analyses...")
import Analyses                                        #Starts Analysis and importing functions

#Analysis
Analyses.LinearReg()
Analyses.DescriptiveAnalysis()
Analyses.TextMining()
Analyses.SentimentAnalysis()
Analyses.AdditionalAnalysis()


#LR Plots
Analyses.mkt_plot()
Analyses.price_plot()
Analyses.pe_plot()
Analyses.eps_plot()

print("\nAll data collection, analysis, and plotting has been completed!")
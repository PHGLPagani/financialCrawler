import pandas as pd                                                     #Needed for database analysis
from sklearn import linear_model
from sklearn.linear_model import LinearRegression                       #Needed for linear regression
from tabulate import tabulate                                           #Needed to put results into neat tables
import matplotlib.pyplot as plt


'''
Linear Regression
'''
def LinearReg():
    lr_output=open("Linear Regression.txt", "w")                            #Creating LINEAR REGRESSION output file
    LRdata=pd.read_csv("txt_Financial_Data (For Pandas).txt", sep="~")        #Reading from file
    print("Data Preview:")
    print("Data Preview:", file=lr_output)
    print(LRdata)                                                             #Printing Data                
    print(LRdata, file=lr_output)
    
    x=LRdata[["mkt_cap","price","pe","eps"]].to_numpy()                       #Specifying the X variable
    y=LRdata[["ytd_gains"]].to_numpy()                                        #Specifying the Y variable
    
    model = LinearRegression()                                              #Creating the Linear Regression Model
    model.fit(x, y)                                                         #Assigning columns as axis
    
    
    coef1, coef2, coef3, coef4 = model.coef_[0]                             #Strips the tuple
    
    
    mkt_cap_coef = coef1
    price_coef = coef2
    pe_coef = coef3
    eps_coef = coef4
    R2 = model.score(x, y)
    
    print("\nStarting Linear Regression...")                                        #Printing regression results into table
    print("Coefficient(s) and R2:")
    print("Coefficient(s) and R2:", file=lr_output)
    LRdf = pd.DataFrame({"MKT_CAP" : [mkt_cap_coef],
                       "PRICE" : [price_coef],
                       "PE_RATIO" : [pe_coef],
                       "EPS" : [eps_coef],
                       "R2" : [R2]})
    print(tabulate(LRdf, headers="keys", tablefmt="psql"))
    print(tabulate(LRdf, headers="keys", tablefmt="psql"), file=lr_output)
    lr_output.close()
    
    print("Linear Regression is complete!\n\n")


'''
Descriptive Analysis
'''
def DescriptiveAnalysis():
    DA_output=open("Descriptive Analysis.txt", "w")                                                #Creating output file
    print("Starting Descriptive Analysis...")
    DAdata=pd.read_csv(r"txt_Financial_Data (For Pandas).txt", sep="~")                            #Reading from data
    print("Here is a description of the data:")
    print("Here is a description of the data:", file=DA_output)
    print(DAdata[["mkt_cap", "ytd_gains", "price", "pe", "eps"]].describe())                       #Describing the data
    print(DAdata[["mkt_cap", "ytd_gains", "price", "pe", "eps"]].describe(), file=DA_output)
    DA_output.close()
    
    print("Descriptive Analysis is complete!\n\n")
    

'''
Text Mining
'''
def TextMining():
    print("Starting Text Mining...")                                                #Creating input and output files
    TMval_input=open("txt_Financial_Data (For Pandas).txt")
    TMpat_input=open("txt_Financial_Data (For Pandas).txt")
    TM_output=open("Market Counter.txt", "w") 
    
    #VALUATION variables
    TMover_counter=0
    TMunder_counter=0
    TMfair_counter=0
    
    #PATTERN variables
    TMbear_counter=0
    TMbull_counter=0
    TMneutral_counter=0
    
    #VALUATION Counter
    print("Market Valuation Counts:", file=TM_output)                               #Counting the number of valuation instances
    for TMval_record in TMval_input:
        TMval_data_points=TMval_record.split("~")
        for TMval_data_point in TMval_data_points:
            if TMval_data_point == "OVERVALUED":
                TMover_counter+=1
            elif TMval_data_point == "UNDERVALUED":
                TMunder_counter+=1
            elif TMval_data_point == "NEAR FAIR VALUE":
                TMfair_counter+=1
                
    SA_PATdf=pd.DataFrame({"OVERVALUED" : [TMover_counter],
                       "UNDERVALUED" : [TMunder_counter],
                       "NEAR FAIR VALUE" : [TMfair_counter]})
    print(tabulate(SA_PATdf, headers="keys", tablefmt="psql"))
    print(tabulate(SA_PATdf, headers="keys", tablefmt="psql"), file=TM_output)
    
    #PATTERN Counter
    print("Market Pattern Counts:", file=TM_output)                                #Counting the number of pattern instances
    for TMpat_record in TMpat_input:
        TMpat_data_points=TMpat_record.split("~")
        for TMpat_data_point in TMpat_data_points:
            if TMpat_data_point == "BEARISH":
                TMbear_counter+=1
            elif TMpat_data_point == "BULLISH":
                TMbull_counter+=1
            elif TMpat_data_point == "NEUTRAL":
                TMneutral_counter+=1
    
    SA_PATdf=pd.DataFrame({"BEARISH" : [TMbear_counter],
                       "BULLISH" : [TMbull_counter],
                       "NEUTRAL" : [TMneutral_counter]})
    print(tabulate(SA_PATdf, headers="keys", tablefmt="psql"))
    print(tabulate(SA_PATdf, headers="keys", tablefmt="psql"), file=TM_output)    #Printing text mining results into table
    
    TM_output.close()
    TMval_input.close()
    TMpat_input.close()
    print("Text mining is complete!\n\n")


'''
Sentiment Analysis
'''
def SentimentAnalysis():
    print("Starting Sentiment Analysis...")
    SAval_input=open("txt_Financial_Data (For Pandas).txt", "r")
    SApat_input=open("txt_Financial_Data (For Pandas).txt", "r")
    SA_output=open("Market Sentiment.txt", "w")
    
    #VALUATION variables
    SAover_counter=0
    SAunder_counter=0
    SAfair_counter=0
    
    #PATTERN variables
    SAbear_counter=0
    SAbull_counter=0
    SAneutral_counter=0
    
    #VALUATION Counter
    print("Market Valuation Sentiment:")
    print("Market Valuation Sentiment:", file=SA_output)
    for SAval_record in SAval_input:
        SAval_data_points=SAval_record.split("~")
        for SAval_data_point in SAval_data_points:
            if SAval_data_point == "-1":
                SAover_counter+=-1
            elif SAval_data_point == "1":
                SAunder_counter+=1
            elif SAval_data_point == "0":
                SAfair_counter+=1
                
    SAval_total = SAover_counter+SAunder_counter
    SA_VALdf=pd.DataFrame({"MARKET" : [SAval_total],
                       "NEUTRAL" : [SAfair_counter]})
    print(tabulate(SA_VALdf, headers="keys", tablefmt="psql"))
    print(tabulate(SA_VALdf, headers="keys", tablefmt="psql"), file=SA_output)    #Printing text mining results into table
    
    #PATTERN Counter
    print("Market Pattern Sentiment:")
    print("Market Pattern Sentiment:", file=SA_output)
    for SApat_record in SApat_input:
        SApat_data_points=SApat_record.split("~")
        for SApat_data_point in SApat_data_points:
            if SApat_data_point == "-1\n":
                SAbear_counter+=-1
            elif SApat_data_point == "1\n":
                SAbull_counter+=1
            elif SApat_data_point == "0\n":
                SAneutral_counter+=1  
    
    SApat_total = SAbear_counter+SAbull_counter
    SA_PATdf=pd.DataFrame({"MARKET" : [SApat_total],
                       "NEUTRAL" : [SAneutral_counter]})
    print(tabulate(SA_PATdf, headers="keys", tablefmt="psql"))
    print(tabulate(SA_PATdf, headers="keys", tablefmt="psql"), file=SA_output)    #Printing text mining results into table
    
    SApat_input.close()
    SAval_input.close()
    SApat_input.close()
    print("Sentiment Analysis is complete!\n\n")


'''
Additional Analysis
'''
def AdditionalAnalysis():
    add_output=open("Additional Analysis.txt", "w")  
    AAdata=pd.read_csv("txt_Financial_Data (For Pandas).txt", sep="~")
    
    print("Starting Additional Analysis...")
    print("Company with the highest PE Ratio:")                                             #Finding the highest PE Ratio company
    print("Company with the highest PE Ratio:", file=add_output)
    peColumnH = AAdata[["ticker","company","pe","ytd_gains"]]
    tickerHigh = peColumnH.nlargest(1, "pe")
    print(tabulate(tickerHigh, headers="keys", tablefmt="psql"))
    print(tabulate(tickerHigh, headers="keys", tablefmt="psql"), file=add_output)
    
    print("\nCompany with the lowest PE Ratio:")                                             #Finding the lowest PE Ratio company
    print("\nCompany with the lowest PE Ratio:", file=add_output)
    peColumnL = AAdata[["ticker","company","pe","ytd_gains"]]
    tickerLOW = peColumnL.nsmallest(1, "pe")
    print(tabulate(tickerLOW, headers="keys", tablefmt="psql"))
    print(tabulate(tickerLOW, headers="keys", tablefmt="psql"), file=add_output)
    
    print("Additional Analysis is complete!")
    
    
'''
PLOTTING FUNCTIONS
'''

plt_data=pd.read_csv("txt_Financial_Data (For Pandas).txt", sep="~")        #Creates connection

#Starting MKT_CAP Plot
def mkt_plot():
    plt.ion()                                                               #Makes plt.show() a non-stopping function
    Xmkt_cap=plt_data[["mkt_cap"]].to_numpy()                               #Creates Axes
    Ymkt_cap=plt_data[["ytd_gains"]].to_numpy()
    
    model_mkt_cap = linear_model.LinearRegression()                         #Creates models
    model_mkt_cap.fit(Xmkt_cap, Ymkt_cap)
    
    Ymkt_cap_predict = model_mkt_cap.predict(Xmkt_cap)                      #Creates Y predictor
    
    plt.scatter(Xmkt_cap, Ymkt_cap, color="black")                          #Creates scatter plot
    plt.plot(Xmkt_cap,Ymkt_cap_predict, color="blue", linewidth=2)
    
    plt.ylabel("YTD_Gains")                                                 #Builds scatter plot
    plt.xlabel("MKT_CAP")
    plt.show()                                                              #Opens, saves, and closes scatter plot
    plt.savefig("mkt_cap.png", bbox_inches="tight")
    plt.close()

#Starting price Plot
def price_plot():
    plt.ion()
    Xprice=plt_data[["price"]].to_numpy() 
    Yprice=plt_data[["ytd_gains"]].to_numpy()
    
    model_price = linear_model.LinearRegression() 
    model_price.fit(Xprice, Yprice)
    
    Yprice_predict = model_price.predict(Xprice)
    
    plt.scatter(Xprice, Yprice, color="black")
    plt.plot(Xprice,Yprice_predict, color="blue", linewidth=2)
    
    plt.ylabel("YTD_Gains")
    plt.xlabel("PRICE")
    plt.show()
    plt.savefig("price.png", bbox_inches="tight")
    plt.close()

#Starting pe Plot
def pe_plot():
    plt.ion()
    Xpe=plt_data[["pe"]].to_numpy() 
    Ype=plt_data[["ytd_gains"]].to_numpy()
    
    model_pe = linear_model.LinearRegression() 
    model_pe.fit(Xpe, Ype)
    
    Ype_predict = model_pe.predict(Xpe)
    
    plt.scatter(Xpe, Ype, color="black")
    plt.plot(Xpe,Ype_predict, color="blue", linewidth=2)
    
    plt.ylabel("YTD_Gains")
    plt.xlabel("PE_Ratio")
    plt.show()
    plt.savefig("pe.png", bbox_inches="tight")
    plt.close()   

#Starting eps Plot
def eps_plot():
    plt.ion()
    Xeps=plt_data[["eps"]].to_numpy() 
    Yeps=plt_data[["ytd_gains"]].to_numpy()
    
    model_eps = linear_model.LinearRegression() 
    model_eps.fit(Xeps, Yeps)
    
    Yeps_predict = model_eps.predict(Xeps)
    
    plt.scatter(Xeps, Yeps, color="black")
    plt.plot(Xeps,Yeps_predict, color="blue", linewidth=2)
    
    plt.ylabel("YTD_Gains")
    plt.xlabel("EPS_Ratio")
    plt.show()
    plt.savefig("eps.png", bbox_inches="tight")
    plt.close() 

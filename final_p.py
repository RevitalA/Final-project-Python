# libraries importing
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import requests
from googletrans import Translator
# הוספתי
from webdriver_manager.chrome import ChromeDriverManager

# functions
def MainCrawller(df, browser, writer):
    # This function will help us retrieve the information we need from each member's page
    flag=True
    while flag:
        mp_l=browser.find_elements(By.XPATH,'//div[@class="ms-srch-item-body"]')
        for i in range(0,len(mp_l)):
            time.sleep(5)
            mp_clicks=browser.find_elements(By.CLASS_NAME,"ms-srch-item-link")
            member_l=[]
            browser.execute_script("arguments[0].scrollIntoView(true);",mp_clicks[i])            
            time.sleep(2)
            mp_clicks[i].click()
            time.sleep(2)
            MainInfoRetrieve(browser, member_l)
            CvInfoRetrieve(browser, member_l)
            ImageRetrieve(browser, member_l)
            GenderAPI(browser, member_l)
            ParliamentMembership(browser, member_l)
            df.loc[len(df)]=member_l
            browser.back()
            time.sleep(5)
        df.to_excel(writer, sheet_name='Sheet1', index=False, header=True)
        print(df)
        try:
            next_p=browser.find_element(By.XPATH,'//*[@id="PageLinkNext"]')
            browser.execute_script("arguments[0].scrollIntoView(true);",next_p)
            next_p.click() 
        except:
            flag=False

def MainInfoRetrieve(browser, member_l):
    # This function will help us retrieve the main and easy-to-reach information from each member's page
    member_l.append((browser.find_element(By.XPATH,'//h1[@class="mopName"]').text))
    member_l.append("Finland")
    member_l.append(browser.current_url)
    try:
        member_l.append((browser.find_element(By.XPATH,'//*[@id="ctl00_PlaceHolderMain_MOPInformation_ContactInformationPanel"]/div[1]/div[2]').text))
    except NoSuchElementException:
        member_l.append("Not Available")
    try:
        member_l.append((browser.find_element(By.XPATH,'//*[@id="ctl00_PlaceHolderMain_MOPInformation_EmailPanel"]/div/div[2]').text))
    except NoSuchElementException:
        member_l.append("Not Available")
    try:
        member_l.append((browser.find_element(By.XPATH, '//*[@id="ctl00_PlaceHolderMain_MOPInformation_HomePagePanel"]/div/div[2]/a')))
    except NoSuchElementException:
        member_l.append("Not Available")

def CvInfoRetrieve(browser, member_l):
    # This function will help us retrieve the information from the CV tab
    cv_word_counter=0
    try:
        accop=browser.find_element(By.XPATH,'//*[@id="ctl00_PlaceHolderMain_MOPInformation_CurrentParliamentaryInformationPanel"]/div/div[2]').text
        member_l.append(accop)
        EnglishAPI(member_l, accop) 
        # The next part counts the words to check how many words were chose to describe the MP's CV
        word_split=accop.split()
        cv_word_counter+=len(word_split)
    except NoSuchElementException:
          member_l.append("Not Available")
          #member_l.append("Not Available")
    cv_info=browser.find_element(By.XPATH,'//*[@id="headingThree"]/button')
    browser.execute_script("arguments[0].scrollIntoView(true);",cv_info)
    cv_info.click()
    time.sleep(2)
    browser.execute_script("arguments[0].scrollIntoView(true);",browser.find_element(By.XPATH,'//*[@id="ctl00_PlaceHolderMain_MOPInformation_CvPanel"]'))
    try:
        cv_i=browser.find_element(By.XPATH,'//*[@id="ctl00_PlaceHolderMain_MOPInformation_CvPanel"]/ul/li[2]/div/div[2]/ul/li').text
        member_l.append(cv_i)
        EnglishAPI(member_l, cv_i)
        # The next part counts the words to check how many words were chose to describe the MP's CV
        word_split=cv_i.split()
        cv_word_counter+=len(word_split)
    except NoSuchElementException:
        member_l.append("Not Available")
        member_l.append("Not Available")            
    try:
        cv_i=browser.find_element(By.XPATH,'//*[@id="ctl00_PlaceHolderMain_MOPInformation_CvPanel"]/ul/li[3]/div/div[2]/ul/li').text
        member_l.append(cv_i)
        EnglishAPI(member_l, cv_i)  
        # The next part counts the words to check how many words were chose to describe the MP's CV
        word_split=cv_i.split()
        cv_word_counter+=len(word_split)        
    except NoSuchElementException:
        member_l.append("Not Available")
        member_l.append("Not Available")
    try:
        cv_i=browser.find_element(By.XPATH,'//*[@id="ctl00_PlaceHolderMain_MOPInformation_LiCareer"]/div/div[2]/ul').text
        cv_il=cv_i.split("\n")
        cv_i="; ".join(cv_il)
        member_l.append(cv_i)
        EnglishAPI(member_l, cv_i)  
        # The next part counts the words to check how many words were chose to describe the MP's CV
        word_split=cv_i.split()
        cv_word_counter+=len(word_split)  
    except NoSuchElementException:
        member_l.append("Not Available")
        member_l.append("Not Available")
    try:
        cv_i=browser.find_element(By.XPATH,'//*[@id="ctl00_PlaceHolderMain_MOPInformation_LiCouncilPositionOfResponsibility"]/div/div[2]/ul').text
        cv_il=cv_i.split("\n")
        cv_i="; ".join(cv_il)
        member_l.append(cv_i)
        EnglishAPI(member_l, cv_i)   
        # The next part counts the words to check how many words were chose to describe the MP's CV
        word_split=cv_i.split()
        cv_word_counter+=len(word_split)          
    except NoSuchElementException:
        member_l.append("Not Available")
        member_l.append("Not Available")
    cv_info.click()
    member_l.append(cv_word_counter)

def EnglishAPI(member_l, text):
    # This function will help us translate the Finnish info columns to English
    for i in range(0,50):
        try:
            is_ok=True
            translator = Translator(timeout=10)
            trans= translator.translate(text).text
            member_l.append(trans)
            break
        except:
            is_ok=False 
    if is_ok==False:
        translator = Translator()
        time.sleep(10)
        trans= translator.translate(text).text
        member_l.append(trans)

def ImageRetrieve(browser, member_l):
    # This function will hepl us retrieve the member's photo
    try:
        img=browser.find_element(By.XPATH,'//*[@id="ctl00_PlaceHolderMain_MOPInformation_MemberOfParliamentPicture__ControlWrapper_RichImageField"]/div/img')
        src = img.get_attribute('src')
        member_l.append(src)
    except NoSuchElementException:
        member_l.append("Not Available")

def GenderAPI(browser, member_l):
    # This function will help us determine the gender of the member
    name=browser.find_element(By.XPATH,'//h1[@class="mopName"]').text
    n_l=name.split()
    key="31da05f7b7724eca68b454d420139f8b"
    query_params={"name":n_l[0],"apikey":key}
    response= requests.get("https://api.genderize.io/",params=query_params)    
    json_dict=response.json()
    gender=json_dict["gender"]
    prob=json_dict["probability"]
    member_l.append(gender)
    member_l.append(prob)

def ParliamentMembership(browser, member_l):
    # This function will help us retrieve the information aout the member's Parliamentary's history
    active_mp=browser.find_element(By.XPATH,'//*[@id="ctl00_PlaceHolderMain_MOPInformation_MOPWrapper"]/p[2]').text
    years_l=active_mp.split()
    years=" ".join(years_l[1:])
    member_l.append(years)

# main code

# process of getting to the right page's retrieve start
#ביצעתי מנהל דרייב
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.maximize_window()
try:
    browser.get("https://www.eduskunta.fi/FI/search/Sivut/peopleresults.aspx?k=")
    time.sleep(5)
    mp_l=browser.find_elements(By.XPATH,'//div[@class="ms-srch-item-body"]')
except:
    print("Sometimes I'm having trouble opening the page. Please try again")

# opening new excel doc to enter the retrieved information in
save_path="C:\\Users\\revit\\OneDrive - Bar-Ilan University\\second year\\Semester A\\Advanced Py\\NoaRevital_Final_Proj\\"
headers=["Koko nimi- full name","maa-country","personal browser link","Puhelin-phone","Sähköposti-email",
         "Kotisivu-homepage","Ammatti-fin","Occupation-eng","Syntymävuosi ja paikka-fin",
         "Year and place of birth-eng","Koulutus-fin","education-eng","Työura- ja elämäkertatietoja-fin",
         "Career and biographical information-eng","Kunnalliset luottamustehtävät-fin",
         "Municipal positions of trust-eng","cv words count","kuva-image","gender",
         "gender prob","years as MP"]
df=pd.DataFrame(columns=headers)

# the starting of the information retrieve process
with pd.ExcelWriter(save_path+'parliament.xlsx') as writer:
    MainCrawller(df, browser, writer)
    df.to_excel(writer, sheet_name='Sheet1', index=False, header=True)
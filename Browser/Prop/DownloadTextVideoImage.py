# Import dependencies
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
from pprint import pprint
import pandas as pd 
from selenium import webdriver
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import time

class GoogleSpider(object):

      def __init__(self):
          """Crawl Google search results

          This class is used to crawl Google's search results using requests and BeautifulSoup.
          """
          super().__init__()
          self.headers = {
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
              'Host': 'www.google.com',
              'Referer': 'https://www.google.com/'
          }

      def __get_source(self, url: str) -> requests.Response:
          """Get the web page's source code

          Args:
              url (str): The URL to crawl

          Returns:
              requests.Response: The response from URL
          """
          return requests.get(url, headers=self.headers)



      def videoDataSecondTime(self, query: str) -> list:
        title=[]
        query.replace(" ", "+")
        print(query)
        search_url = "https://www.google.com/search?q="+query+"&source=lmns&tbm=vid&bih=657&biw=1366&rlz=1C1GCEU_enPK967PK967&hl=en&sa=X&ved=2ahUKEwiVyqHZj5DzAhXT4YUKHam7AlwQ_AUoAnoECAEQAg"
        request_result=requests.get(search_url)
        soup = BeautifulSoup(request_result.text, 'lxml')
        result_containers = soup.findAll('BNeawe s3v9rd AP7Wnd')
        divs = soup.find_all('div', class_=['BNeawe s3v9rd AP7Wnd'])

        onlyOdd=1
        for text in divs:
          if(onlyOdd%2==0):
            onlyOdd+=1
            continue
          print(text.get_text())
          title.append(text.get_text())
          onlyOdd+=1
          print("\n")
        success={'title':title}
        return success


      def imageDataSecondTime(self, query: str) -> list:
        query.replace(" ", "+")
        search_url = "https://www.google.com/search?q="+query+"&rlz=1C1GCEU_enPK967PK967&sxsrf=AOaemvItjgnpCmY0s-Q7Hx6AljmcM2X35Q:1632229222571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiS6ILYj5DzAhUHtRoKHTZkDCAQ_AUoAXoECAEQAw&biw=1366&bih=657&dpr=1"
        title=[]
        html = requests.get(search_url)
        soup = BeautifulSoup(html.text, 'lxml')
        print('\nGoogle Images Metadata:')
            #print(soup)
            
        id=1
        alldata=soup.find_all(class_='qXLe6d x3G5ab')
        print("AllData ",alldata)
        for text in alldata:
          print(text.get_text())
          if id==11:
            break
          id+=1
          title.append(text.get_text())
        #success={'title':title}
        return title




      def search(self, query: str) -> list:

          response = self.__get_source('https://www.google.com/search?q=%s' % quote(query))
          # Initialize BeautifulSoup
          soup = BeautifulSoup(response.text, 'html.parser')
          # Get the result containers
          #print(soup)
          result_containers = soup.findAll('div', class_='g')
          #print(result_containers)
          # Final results list
          #results = []
          #df_text = pd.DataFrame(columns = ['url', 'title', 'des']) 
          url=[]
          title=[]
          des=[]
          # Loop through every container
          i=0
          for container in result_containers:
              # Result title
              title_text=" "
              des_text=" "
              url_text=" "
              try:
                title_text = container.find('h3').text
              except:
                print(" ")
              #print(title)
              # Result URL
              try:
                url_text = container.find('a')['href']
              except:
                print(" ")
              #print(url)
              # Result description
              try:
                des_text = container.find("div", attrs={"class" :"IsZvec"}).text
              except:
                print(" ")
              try:
                url.append(url_text)
                title.append(title_text)
                des.append(des_text)
#                df_text.at[i, 'url'] = url
 #               df_text.at[i, 'title'] = title
  #              df_text.at[i, 'des'] = des
              except:
                print(" ")
              i+=1
              #print(des)
  #           results.append({
  #               'title': title,
    #              'url': url,
    #             'des': des
      #        })
          success={'url':url,'title':title,'des':des}
          return success

      # this function data access from complete class
      def searchOnlyTenText(self, query: str) -> list:

          response = self.__get_source('https://www.google.com/search?q=%s' % quote(query))
          # Initialize BeautifulSoup
          soup = BeautifulSoup(response.text, 'html.parser')
          # Get the result containers
          #print(soup)
          result_containers = soup.findAll('div', class_='g')
          url=[]
          title=[]
          des=[]
          ful_des=[]
          # Loop through every container
          i=0
          
          for container in result_containers:
              # Result title
              title_text=" "
              des_text=" "
              url_text=" "
              try:
                title_text = container.find('h3').text
              except:
                print(" ")
              #print(title)
              # Result URL
              try:
                url_text = container.find('a')['href']
              except:
                print(" ")
              #print(url)
              # Result description
              try:
                des_text = container.find("div", attrs={"class" :"IsZvec"}).text
              except:
                print(" ")
              try:
                reqs2 = requests.get(url_text)
                soup2 = BeautifulSoup(reqs2.text, 'lxml')
                print("List of all the h1, h2, h3 :")
                deslarge_text=" "
                for heading in soup2.find_all(["h1", "h2", "h3","p","title"]):
                  #print(heading.name + ' ' + heading.text.strip())
                  
                  deslarge_text+=heading.text.strip()

                url.append(url_text)
                title.append(title_text)
                des.append(des_text)
                ful_des.append(deslarge_text)
#                df_text.at[i, 'url'] = url
 #               df_text.at[i, 'title'] = title
  #              df_text.at[i, 'des'] = des
              except Exception as a:
                print(" Error ",a)
 
              i+=1
              if(i==11):
                break
              #print(des)
  #           results.append({
  #               'title': title,
    #              'url': url,
    #             'des': des
      #        })
          success={'url':url,'title':title,'des':des,'ful_des':ful_des}
          return success


      def imagesData(self,query):   
        driver_img = webdriver.Chrome('chromedriver',options =chrome_options)
        query.replace(" ", "+")

        search_url = "https://www.google.com/search?q="+query+"&rlz=1C1GCEU_enPK967PK967&sxsrf=AOaemvItjgnpCmY0s-Q7Hx6AljmcM2X35Q:1632229222571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiS6ILYj5DzAhUHtRoKHTZkDCAQ_AUoAXoECAEQAw&biw=1366&bih=657&dpr=1"
        driver_img.get(search_url)

        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

      
        params = {
            "q": query,
            "tbm": "isch",
            "ijn": "0",
        }
        title=[]
        domain=[]
        url=[]
        images=[]
        html = requests.get("https://www.google.com/search", params=params, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        time.sleep(5)
        print('\nGoogle Images Metadata:')
        id=1
        for google_image in soup.select('.isv-r.PNCib.MSM1fd.BUooTd'):
          title_txt = google_image.select_one('.VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb')['title']
          source_txt = google_image.select_one('.fxgdke').text
          link_txt = google_image.select_one('.VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb')['href']
          

        
                #v = img.get('src', img.get('data-src'))
          title.append(title_txt)
          domain.append(source_txt)
          url.append(link_txt)
          try:
            url2=driver_img.find_element_by_xpath('//*[@id="islrg"]/div[1]/div['+str(id)+']/a[1]/div[1]/img')
            img_txt = url2.get_attribute('src')
            images.append(img_txt)
          except:
            print(" ")
          id+=1  
                #print(f'{title}\n{source}\n{link}\n{img}\n')
        print(title)
        print(domain)        
        print(url)
        print(images)
        success={'title':title,'domain':domain,'url':url,'images':images}
        return success
      


      def PresentVideo(self,query):
        driver_img = webdriver.Chrome('chromedriver',options =chrome_options)
        query2=query
        try:
          query.replace(" ", "+")
        except:
          print(" Error in replace query ")

        search_url = "https://www.google.com/search?q="+query+"&source=lmns&tbm=vid&bih=657&biw=1366&rlz=1C1GCEU_enPK967PK967&hl=en&sa=X&ved=2ahUKEwiVyqHZj5DzAhXT4YUKHam7AlwQ_AUoAnoECAEQAg"
        driver_img.get(search_url)

        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

        params = {
            "q": query2,
            "tbm": "vid",
            "hl": "en" # get english results
        }

        response = requests.get("https://www.google.com/search", headers=headers, params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        print("response", response)
        print("soup", soup)


        title=[]
        desc=[]
        url=[]
        sourc_url=[]
        images=[]
        uploadedDate_By=[]
        
        
        id=1
        time.sleep(5)
        for results in soup.select('.tF2Cxc'):
            title_txt = results.select_one('.DKV0Md').text
            link = results.a['href']
            displayed_link = results.select_one('.TbwUpd.NJjxre').text
            snippet = results.select_one('.aCOpRe span').text
            uploadDandB=""
            uploadDandB=results.select_one('.fG8Fp.uo4vr').text.split(' · ')[0]
            uploadDandB+=" - "
            uploadDandB+= results.select_one('.uo4vr span').text.split(' ')[2]
            
            title.append(title_txt) # all title
            url.append(link)        # click to play
            sourc_url.append(displayed_link) # domain url 
            desc.append(snippet)             #description
            
            uploadedDate_By.append(uploadDandB) #uploaded data and who
            
            img_txt=""
            try:
              url2=driver_img.find_element_by_xpath('//*[@id="vidthumb'+str(id)+'"]')
              img_txt = url2.get_attribute('src')
              #print(img_txt)
              id+=1
            except Exception as a:
              print(a)
              print("error here")
           
            images.append(img_txt)   #all thumbnails url 
            print(f'{title}\n{link}\n{displayed_link}\n{snippet}\n{upload_date}\n{uploaded_by}\n{img_txt}\n')
        success={'title':title,'url':url,'sourc_url':sourc_url,'desc':desc,'uploadedDate_By':uploadedDate_By,'images':images}
        return success

import  re
import os
import  json
import pandas as pd
import  requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from  tqdm import tqdm
def net_txt_transformer(core_url):

    response = requests.get(core_url)
    soup = BeautifulSoup(response.text,"lxml")
    p_text=soup.find_all("p")
    for num ,p in enumerate(p_text):
        content=pd.DataFrame(json.loads(p.getText())["content"])
        organism=[i for i in content["organism"]]
        sample=[i for i in content["sample"]]
        fname=["http://www.bdbe.cn/kun/api/h5ad?name="+i for i in content["fname"]]
        return  organism,sample,fname

class Download():
    def __init__(self,core_url):
        self.organism,self.sample,self.url_list=net_txt_transformer(core_url)

    def download(self):
        for  organism,sample,url in tqdm(zip(self.organism,self.sample,self.url_list),total=len(self.url_list), desc="Processing", unit="item", ncols=100):

            if organism=="Homo sapiens":
                try:
                    urlretrieve(url,filename=os.path.join("E:\SCAD",sample+".h5ad"))
                    print("完成")
                except Exception as e:
                    print(f"错误出现了:{e},文件{sample}没有爬下来")
                    with open(os.path.join("E:\SCAD","erro"+".txt"),"wb") as f:
                        f.write(str(e))
                        break
if __name__ == '__main__':
     do=Download(core_url="http://www.bdbe.cn/kun/api/homo?Organism=&Organ=&Class=&Time=&Gender=&Cell_line=&Organoid=&Tumor=&pageNum=1&pagesize=15337")
     do.download()

import requests
import pandas as pd
from lxml import html

# Request the page
def scrape_news(tag:str='stunting', max_page:int=100):

    def convert_todf(nama_berita:str, tgl:list, judul:list, image:list, link:list):
        tgl_norm=[]
        for t in tgl:
            t = ' '.join(t.split(',')[1].split()[:-1])
            t = t.replace('Mei', 'May').replace('Agu', 'Aug').replace('Okt', 'Oct').replace('Des','Dec')
            tgl_norm.append(t)
        df_news = pd.DataFrame({
                  'nama': nama_berita,
                  'tgl': tgl_norm, 
                  'judul': judul,
                  'image': image,
                  'link': link
                  })
        return df_news

    #  inisiasi dataframe
    df_all_news=pd.DataFrame()

    # berita detik
    for page in range(max_page):
        page = page+1
        try:
            base_url = 'https://www.detik.com/'
            url = requests.get(base_url+'/tag/'+tag+'?sortby=time&page='+str(page))
            tree = html.fromstring(url.content)  

            # Get element using XPath
            tgl = tree.xpath('/html/body/div[2]/div/div[1]/div[1]/article[*]/a/span[2]/span/text()')
            judul = tree.xpath('/html/body/div[2]/div/div[1]/div[1]/article[*]/a/span[2]/h2/text()')
            image_els = tree.xpath('/html/body/div[2]/div/div[1]/div[1]/article[*]/a/span[1]/span/img')
            image = [ele.attrib['src'] for ele in image_els]
            link_els = tree.xpath('/html/body/div[2]/div/div[1]/div[1]/article[*]/a')
            link = [ele.attrib['href'] for ele in link_els]

            # convert to dataframe
            df_all_news = pd.concat([df_all_news, convert_todf('detik.com', tgl, judul, image, link)]).reset_index(drop=True)
        except: break

    # berita kompas
    for page in range(max_page):
        page = page+1
        try:
            base_url = 'https://www.kompas.com/'
            url = requests.get(base_url+'/tag/'+tag+'?sortby=time&page='+str(page))
            tree = html.fromstring(url.content)  

            # Get element using XPath
            tgl = tree.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/div[*]/div[3]/div[2]/text()')
            judul = tree.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/div[*]/div[2]/h3/a/text()')
            image_els = tree.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/div[*]/div[1]/div/a/img')
            image = [ele.attrib['src'] for ele in image_els]
            link_els = tree.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/div[*]/div[2]/h3/a')
            link = [ele.attrib['href'] for ele in link_els]

            # convert to dataframe
            df_all_news = pd.concat([df_all_news, convert_todf('kompas.com', tgl, judul, image, link)]).reset_index(drop=True)
        except: break 

    df_all_news['tgl'] = pd.to_datetime(df_all_news['tgl'])
    return df_all_news.sort_values(by='tgl',ascending=False).reset_index(drop=True)


def save_news(df:pd.DataFrame):
    df.to_csv('stunting_data/news_stunting.csv', sep=';', encoding='utf-8', index=False)

    
def get_news(nrows:int=100):
    return pd.read_csv(
            'stunting_data/news_stunting.csv', 
            delimiter=';', 
            nrows=nrows)\
                .to_dict(orient="records")
    

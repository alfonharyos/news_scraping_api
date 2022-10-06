import requests
import pandas as pd
from lxml import html
from dateutil import parser
from datetime import date, timedelta

# Request the page
def scrape_news(max_page:int=100, tag:str='stunting'):

    bulan_dict={
                'januari':'jan',
                'februari':'feb',
                'maret':'mar',
                'april':'apr',
                'mei':'may',
                'juni':'jun',
                'juli':'jul',
                'agustus':'aug',
                'oktober':'oct',
                'desember':'dec'
                }

    def convert_todf(nama_berita:str, tgl_norm:list, judul:list, image:list, link:list):
        return pd.DataFrame({
                  'nama': nama_berita,
                  'tgl': tgl_norm, 
                  'judul': judul,
                  'image': image,
                  'link': link
                  })

    #  inisiasi dataframe
    df_all_news=pd.DataFrame()

    # detik
    for page in range(max_page):
        page = page+1
        try:
            base_url = 'https://www.detik.com'
            url = requests.get(base_url+'/tag/'+tag+'?sortby=time&page='+str(page))
            tree = html.fromstring(url.content)  

            # Get element using XPath
            tgl = tree.xpath('/html/body/div[2]/div/div[1]/div[1]/article[*]/a/span[2]/span/text()')
            judul = tree.xpath('/html/body/div[2]/div/div[1]/div[1]/article[*]/a/span[2]/h2/text()')
            image = tree.xpath('/html/body/div[2]/div/div[1]/div[1]/article[*]/a/span[1]/span/img')
            image = [ele.attrib['src'] for ele in image]
            link = tree.xpath('/html/body/div[2]/div/div[1]/div[1]/article[*]/a')
            link = [ele.attrib['href'] for ele in link]

            # normalisasi tanggal --> tahun-bulan-hari
            tgl_norm=[]
            for t in tgl:
                t = ' '.join(t.split(',')[1].split()[:3])\
                    .replace('Mei', 'May')\
                    .replace('Agu', 'Aug')\
                    .replace('Okt', 'Oct')\
                    .replace('Des','Dec')
                t = parser.parse(t).strftime('%Y-%m-%d')  # mengubah ke format tahun-bulan-hari
                tgl_norm.append(t)

            # convert to dataframe
            df_all_news = pd.concat([df_all_news, convert_todf('detik.com', tgl_norm, judul, image, link)]).reset_index(drop=True)
        except: pass

    # kompas
    for page in range(max_page):
        page = page+1
        try:
            base_url = 'https://www.kompas.com'
            url = requests.get(base_url+'/tag/'+tag+'?sortby=time&page='+str(page))
            tree = html.fromstring(url.content)  

            # Get element using XPath
            tgl = tree.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/div[*]/div[3]/div[2]/text()')
            judul = tree.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/div[*]/div[2]/h3/a/text()')
            image = tree.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/div[*]/div[1]/div/a/img')
            image = [ele.attrib['src'] for ele in image]
            link = tree.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[4]/div[*]/div[2]/h3/a')
            link = [ele.attrib['href'] for ele in link]
            
            # normalisasi tanggal --> tahun-bulan-hari
            tgl_norm=[]
            for t in tgl:
                t = '-'.join(t.split(',')[0].split('/')[::-1])  # mengubah ke format tahun-bulan-hari
                tgl_norm.append(t)

            # convert to dataframe
            df_all_news = pd.concat([df_all_news, convert_todf('kompas.com', tgl_norm, judul, image, link)]).reset_index(drop=True)
        except: pass

    # tribun
    for page in range(max_page):
        page = page+1
        try:
            base_url = 'https://www.tribunnews.com'
            url = requests.get(base_url+'/tag/'+tag+'?sortby=time&page='+str(page))
            tree = html.fromstring(url.content)  

            # Get element using XPath
            tgl = tree.xpath('//*[@id="bodyart"]/div[5]/div[4]/div[1]/div/div[2]/div[4]/ul/li[*]/div[2]/div/time/text()')
            judul = tree.xpath('//*[@id="bodyart"]/div[5]/div[4]/div[1]/div/div[2]/div[4]/ul/li[*]/div[2]/h3/a')
            judul = [ele.attrib['title'] for ele in judul]
            image = tree.xpath('//*[@id="bodyart"]/div[5]/div[4]/div[1]/div/div[2]/div[4]/ul/li[*]/div[1]/a/img')
            image = [ele.attrib['src'] for ele in image]
            link = tree.xpath('//*[@id="bodyart"]/div[5]/div[4]/div[1]/div/div[2]/div[4]/ul/li[*]/div[2]/h3/a')
            link = [ele.attrib['href'] for ele in link]

            # normalisasi tanggal --> tahun-bulan-hari
            tgl_norm=[]
            for t in tgl:
                if 'hari' in t:
                    t = (date.today() - timedelta(days=int(t.split()[0]))).strftime('%Y-%m-%d')
                elif ('detik' in t) or ('menit' in t) or ('jam' in t):
                    t = date.today().strftime('%Y-%m-%d')
                else:
                    t = t.split(',')[1].lower()  # ambil hari, bulan, tahun
                    t = " ".join(bulan_dict.get(ele, ele) for ele in t.split())  # merubah bulan ke b.ing
                    t = parser.parse(t).strftime('%Y-%m-%d')  # mengubah ke format tahun-bulan-hari
                tgl_norm.append(t)
            
            # convert to dataframe
            df_all_news = pd.concat([df_all_news, convert_todf('tribunnews.com', tgl_norm, judul, image, link)]).reset_index(drop=True)
        except: pass
    
    # tempo
    for page in range(max_page):
        page = page+1
        try:
            base_url = 'https://www.tempo.co'
            url = requests.get(base_url+'/tag/'+tag+'?type=berita?sortby=time&page='+str(page))
            tree = html.fromstring(url.content)   

            # Get element using XPath
            tgl = tree.xpath('/html/body/main/div[2]/main/div[2]/div[*]/article/h4/text()')
            judul = tree.xpath('/html/body/main/div[2]/main/div[2]/div[*]/article/h2/a/text()')
            image = tree.xpath('/html/body/main/div[2]/main/div[2]/div[*]/figure/a/img')
            image = [ele.attrib['src'] for ele in image]
            link = tree.xpath('/html/body/main/div[2]/main/div[2]/div[*]/figure/a')
            link = [ele.attrib['href'] for ele in link]

            # normalisasi tanggal --> tahun-bulan-hari
            tgl_norm=[]
            for t in tgl:
                t = t.lower().split()[:3]  # ambil hari, bulan, tahun
                t = " ".join(bulan_dict.get(ele, ele) for ele in t)  # merubah bulan ke b.ing
                t = parser.parse(t).strftime('%Y-%m-%d')  # mengubah ke format tahun-bulan-hari
                tgl_norm.append(t)
            
            # convert to dataframe
            df_all_news = pd.concat([df_all_news, convert_todf('tempo.co', tgl_norm, judul, image, link)]).reset_index(drop=True)
        except: pass

    # idntimes
    for page in range(max_page):
        page = page+1
        try:
            base_url = 'https://www.idntimes.com'
            url = requests.get(base_url+'/tag/'+tag+'?sortby=time&page='+str(page))
            tree = html.fromstring(url.content)  

            # Get element using XPath
            tgl = tree.xpath('/html/body/div[4]/div/div[2]/div[1]/section/div/div/div/time/text()')
            judul = tree.xpath('/html/body/div[4]/div/div[2]/div[1]/section/div/div/div/a/h3/text()')
            image = tree.xpath('/html/body/div[4]/div/div[2]/div[1]/section/div/div/a/div/img')
            image = [ele.attrib['data-src'] for ele in image]
            link = tree.xpath('/html/body/div[4]/div/div[2]/div[1]/section/div/div/div/a')
            link = [ele.attrib['href'] for ele in link]

            # normalisasi tanggal --> tahun-bulan-hari
            tgl_norm=[]
            for t in tgl:
                t = t.replace('\n','').strip().lower().split()      # ambil hari, bulan, tahun
                t = " ".join(bulan_dict.get(ele, ele) for ele in t) # merubah bulan ke b.ing
                t = parser.parse(t).strftime('%Y-%m-%d')            # mengubah ke format tahun-bulan-hari
                tgl_norm.append(t)
            tgl_norm
            
            # convert to dataframe
            df_all_news = pd.concat([df_all_news, convert_todf('idntimes.com', tgl_norm, judul, image, link)]).reset_index(drop=True)
        except: pass 

    # sindonews
    for page in range(max_page):
        page = page+1
        page = '' if page==1 else page*10
        try:
            base_url = 'https://search.sindonews.com'
            url = requests.get(base_url+'/go/'+str(page)+'?type=artikel&q='+tag)
            tree = html.fromstring(url.content)  

            # Get element using XPath
            tgl = tree.xpath('/html/body/section/div[2]/ul/li[*]/div[2]/div[1]/div[2]/text()')
            judul = tree.xpath('/html/body/section/div[2]/ul/li[*]/div[2]/div[2]/a/text()')
            image = tree.xpath('/html/body/section/div[2]/ul/li[*]/div[1]/a/img')
            image = [ele.attrib['data-src'] for ele in image]
            link = tree.xpath('/html/body/section/div[2]/ul/li[*]/div[2]/div[2]/a')
            link = [ele.attrib['href'] for ele in link]

            # normalisasi tanggal --> tahun-bulan-hari
            tgl_norm=[]
            for t in tgl:
                t = t.split('-')[0].lower().split()[1:]             # ambil hari, bulan, tahun
                t = " ".join(bulan_dict.get(ele, ele) for ele in t) # merubah bulan ke b.ing
                t = parser.parse(t).strftime('%Y-%m-%d')            # mengubah ke format tahun-bulan-hari
                tgl_norm.append(t)
            tgl_norm
            
            # convert to dataframe
            df_all_news = pd.concat([df_all_news, convert_todf('sindonews.com', tgl_norm, judul, image, link)]).reset_index(drop=True)
        except: pass 

    # sindonews
    for page in range(max_page):
        page = page+1
        page = '' if page==1 else page*10
        try:
            base_url = 'https://www.okezone.com'
            url = requests.get(base_url+'/tag/'+tag+str(page))
            tree = html.fromstring(url.content) 

            # Get element using XPath
            tgl = tree.xpath('/html/body/div[2]/div[11]/div/div[2]/div[*]/div/div[1]/div[2]/text()')
            judul = tree.xpath('/html/body/div[2]/div[11]/div/div[2]/div[*]/div/div[1]/div[3]/a')
            judul = [ele.attrib['title'].replace('<i>','').replace('</i>','') for ele in judul]
            image = tree.xpath('/html/body/div[2]/div[11]/div/div[2]/div[*]/div/a/div')
            image = [ele.attrib['style'].replace("background-image:url('","").replace("')","") for ele in image]
            link = tree.xpath('/html/body/div[2]/div[11]/div/div[2]/div[*]/div/div[1]/div[3]/a')
            link = [ele.attrib['href'] for ele in link]

            # normalisasi tanggal --> tahun-bulan-hari
            tgl_norm=[]
            for t in tgl:
                if ('detik' in t) or ('menit' in t) or ('jam' in t):
                    t = date.today().strftime('%Y-%m-%d')
                else:
                    t = t.split(':')[0].lower().split()[:3]              # ambil hari, bulan, tahun
                    t = " ".join(bulan_dict.get(ele, ele) for ele in t)  # merubah bulan ke b.ing
                    t = parser.parse(t).strftime('%Y-%m-%d')             # mengubah ke format tahun-bulan-hari
                    tgl_norm.append(t)
            tgl_norm

            # convert to dataframe
            df_all_news = pd.concat([df_all_news, convert_todf('okezone.com', tgl_norm, judul, image, link)]).reset_index(drop=True)
        except: pass 

    return df_all_news.sort_values(by='tgl',ascending=False).reset_index(drop=True)

def save_news(df:pd.DataFrame):
    df.to_csv('stunting_data/news_stunting.csv', sep=';', encoding='utf-8', index=False)

    
def get_news(nrows:int=100):
    return pd.read_csv(
            'stunting_data/news_stunting.csv', 
            delimiter=';', 
            nrows=nrows)\
                .to_dict(orient="records")
    

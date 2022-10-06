from flask import Flask, request
from base_news_scraper import scrape_news, save_news, get_news
from auto_scraper import update_news

app = Flask(__name__)

@app.route("/scrapeNews")
def do_scrape():
    return scrape_news(
        tag = request.args\
            .get('tag', default='stunting', type=str),
        max_page = request.args\
            .get('max_page', default=1, type=int)
        )\
            .to_dict(orient="records")
     

@app.route("/scrapeBaseNews")
def do_scrapeBase():
    try:
        save_news(df=scrape_news(
            tag = request.args\
                .get('tag', default='stunting', type=str),
            max_page = request.args\
                .get('max_page', default=100, type=int)
        ))
        s='finish'
    except:s='error'
    return s

@app.route("/updateNews")
def do_update_news():
    try:  
        update_news()
        s='ok'
    except:s='error'
    return s

@app.route("/getNews")
def do_get_news():
    return get_news(request.args\
        .get('nrows', default=100, type=int)
        )

if __name__ == '__main__':
    app.run(debug=True)

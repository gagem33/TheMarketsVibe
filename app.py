import streamlit as st
import feedparser
from textblob import TextBlob
import numpy as np

# US-focused RSS feeds (50+)
rss_feeds_us = [
    'https://fortune.com/feed/fortune-feeds/?id=3230629',
    'https://seekingalpha.com/feed.xml',
    'https://www.fool.com/a/feeds/partner/googlechromefollow?apikey=5e092c1f-c5f9-4428-9219-908a47d2e2de',
    'https://www.nasdaq.com/feed/nasdaq-original/rss.xml',
    'https://www.thestreet.com/.rss/full/',
    'http://feeds.benzinga.com/benzinga',
    'https://www.marketbeat.com/feed/',
    'https://money.com/money/feed/',
    'https://www.financialsamurai.com/feed/',
    'https://moneymorning.com/feed/',
    'https://dealbreaker.com/.rss/full/',
    'https://www.cnbc.com/id/100003114/device/rss/rss.html',
    'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
    'https://www.latimes.com/world-nation/rss2.0.xml',
    'https://rss.politico.com/playbook.xml',
    'https://www.musicbusinessworldwide.com/feed/',
    'https://affordanything.com/feed/',
    'https://studentloanhero.com/blog/feed',
    'https://feeds2.feedburner.com/budgetsaresexy',
    'https://www.getrichslowly.org/feed/',
    'https://www.goodfinancialcents.com/feed/',
    'https://feeds.feedburner.com/Frugalwoods',
    'https://www.iwillteachyoutoberich.com/feed/',
    'https://www.learntotradethemarket.com/feed',
    'https://www.makingsenseofcents.com/feed',
    'https://millennialmoney.com/feed/',
    'https://blog.mint.com/feed/',
    'https://www.moneycrashers.com/feed/',
    'https://moneysavingmom.com/feed/',
    'https://www.moneyunder30.com/feed',
    'https://mywifequitherjob.com/feed/',
    'https://obliviousinvestor.com/feed/',
    'https://www.savingadvice.com/feed/',
    'https://www.sidehustlenation.com/feed',
    'https://thecollegeinvestor.com/feed/',
    'https://www.doughroller.net/feed/',
    'https://www.thepennyhoarder.com/feed/',
    'https://wellkeptwallet.com/feed/',
    'http://feeds.killeraces.com/wisebread',
    'https://avc.com/feed/',
    'https://bothsidesofthetable.com/feed',
    'http://feeds.feedburner.com/entrepreneur/latest',
    'https://feld.com/feed',
    'https://www.forbes.com/business/feed/',
    'https://www.marketwatch.com/rss/topstories',
    'https://finance.yahoo.com/news/rssindex',
    'https://feeds.feedburner.com/reuters/businessNews',
    'https://www.investopedia.com/feedbuilder/feed/getfeed?feedName=rss_articles',
    'https://www.federalreserve.gov/feeds/press_monetary.xml',
    'https://www.stocktitan.net/rss/news',
    'https://www.mtnewswires.com/rss',
    'https://www.nyse.com/rss',
    'https://www.bloomberg.com/feeds/markets.rss',
    'https://www.cbsnews.com/rss/topics/moneywatch',
]

# World/International-focused RSS feeds (50+)
rss_feeds_world = [
    'https://www.ft.com/rss/home',
    'https://bankpediaa.com/feed/',
    'https://www.business-standard.com/rss/latest.rss',
    'https://gfmag.com/feed/',
    'https://moneyweek.com/feed/all',
    'https://www.finance-monthly.com/feed/',
    'https://www.europeanfinancialreview.com/feed/',
    'https://www.worldfinance.com/feed',
    'https://www.finews.com/news/english-news?format=feed&type=rss',
    'https://www.financeasia.com/rss/latest',
    'https://www.businessnews.com.au/rssfeed/latest.rss',
    'https://feeds.feedburner.com/com/rCTl',
    'https://www.michaelwest.com.au/feed/',
    'https://business.financialpost.com/feed/',
    'https://riotimesonline.com/feed/',
    'http://www.brasilwire.com/feed/',
    'https://e00-expansion.uecdn.es/rss/portada.xml',
    'https://www.elfinanciero.com.mx/arc/outboundfeeds/rss/?outputType=xml',
    'https://www.bworldonline.com/feed/',
    'https://businessmirror.com.ph/feed/',
    'https://www.moneyweb.co.za/feed/',
    'https://businesstech.co.za/news/feed/',
    'https://www.investing.com/rss/news.rss',
    'https://economictimes.indiatimes.com/rssfeedsdefault.cms',
    'https://fortune.com/feed',
    'http://feeds.harvardbusiness.org/har',
    'https://www.cnbc.com/id/100727362/device/rss/rss.html',
    'http://feeds.bbci.co.uk/news/world/rss.xml',
    'http://rss.cnn.com/rss/edition_world.rss',
    'http://feeds.feedburner.com/ndtvnews-world-news',
    'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    'http://feeds.washingtonpost.com/rss/world',
    'https://www.reddit.com/r/worldnews/.rss',
    'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms',
    'https://www.theguardian.com/world/rss',
    'https://www.yahoo.com/news/rss',
    'https://news.google.com/rss',
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'https://archive.nytimes.com/www.nytimes.com/services/xml/rss/index.html',
    'http://rssfeeds.usatoday.com/UsatodaycomNation-TopStories',
    'https://www.huffingtonpost.in/news/rss/',
    'https://www.abc.net.au/news/rural/rss/',
    'https://www.theage.com.au/rssheadlines',
    'https://www.heraldsun.com.au/help-rss',
    'https://www.sbs.com.au/news/feeds',
    'https://www.northernstar.com.au/feeds/rss/homepage/',
    'https://www.channel4.com/news/rss-feeds',
    'https://www.irishtimes.com/business/rss-bringing-the-latest-syndicated-news-feeds-to-a-desktop-near-you-1.412210',
    'https://www.wired.com/about/rss_feeds/',
    'https://www.theboltonnews.co.uk/rss/',
    'https://www.telegraph.co.uk/rss.xml',
    'https://thediplomat.com/tag/rss/',
    'https://asiancorrespondent.com/feed',
    'http://www.asianage.com/rss_feed/',
    'https://www.channelnewsasia.com/rssfeeds/8395986',
    'https://www.eastasiaforum.org/feed/',
    'https://www.retailnews.asia/feed/',
    'https://www.globalnews.ca/feed',
    'https://torontosun.com/feed',
    'https://www.vancouversun.com/feed/?x=1',
    'https://www.metronews.ca/feeds.articles.news.rss',
    'https://www.thepostmillennial.com/feed',
    'https://www.cbc.ca/rss/',
    'https://www.rsssearchhub.com/feeds/national-post',
    'https://meduza.io/rss/podcasts/meduza-v-kurse',
    'https://www.themoscowtimes.com/page/rss',
    'https://tass.com/search',
    'https://www.rt.com/rss-feeds/',
    'https://www.ft.com/?format=rss',
    'https://www.economist.com/finance-and-economics/rss.xml',
]

def get_color(score):
    if score <= 33:
        return 'red'
    elif score <= 66:
        return 'yellow'
    else:
        return 'green'

def tug_of_war(score):
    if score > 50:
        return '🐻 ---< 🐂'  # Bull winning
    elif score < 50:
        return '🐻 >--- 🐂'  # Bear winning
    else:
        return '🐻 --- 🐂'  # Tie

def compute_scores(feeds):
    all_texts = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                text = (entry.title + ' ' + (entry.summary or '')).strip()
                if text:
                    all_texts.append(text)
        except Exception:
            pass
    if not all_texts:
        return 0, 0, 0
    sentiments = [TextBlob(t).sentiment.polarity for t in all_texts]
    avg_polarity = np.mean(sentiments)
    std_polarity = np.std(sentiments)
    bull_score = int((avg_polarity + 1) * 50)
    vol_score = int(min(std_polarity / 0.5, 1) * 100) if std_polarity else 0
    return bull_score, vol_score, len(all_texts)

st.title('TheMarketsVibe')
st.write('Summarizes global market sentiment like a personal Bloomberg Terminal. Scores bull/bear (0-100) and volatility (0-100) for US and World.')

if st.button('Compute Scores'):
    with st.spinner('Fetching and analyzing...'):
        us_bull, us_vol, us_items = compute_scores(rss_feeds_us)
        world_bull, world_vol, world_items = compute_scores(rss_feeds_world)
        
        st.success(f'US: Analyzed {us_items} items from 50+ sources.')
        st.markdown(f"<h3 style='color:{get_color(us_bull)};'>US Bullish Score: {us_bull}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:{get_color(us_vol)};'>US Volatility Score: {us_vol}</h3>", unsafe_allow_html=True)
        st.text(tug_of_war(us_bull))
        
        st.success(f'World: Analyzed {world_items} items from 50+ sources.')
        st.markdown(f"<h3 style='color:{get_color(world_bull)};'>World Bullish Score: {world_bull}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:{get_color(world_vol)};'>World Volatility Score: {world_vol}</h3>", unsafe_allow_html=True)
        st.text(tug_of_war(world_bull))

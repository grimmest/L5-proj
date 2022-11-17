import os, requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# Get remaining video links from wikihow article links using BeautifulSoup. Write out every 100 articles
def get_remaining_video_links():
    print('Starting to get video links from articles...')
    df = pd.read_csv('wikihow_videos.csv')
    remaining = len(df)-len(df[df.accessed.notnull()])
    for i, row in df.iterrows():
        print(remaining)
        if row.accessed != np.NaN:
            try:
                page = requests.get(row.url)
                soup = BeautifulSoup(page.content, "html.parser")
                embed_video = soup.find(id='yoexutube_embed_iframe')
                if embed_video:
                    df['video'][i] = embed_video.attrs.get('data-src', None)
            except:
                print('Error accessing article at '+row.url)
            df['accessed'][i] = True
        remaining-=1
        if remaining%100 == 0:
            df.to_csv('wikihow_videos.csv', index=False)
    print('Outputted to wikihow_videos.csv')

if __name__ == '__main__':
    get_remaining_video_links()
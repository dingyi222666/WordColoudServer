import jieba
import codecs
import sys
import pandas
import numpy as np
import imageio
import base64
from io import BytesIO
from PIL import Image
from jieba import posseg
from random import choice, shuffle
from wordcloud import WordCloud, ImageColorGenerator
from os import listdir
from os.path import isfile, join

stopwords_filename = 'data/stopwords.txt'
font_filename = 'fonts/msyh.ttc'
template_dir = 'data/templates/'
background_picture_filename = template_dir + "/image3.png"


def posseg_lcut(segment):
    try:
        jieba.enable_parallel()
    except BaseException:
        pass
    keywords = posseg.lcut(segment)
    print(keywords)
    shuffle(keywords)
    result = []
    for i in keywords:
        a = i.word
        b = list(a)
        try:
            if b[0] == b[1]:
                a = b[0]
        except BaseException:
            pass
        result.append(a)

    return result


def render(segment_list):
    try:
        jieba.enable_parallel()
    except BaseException:
        pass
    content = '\n'.join([line.strip()
                         for line in segment_list
                         if len(line.strip()) > 0])
    stopwords = set([line.strip()
                     for line in codecs.open(stopwords_filename, 'r', 'utf-8')])

    segs = jieba.cut(content)
    words = []
    for seg in segs:
        word = seg.strip().lower()
        if len(word) > 1 and word not in stopwords:
            words.append(word)

    words_df = pandas.DataFrame({'word': words})
    words_stat = words_df.groupby(by=['word'])['word'].agg(np.size)
    words_stat = words_stat.to_frame()
    words_stat.columns = ['number']
    words_stat = words_stat.reset_index().sort_values(by="number", ascending=False)

    print('# of different words =', len(words_stat))

    if isfile(background_picture_filename):
        bimg = imageio.imread(background_picture_filename)
        wordcloud = WordCloud(font_path=font_filename, background_color="white",
                              mask=bimg, max_font_size=600, random_state=100,
                              contour_width=0,  # (float)mask轮廓线宽。若mask不为空且此项值大于0，就绘制出mask轮廓 (default=0)
                              contour_color='black',  # (color value) Mask轮廓颜色，默认黑色
                              )
        wordcloud = wordcloud.fit_words(
            dict(words_stat.head(100).itertuples(index=False)))

        backgroundingColors = ImageColorGenerator(bimg)
        wordcloud.recolor(color_func=backgroundingColors)

        image: Image = wordcloud.to_image()

        output_buffer = BytesIO()
        image.save(output_buffer, format='PNG')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)
        return base64_str.decode('utf-8')

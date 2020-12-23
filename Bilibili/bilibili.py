import re
import pandas
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib import font_manager


def get_html(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '错误'


def save(html):

    # 解析网页
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)

    with open('./data/B_data.txt', 'r+', encoding='UTF-8') as f:
        f.write(soup.text)

    TScore = []  # 综合评分
    name = []    # 动漫名字
    bfl = []     # 播放量
    pls = []     # 评论数
    scs = []     # 收藏数

    # ********************************************  动漫名字存储
    for tag in soup.find_all('div', class_='info'):
        # print(tag)
        bf = tag.a.string
        name.append(str(bf))
    print(name)

    # ********************************************  播放量存储
    for tag in soup.find_all('div', class_='detail'):
        # print(tag)
        bf = tag.find('span', class_='data-box').get_text()
        if '亿' in bf:
            num = float(re.search(r'\d(.\d)?', bf).group()) * 10000
            # print(num)
            bf = num
        else:
            bf = re.search(r'\d*(\.)?\d', bf).group()
        bfl.append(float(bf))
    print(bfl)
    # ********************************************  评论数存储
    for tag in soup.find_all('div', class_='detail'):
        # pl = tag.span.next_sibling.next_sibling
        pl = tag.find('span', class_='data-box').next_sibling.next_sibling.get_text()
        # *********统一单位
        if '万' not in pl:
            pl = '%.1f' % (float(pl) / 10000)
            # print(123, pl)
        else:
            pl = re.search(r'\d*(\.)?\d', pl).group()
        pls.append(float(pl))
    print(pls)
    # ********************************************  收藏数
    for tag in soup.find_all('div', class_='detail'):
        sc = tag.find('span', class_='data-box').next_sibling.next_sibling.next_sibling.next_sibling.get_text()
        sc = re.search(r'\d*(\.)?\d', sc).group()
        scs.append(float(sc))
    print(scs)
    # ********************************************  综合评分
    for tag in soup.find_all('div', class_='pts'):
        zh = tag.find('div').get_text()
        TScore.append(int(zh))
    print('综合评分', TScore)

    # 存储至excel表格中
    info = {'动漫名': name, '播放量(万)': bfl, '评论数(万)': pls, '收藏数(万)': scs, '综合评分': TScore}
    dm_file = pandas.DataFrame(info)
    dm_file.to_excel('Dongman.xlsx', sheet_name="动漫数据分析")
    # 将所有列表返回
    return name, bfl, pls, scs, TScore


def view(info):
    my_font = font_manager.FontProperties(fname='./data/STHeiti Medium.ttc')  # 设置中文字体
    dm_name = info[0]
    dm_play = info[1]
    dm_review = info[2]
    dm_favorite = info[3]
    dm_com_score = info[4]
    # print(dm_com_score)

    # 为了坐标轴上能显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 图像绘制
    # 播放量水平柱状图
    # fig, ax1 = plt.subplots()
    # ax1.barh(x, y, height=0.7, align='center', color='pink')
    # ax1.tick_params(labelsize=6)
    # plt.yticks(rotation=10, color='green')
    # plt.ylabel('番剧名')
    # plt.xlabel('播放量')

    # **********************************************************************综合评分和播放量对比
    # *******综合评分条形图
    fig, ax1 = plt.subplots()
    plt.bar(dm_name, dm_com_score, color='red')
    plt.title('综合评分和播放量数据分析', fontproperties=my_font)
    ax1.tick_params(labelsize=6)
    plt.xlabel('番剧名')
    plt.ylabel('综合评分')
    plt.xticks(rotation=90, color='green')

    # *******播放量折线图
    ax2 = ax1.twinx()  # 组合图必须加这个
    ax2.plot(dm_play, color='cyan')  # 设置线粗细，节点样式
    plt.ylabel('播放量')

    plt.plot(1, label='综合评分', color="red", linewidth=5.0)
    plt.plot(1, label='播放量', color="cyan", linewidth=1.0, linestyle="-")
    plt.legend()

    plt.savefig(r'E:1.png', dpi=1000, bbox_inches='tight')

    # plt.show()

    # **********************************************************************评论数和收藏数对比
    # ********评论数条形图
    fig, ax3 = plt.subplots()
    plt.bar(dm_name, dm_review, color='green')
    plt.title('番剧评论数和收藏数分析')
    plt.ylabel('评论数（万）')
    ax3.tick_params(labelsize=6)
    plt.xticks(rotation=90, color='green')

    # *******收藏数折线图
    ax4 = ax3.twinx()  # 组合图必须加这个
    ax4.plot(dm_favorite, color='yellow')  # 设置线粗细，节点样式
    plt.ylabel('收藏数（万）')

    plt.plot(1, label='评论数', color="green", linewidth=5.0)
    plt.plot(1, label='收藏数', color="yellow", linewidth=1.0, linestyle="-")
    plt.legend()
    plt.savefig(r'E:2.png', dpi=1000, bbox_inches='tight')

    # **********************************************************************综合评分和收藏数对比
    # *******综合评分条形图
    fig, ax5 = plt.subplots()
    plt.bar(dm_name, dm_com_score, color='red')
    plt.title('综合评分和收藏数量数据分析')
    plt.ylabel('综合评分')
    ax5.tick_params(labelsize=6)
    plt.xticks(rotation=90, color='green')

    # *******收藏折线图
    ax6 = ax5.twinx()  # 组合图必须加这个
    ax6.plot(dm_favorite, color='yellow')  # 设置线粗细，节点样式
    plt.ylabel('收藏数（万）')
    plt.plot(1, label='综合评分', color="red", linewidth=5.0)
    plt.plot(1, label='收藏数', color="yellow", linewidth=1.0, linestyle="-")
    plt.legend()

    plt.savefig(r'E:3.png', dpi=1000, bbox_inches='tight')

    # **********************************************************************播放量和评论数对比
    # *******播放量条形图
    fig, ax7 = plt.subplots()
    plt.bar(dm_name, dm_play, color='cyan')
    plt.title('播放量和评论数 数据分析')
    plt.ylabel('播放量（万）')
    ax7.tick_params(labelsize=6)
    plt.xticks(rotation=90, color='green')

    # *******评论数折线图
    ax8 = ax7.twinx()  # 组合图必须加这个
    ax8.plot(dm_review, color='green')  # 设置线粗细，节点样式
    plt.ylabel('评论数（万）')
    plt.plot(1, label='播放量', color="cyan", linewidth=5.0)
    plt.plot(1, label='评论数', color="green", linewidth=1.0, linestyle="-")
    plt.legend()
    plt.savefig(r'E:4.png', dpi=1000, bbox_inches='tight')

    plt.show()


def main():
    url = 'https://www.bilibili.com/v/popular/rank/bangumi'
    html = get_html(url)
    info = save(html)
    view(info)


if __name__ == '__main__':
    main()

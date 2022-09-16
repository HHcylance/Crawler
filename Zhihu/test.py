import requests
import json
import time
import csv
from lxml import etree
import re
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
}
def GetAnswers(id):
    i = 0
    while True:
        url = 'https://www.zhihu.com/api//v4/questions/'+ id +'/answers' \
              '?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%' \
              '2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%' \
              '2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%' \
              '2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%' \
              '2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%' \
              '2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%' \
              '2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset={0}&platform=desktop&' \
              'sort_by=default'.format(i)

        state=1
        while state:
            try:
                res = requests.get(url, headers=headers, timeout=(3, 7))
                state=0
            except:
                continue

        res.encoding = 'utf-8'
        jsonAnswer = json.loads(res.text)
        # print(jsonAnswer)
        # print('----------------------------------')
        # break
        is_end = jsonAnswer['paging']['is_end']

        for data in jsonAnswer['data']:
            try:
                l = list()
                l.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['created_time'])))      #时间
                l.append(''.join(etree.HTML(data['content']).xpath('//p//text()')))                     #文本
                l.append('0')
                l.append(data['comment_count'])                                                         #评论数
                l.append(data['voteup_count'])                                                          #点赞数
                answer_id = str(data['id'])
                l.append(answer_id)   
                name = data['author']['name']                                                                  #评论id                            
                l.append(name)                                                        #评论者name
                l.append(data['author']['headline'])                                                    #作者签名
                l.append(data['author']['gender'])                                                                #性别
                l.append(data['author']['follower_count'])                                              #粉丝数
                l.append('')      
                l.append('')
                # print(l)
                if l:
                    writer.writerow(l)

                if data['admin_closed_comment'] == False and data['can_comment']['status'] and data['comment_count'] > 0:
                    GetComments(answer_id, name)
            except:
                # print(l)
                continue


        i += 5
        print('打印到第{0}页'.format(int(i / 5)))

        if is_end:
            break

        time.sleep(1)

def GetComments(answer_id, name):
    j = 0
    while True:
        # url = 'https://www.zhihu.com/api//v4/answers/{0}/root_comments?order=normal&limit=20&offset={1}&status=open'.format(
        #     answer_id, j)
        url = 'https://www.zhihu.com//api/v4/comment_v5/answers/{0}/root_comment?order_by=score&limit=20&offset={1}&status=open'.format(answer_id, j)
        state=1
        while state:
            try:
                res = requests.get(url, headers=headers, timeout=(3, 7))
                state=0
            except:
                continue

        res.encoding = 'utf-8'
        jsonComment = json.loads(res.text)
        # print(jsonComment)
        # break
        is_end = jsonComment['paging']['is_end']

        for data in jsonComment['data']:
            # print(data)
            l = list()
            l.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['created_time'])))
            l.append(''.join(etree.HTML(data['content']).xpath('//p//text()')))
            l.append('0')
            l.append(data['child_comment_count'])
            l.append(data['like_count'])
            comment_id = str(data['id'])
            l.append(comment_id)
            c_name = data['author']['name']
            l.append(c_name)
            l.append(data['author']['headline'])
            l.append(data['author']['gender'])
            l.append('')
            l.append('')
            l.append(name)
            
            # print(l)

            if l:
                writer.writerow(l)
            # print(l)
            if data['child_comments']:
                GetChildComments(comment_id, c_name)
                # print(l)
        j = jsonComment['paging']['next']
        _next = re.compile('offset=(.*)&order_by=score&status=open')
        j = re.findall(_next,j)[0]
        if is_end:
            break

        time.sleep(1)

def GetChildComments(comment_id, c_name):
    j = 0
    while True:
        # url = 'https://www.zhihu.com/api//v4/answers/{0}/root_comments?order=normal&limit=20&offset={1}&status=open'.format(
        #     answer_id, j)
        url = 'https://www.zhihu.com//api/v4/comment_v5/comment/{0}/child_comment?order_by=ts&limit=20&offset={1}&status=open'.format(comment_id, j)
        state=1
        while state:
            try:
                res = requests.get(url, headers=headers, timeout=(3, 7))
                state=0
            except:
                continue

        res.encoding = 'utf-8'
        jsonComment = json.loads(res.text)
        # print(jsonComment)
        # break
        is_end = jsonComment['paging']['is_end']
        
        for child_comments in jsonComment['data']:
            l = list()
            l.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(child_comments['created_time'])))
            l.append(''.join(etree.HTML(child_comments['content']).xpath('//p//text()')))
            l.append('0')
            l.append(child_comments['child_comment_count'])
            l.append(child_comments['like_count'])
            l.append(str(child_comments['id']))
            l.append(child_comments['author']['name'])
            l.append(child_comments['author']['headline'])
            l.append(child_comments['author']['gender'])
            l.append('')
            l.append('')
            if child_comments['reply_comment_id'] != child_comments['reply_root_comment_id']:
                l.append(child_comments['reply_to_author']['name'])
            else:
                l.append(c_name)
            if l:
                writer.writerow(l)

        j = jsonComment['paging']['next']
        _next = re.compile('offset=(.*)&order_by=ts&status=open')
        j = re.findall(_next,j)[0]
        if is_end:
            break

        time.sleep(1)


tweeter = input()
csvfile = open(tweeter+'.csv', 'w', newline='', encoding='utf-16')
writer = csv.writer(csvfile)
title = ['转发created_at', '转发text', '转发reposts_count', '转发comments_count', '转发attitudes_count', '转发id', '转发screen_name', '转发description', '转发gender', '转发followers_count', '转发follow_count','转发source_name']
writer.writerow(title)
id  = input()
GetAnswers(id)
csvfile.close()
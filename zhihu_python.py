import urllib.request as request
import os
import re
import time

def get_page(url):
    headers = {
        'cookie': '_zap=5913d687-d7bf-478f-a014-3622e016a732; d_c0="AEAUW6BGKBGPTgE484is8g87umvAAzoTXtY=|1587540644"; _ga=GA1.2.2296263.1587540646; _xsrf=15587bd2-8cad-4497-a66c-00c79ca501c2; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1587540646,1588557264,1589163745; capsion_ticket="2|1:0|10:1589163745|14:capsion_ticket|44:Y2YzZGFhMDQ2ZjBlNGIwNjk1ZDY3MzQ4NjMwMDRhODc=|33baa190cebbfa2b0ec7a437f40fef8a9fac2ef37a526f78fb80379e5bae14c3"; _gid=GA1.2.682323623.1589163746; SESSIONID=EmYRiXcLyjF9IWiue2QSdx59Wv60gutdtd1feCPeIYL; JOID=VlwXA0jtJicUkoiYVelht_XQ-t9CqE18RfzQ_RuTTGcv2NjxJgqUnk6VjpxUFLLBNYdaIwuFMn6PzNS-ymNImXs=; osd=W1kVA0zgIyUUloWdV-lluvDS-ttPrU98QfHV_xuXQWIt2Nz8IwiUmkOQjJxQGbfDNYNXJgmFNnOKztS6x2ZKmX8=; z_c0="2|1:0|10:1589163770|4:z_c0|92:Mi4xZ2duZUFnQUFBQUFBUUJSYm9FWW9FU1lBQUFCZ0FsVk4tZ1NtWHdBUkVGU2EwVW9CYXFZbldZTXNCZ1NCTGEyX29n|f04f62eadce9259cf8af8e7ce5a5301eec149a7cf302c55c0346580ee47cd35f"; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1589168003; KLBRSID=d017ffedd50a8c265f0e648afe355952|1589168298|1589163742',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }

    req = request.Request(url, headers= headers)

    response = request.urlopen(req)
    html = response.read()
    return html

def get_address(html):
    pat = re.compile(r'u003cimg src=\\"([\w\S\.]*\.jpg)\\"')
    result = pat.findall(html)
    return result

def store_img(addr):
    img = get_page(addr)
    filename = addr.split('/')[-1]
    with open(filename, 'wb') as f:
        f.write(img)

os.chdir('/Users/wangshizhu/Desktop')
os.mkdir('知乎')
os.chdir('/Users/wangshizhu/Desktop/知乎')

for i in range(10):
    question_num = 316954079
    offset = i*5
    url = 'https://www.zhihu.com/api/v4/questions/' + str(question_num) + '/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset='+ str(offset) +'&platform=desktop&sort_by=default'

    html = get_page(url).decode('utf-8')
    img_addrs = get_address(html)

    print("current process:" + str(offset))
    for addr in img_addrs:
        print(addr.split('/')[-1])
        store_img(addr)
        
    time.sleep(0.5)

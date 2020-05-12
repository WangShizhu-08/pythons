import urllib.request as request
import urllib.parse as parse
import json

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"

while True:
    input_data = input('请输入你想翻译的内容(press q to quit)： ')
    if input_data == 'q':
        break
    
    data = {}

    data['i'] = input_data
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['salt'] = '15888157441621'
    data['sign'] = '8f04d4a1afe04f99866678a5bedd8bb7'
    data['ts'] = '1588815744162'
    data['bv'] = 'eb1be27b4ce01b14f22b6c915c2aab82'
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_CLICKBUTTION'

    data = parse.urlencode(data).encode('utf-8')

    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

    req = request.Request(url, data, headers)
    
    response = request.urlopen(req)

    html = response.read().decode('utf-8')

    result = json.loads(html)

    print("翻译结果是：", result['translateResult'][0][0]['tgt'].strip())

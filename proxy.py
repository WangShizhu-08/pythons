import urllib.request

url = 'https://www.whatismyip.com.tw/'

proxy_support = urllib.request.ProxyHandler({'http':'39.137.69.6:80'})

opener = urllib.request.build_opener(proxy_support)

response = opener.open(url)

html = response.read().decode('utf-8')

print(html)

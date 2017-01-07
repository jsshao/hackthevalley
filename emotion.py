import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'd6442c460e1e40e0958eaa6df0431e98',
}

params = urllib.urlencode({
})

def emotions(img_url):
    try:
        body = '{"url": "' + img_url + '"}'
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
     
# For testing
if __name__ == "__main__":
    print emotions('https://portalstoragewuprod.azureedge.net/face/demo/detection%206.jpg')    

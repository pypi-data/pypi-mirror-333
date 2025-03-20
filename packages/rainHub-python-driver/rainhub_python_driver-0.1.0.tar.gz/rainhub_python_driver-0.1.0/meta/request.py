# 此文件用于封装对meta的请求

import hashlib
import json
import os
import time
import requests
import base64

class MetaRequest:
    def __init__(self, path, host, headers, method, body):
        self.path = path
        self.host = host
        self.headers = headers
        self.method = method
        self.body = body

    def generate_canonicalize_resource(self):
      queries = self.path.split('?')
      canonicalizeResource = queries[0]
      if len(queries) > 1:
        query = queries[1]
        query_params = query.split('&')
        query_params = sorted(query_params)
        canonicalizeResource = '&'.join(query_params)
      return canonicalizeResource
    

    def send_request(self):
        headers = self.generate_headers()
        url = f'{self.host}{self.path}'
        if self.method == 'GET':
            response = requests.get(url, headers=headers)
        elif self.method == 'POST':
            response = requests.post(url, headers=headers, json=self.body)
        else:
            raise ValueError(f"Unsupported method: {self.method}")
        return response.json()

    def generate_headers(self):
        key = os.getenv('RAIN_USER_API_KEY')
        # key = 'JS5Zay4VwK_gdvVkTTEO_'
        secret = os.getenv('RAIN_USER_API_SECRET')
        # secret = '4SsWFCBDoBysJxOaqIl4S4-5rS0_b6DuJ9yprIp1dCV2kb9LzHb4-MtzrQ2xFrIr'

        if not key or not secret:
            raise ValueError("META_API_KEY or META_API_SECRET is not set")

        timestamp = str(int(time.time() * 1000))
        
        # headers的type
        type = self.headers.get('Content-Type', '')

        # 如果type为application/json，则对body进行md5加密
        if type == 'application/json': 
            body = json.dumps(self.body)
            body_md5 = hashlib.md5(body.encode()).hexdigest()
        else:
            body_md5 = ''
        canonicalizeHeaders = ''
        canonicalizeResource = self.generate_canonicalize_resource()
        print("canonicalizeResource: ", canonicalizeResource)

        # 生成签名
        signature_string = f"{self.method}:{type}:{body_md5}:{canonicalizeHeaders}:{canonicalizeResource}:{timestamp}"
        print("signature_string: ", signature_string)
        signature = f"{signature_string}:{secret}"
        signature = hashlib.sha256(signature.encode()).hexdigest()
        print("signature: ", signature)
        signature_header = f'{timestamp}:{key}:{signature}'
        signature_header = base64.b64encode(signature_header.encode()).decode()
        print("signature_header: ", signature_header)
        return {
            'signature-header': signature_header,
        }

def get_user_request():
    host = os.getenv('META_HOST')
    path = '/data/open/v1/user'
    request = MetaRequest(path, host, headers={}, method='GET', body={})
    headers = request.generate_headers()
    print("headers: ", headers)
    response = request.send_request()
    print("response: ", response)

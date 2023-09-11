import http.client
import json
import os
import base64

# 检测是否存在setting.json文件,moderation是内容检查，false是不检查，而true是检查（消耗1P）,moderation是调用文本安全接口对内容进行判定（暂不开放）
if not os.path.exists("settings.json"):
    print(True)
    null = {"host": "oa.api2d.net",
            "model": "gpt-3.5-turbo",
            "original_key": "null",
            "safe_mode": "False",
            "moderation": "False",
            "moderation_stop": "False",
            "stream": "False",
            "max_tokens": "0"  # 如果为0为无限制，如果为非0数值则为设置值，如果用户少于41P,则强制以一定值发送
            }
    with open("information.json", 'w', encoding='utf-8') as file:
        json.dump(null, file, ensure_ascii=False)

# 列举
model_list = ["gpt-4",
              "gpt-4-0613",
              "gpt-3.5-turbo",
              "gpt-3.5-turbo-0301",
              "gpt-3.5-turbo-16k",
              "gpt-3.5-turbo-0613",
              "gpt-3.5-turbo-16k-0613"
              ]

# 读取setting.json信息
with open("information.json", 'r', encoding='utf-8') as file:
    file_dict = json.load(file)
    host = file_dict["host"]
    model = file_dict["model"]
    original_key = file_dict["original_key"]
    safe_mode = file_dict["safe_mode"]
    moderation = False  # moderation = file_dict["moderation"]
    moderation_stop = False  # moderation_stop = file_dict["moderation_stop"]
    stream = file_dict["stream"]

# keybase解码处理（可能未来会用其他更安全的解码方式）
if original_key == "null":
    key = "null"
else:
    base64_return_key = str(base64.b64decode(original_key))
    if base64_return_key[0:2] == "fk":
        key = base64_return_key
    else:
        key = "error"  # 输出error！！！

# 编辑获得的信息来方便使用(注：修改的每一个值都需要写入information文件中，包括P值，重要的是把密钥用base64编码存起来)
host_body = '"' + host + '"'
model_body = '"' + model + '"'
auth = "'Bearer " + key + "'"

# 功能1：回复本体（思考功能）
conn = (http.
        client.HTTPSConnection(host_body))
payload = json.dumps({
   "model": model_body,
   "messages": [
      {
         "role": "user",
         "content": "讲个笑话"
      }
   ],
   "safe_mode": safe_mode,
   "moderation": moderation,
   "moderation_stop": moderation_stop,
   "stream": stream
})
headers = {
   'Authorization': auth,
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}
conn.request("POST", "/v1/chat/completions", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

# 功能2：发送信息检查分组
conn = http.client.HTTPSConnection(host_body)
payload = json.dumps({
   "model": model_body,
   "instruction": "请修改文本中的拼写错误",
   "input": "What tim is it"
})
headers = {
   'Authorization': auth,
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}
conn.request("POST", "/custom_key/search", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

# 查询P的余额
conn = http.client.HTTPSConnection("oa.api2d.net")
payload = json.dumps({
   "model": "text-davinci-edit-001",
   "instruction": "请修改文本中的拼写错误",
   "input": "What tim is it"
})
headers = {
   'Authorization': 'Bearer fk....',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}
conn.request("GET", "/dashboard/billing/credit_grants", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

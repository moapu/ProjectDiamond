# file = open('group4_payload_hash.json', 'r')
# json_data = json.load(file)
# file.close()
# # print(type(json_data))
# #
# sha256 = json_data.pop('sha256')
# print(sha256)
# #
# # print(json_data)
# #
# str_json = str(json_data)
# #
# bytes_json = bytes(str_json, 'utf-8')
# # print(bytes_json)
# # #
# # #
# key = b'team4_secret_key'
# sha256_ = hmac.new(key, bytes_json, hashlib.sha256)
# verify = sha256_.hexdigest()
#
# print('\nfrom file: ', sha256)
# print('verify: ', verify)

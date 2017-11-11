from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import datetime as dt
import iten_model.Secret as Secret
import requests

def upload_video(filepath, user_id):
    qiniu_client = Auth(Secret.QINIU_ACCESS_KEY, Secret.QINIU_SECRET_KEY)
    bucket_name = Secret.QINIU_BUCKET
    key = user_id + str(dt.datetime.now().timestamp()) + '.mp4'
    token = qiniu_client.upload_token(bucket_name, key, 3600)
    localfile = filepath
    ret, info = put_file(token, key, localfile)
    key = ret['key']
    url = Secret.QINIU_DOMAIN + key
    requests.post()


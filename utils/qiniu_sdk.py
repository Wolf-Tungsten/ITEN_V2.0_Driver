from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import datetime as dt
import iten_model.Secret as Secret
import requests
import iten_model.Config as Config
import os
from utils.log import log

def upload_video(filepath, user_id):
    qiniu_client = Auth(Secret.QINIU_ACCESS_KEY, Secret.QINIU_SECRET_KEY)
    bucket_name = Secret.QINIU_BUCKET
    key = user_id + str(dt.datetime.now().timestamp()) + '.mp4'
    token = qiniu_client.upload_token(bucket_name, key, 3600)
    localfile = filepath
    ret, info = put_file(token, key, localfile)
    key = ret['key']
    log('视频'+key+'已上传至对象存储服务器')
    video_url = Secret.QINIU_DOMAIN + key
    server_url = Config.SERVER + '/video/upload'
    requests.post(server_url, data={
        'user_id': user_id,
        'video_url': video_url,
        'key': key
    })
    log('视频' + key + '已保存至用户索引')
    dirpath, filename = os.path.split(filepath)
    os.system('rm -rf '+dirpath)
    log('视频' + key + '临时文件已删除')




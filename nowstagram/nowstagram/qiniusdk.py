# -*- coding: utf-8 -*-
from nowstagram import app
from qiniu import Auth,put_stream,put_file  #put_stream表示读取的是二进制流,put_file表示文件，put_data表示数据
import os

#需要填写你的 Access Key 和 Secret Key
access_key = app.config['QINIU_ACCESS_KEY']
secret_key = app.config['QINIU_SECRET_KEY']
domain_prefix = app.config['QINIU_DOMAIN_PREFIX']

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = app.config['QINIU_BUCKET_NAME']
save_dir = app.config['UPLOAD_DIR']

def qiniu_upload_file(source_file,save_file_name):
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, save_file_name)
    source_file.save(os.path.join(save_dir,save_file_name))
    #source_file.save('C:/Users/wangtuanfei/Desktop/newcoder/upload/' + save_file_name)
    ret, info = put_file(token,save_file_name,os.path.join(save_dir,save_file_name))

    #fileno()用来取得参数stream指定的文件流所使用的文件描述符,,,,结果不对，UnsupportedOperation: fileno。。。。
    #ret, info = put_stream(token, save_file_name, source_file.stream,"qiniu",os.fstat(source_file.stream.fileno()).st_size)

    print(info)
    if info.status_code == 200:  #将数据保存到本地，不返回None就会保存到本地
        return domain_prefix + save_file_name
    return None
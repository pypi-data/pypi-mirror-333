
# 打包上传 python setup.py sdist upload
# 打包并安装 python setup.py sdist install
# twine upload --repository-url https://test.pypi.org/legacy/ dist/* #上传到测试
# pip install --index-url https://pypi.org/simple/ kcweb   #安装测试服务上的kcweb pip3 install kcweb==4.12.4 -i https://pypi.org/simple/
# 安装 python setup.py install
#############################################
import os,sys
from setuptools import setup, find_packages,Extension
kcw={}
kcw['name']='kcw'                             #项目的名称
kcw['version']='2.6.6'							#项目版本
kcw['description']='超轻量级http框架'       #项目的简单描述
kcw['long_description']='kcw是一个由kcw抽象出来的超轻量级http框架'     #项目详细描述
kcw['license']='MIT License'                    #开源协议   mit开源
kcw['url']='https://docs.kwebapp.cn/index/index/1'
kcw['author']='百里-坤坤'  					 #名字
kcw['author_email']='kcweb@kwebapp.cn' 	     #邮件地址
kcw['maintainer']='坤坤' 						 #维护人员的名字
kcw['maintainer_email']='fk1402936534@qq.com'    #维护人员的邮件地址
confkcw={}
confkcw['name']=kcw['name']                            #项目的名称 
confkcw['version']=kcw['version']							#项目版本
confkcw['description']=kcw['description']       #项目的简单描述
confkcw['long_description']=kcw['long_description']     #项目详细描述
confkcw['license']=kcw['license']                   #开源协议   mit开源
confkcw['url']=kcw['url']
confkcw['author']=kcw['author']  					 #名字
confkcw['author_email']=kcw['author_email'] 	     #邮件地址
confkcw['maintainer']=kcw['maintainer'] 						 #维护人员的名字
confkcw['maintainer_email']=kcw['maintainer_email']    #维护人员的邮件地址
def get_file(folder='./',lists=[]):
    lis=os.listdir(folder)
    for files in lis:
        if not os.path.isfile(folder+"/"+files):
            if files=='__pycache__' or files=='.git':
                pass
            else:
                lists.append(folder+"/"+files)
                get_file(folder+"/"+files,lists)
        else:
            pass
    return lists
b=get_file("kcw",['kcw'])
setup(
    name = confkcw["name"],
    version = confkcw["version"],
    keywords = "kcw"+confkcw['version'],
    description = confkcw["description"],
    long_description = confkcw["long_description"],
    license = confkcw["license"],
    author = confkcw["author"],
    author_email = confkcw["author_email"],
    maintainer = confkcw["maintainer"],
    maintainer_email = confkcw["maintainer_email"],
    url=confkcw['url'],
    packages =  b,
    # data_files=[('Scripts', ['kcw/bin/kcw.exe'])],
    install_requires = ['gunicorn==20.0.4','watchdog==4.0.0','filetype==1.2.0','psutil==5.8.0','requests==2.31.0',], #第三方包
    package_data = {
        '': ['*.html', '*.js','*.css','*.jpg','*.png','*.gif'],
    },
    entry_points = {
        'console_scripts':[
            'kcw = kcw.kcw:cill_start'
        ]
    }
)
# ssh-py python3命令号工具上传文件到服务器


> 安装依赖

```bash
pip3 install paramiko json argparse
```

> 添加配置

```bash
python3 index.py -add
```

> 查看配置文件列表

```bash
python3 index.py -look
```
> 上传文件，然后输入要上传的服务器索引

```bash
python3 index.py -upload
```


> 配置文件参考

```python
config = {
	# 项目名
	'project':'项目名',
	# 本地地址
	'local_path':'/Users/user/workSpace/Wechat/src/dist',
	# 本地地址下 ，上传的文件和文件夹，没有就是全部
	'project_name':['assets', 'js','index.html'],
	# 服务器地址，
	'ssh_path':'/home/webapp/public',
	# ssh服务器，用户名，密码，端口
	'hostname':'129.177.192.192',
	'username':'root',
	'password':'*****',
	'port':22,
	# 绝对忽略
	'ignore':['.DS_Store','404.html','register.html']
}
```
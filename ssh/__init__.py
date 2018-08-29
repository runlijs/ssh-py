import os
import datetime
import paramiko
import re


# 检查文件
def checkFile(loacl_path,ssh_path,filename,**args):
	# print(loacl_path)
	# print(ssh_path)
	ssh,sftp = args['ssh'],args['sftp']
	stdin,stdout,stderr = ssh.exec_command('find '+ssh_path)
	result = stdout.read().decode('utf-8')
	# print(result)
	if len(result)==0:
		sftp.put(loacl_path,ssh_path)
		print('%s\t文件创建成功'%(filename))
		return 1
	else:
		local_size = os.path.getsize(loacl_path)
		stdin,stdout,stderr = ssh.exec_command('du -b '+ssh_path)
		result = stdout.read().decode('utf-8')
		s_size = int(result.split('\t')[0])
		# print('%s:本地文件大小为：%s，ssh文件大小为：%s'%(filename,local_size,s_size))
		if local_size == s_size:
			print('%s\t文件没有改动，不更新'%(filename))
			return 0
		else:
			sftp.put(loacl_path,ssh_path)
			print('%s\t文件更新成功'%(filename))
			return 1


# 检查文件夹
def checkFolder(ssh_folder,**args):
	config = args['config']
	ssh    = args['ssh']
	stdin,stdout,stderr = ssh.exec_command('find '+ssh_folder)
	result = stdout.read().decode('utf-8')
	if len(result)==0:
		print('目录%s不存在，创建目录'%ssh_folder)
		ssh.exec_command('mkdir '+ssh_folder)
		print('目录%s创建成功'%ssh_folder)
		return 1
	else:
		print('目录%s已存在'%ssh_folder)
		return 0




# # ssh文件列表
# ssh_file_list = []

def get_file_list(config,item):
	# 本地文件夹个数
	folder_list = []
	# 本地文件个数
	file_list = []
	# 判断字符串,去空格后是否为空
	local_path = config['local_path']
	for parent,dirnames,filenames in os.walk(os.path.join(local_path,item)):
		'''os.walk(config['local_path'])方法返回的一个tuple数据类型'''
		for dirname in dirnames:
			print(dirname)
			if dirname not in config['ignore_folder']:
				dirname = os.path.join(parent,dirname)
				dirname = dirname[int(dirname.find(item)):]
				# p.find(config['project_name'])找到对应的字符串的索引 
				# 然后在字符串的切割
				folder_list.append(dirname)

		for filename in filenames:
			#  过滤绝对忽略的文件，
			if filename not in config['ignore']:
				filename = os.path.join(parent,filename)
				filename = filename[int(filename.find(item)):]
				file_list.append(filename)
		
	# 返回文件list和文件夹list
	return (folder_list,file_list)

# print(folder_list)
# print(file_list)

# ssh控制台
def create_ssh(config):
	__ssh__ = paramiko.SSHClient()
	__ssh__.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	__ssh__.connect(hostname=config['hostname'], port=config['port'], username=config['username'], password=config['password'])
	# ssh传输
	transport = paramiko.Transport((config['hostname'],config['port']))
	transport.connect(username=config['username'],password=config['password'])
	__sftp__ = paramiko.SFTPClient.from_transport(transport)
	return (__ssh__,__sftp__)


# 检查服务器目录是否存在
def check_ssh_path(**args):
	config = args['config']
	folder = args['folder']
	ssh = args['ssh']
	root_path = os.path.join(config['ssh_path'],folder)

	stdin,stdout,stderr=ssh.exec_command('find '+root_path)
	result = stdout.read().decode('utf-8')

	if len(result)==0:
		print('目录%s不存在，创建目录'%root_path)
		ssh.exec_command('mkdir  '+root_path)
		print('创建成功')
		return 1
	else:
		print('目录%s存在，获取所有文件'%root_path)
		return 0



# 检查所有文件夹，没有就创建文件夹
def upload_folder(folder_list,**args):
	config=args['config']
	num = 0
	for folder in folder_list:
		_path = os.path.join(config['ssh_path'],folder)
		num = num+checkFolder(_path,**args)
	return num

# # 检查所有文件，
def upload_file(file_list,**args):
	update_file_num,config = 0,args['config']
	for file in file_list:
		local_file = os.path.join(config['local_path'],file)
		ssh_file = os.path.join(config['ssh_path'],file)
		update_file_num = update_file_num+checkFile(local_file,ssh_file,file,**args)
	return update_file_num


# 获取项目下的文件list和文件夹list
def get_file_folder_list(config):

	print('start upload!!')
	begin = datetime.datetime.now()
	# 记录上传的文件和文件夹数
	upload_file_num,upload_folder_num = 0,0 
	# 需要上传的文件和文件夹list
	folder_list,file_list = [],[]

	# print(config['project_name'])
	if 'project_name' not in config or len(config['project_name'])==0:
		print('project_name值不存在')
		print('上传local_path路径下的全部文件和文件夹')
		config['project_name'] = os.listdir(config['local_path'])



	local_path = config['local_path']
	for item in config['project_name']:
		item = item.strip()

		# print(local_path)
		if os.path.isdir(os.path.join(local_path,item))!= False:
			# 获取 project_name 目录下文件和文件夹
			folder_list.append(item)
			folders,files = get_file_list(config,item)
			file_list = file_list+files
			folder_list = folder_list+folders
		else:
			file_list.append(item)

	print('共有%s个文件待更新'%(len(file_list)))
	print('共有%s个文件夹待更新'%(len(folder_list)))
	ssh,sftp = create_ssh(config)
	# 检查文件夹，是否存在与创建
	upload_folder_num = upload_folder_num+upload_folder(folder_list,config=config,ssh=ssh)
	upload_file_num   = upload_file_num+upload_file(file_list,config=config,ssh=ssh,sftp=sftp)
	sftp.close()
	ssh.close()
	end = datetime.datetime.now()
	print('本次更新：%s个文件夹，%s个文件，耗时:%s'%(upload_folder_num,upload_file_num,end-begin))












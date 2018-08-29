import os
import json
import ssh
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-add', help='添加配置',action="store_true")
parser.add_argument('-look', help='编辑配置列表',action="store_true")
parser.add_argument('-upload', help='上传服务器',action="store_true")
parser.add_argument('-sheer', help='是否强制更新',action="store_true")
args = parser.parse_args()


__CWD__ = os.getcwd()
__CONFIG__ = os.path.join(__CWD__,'config.json')
# 按照 @ 符合切割成list , 然后在去空格
def strip_text(text_list):
	names = []
	if text_list.strip():
		text_list = text_list.split('@')
		for name in text_list:
			name = name.strip()
			names.append(name)
	return names
# 写入文件
def writeJsonToFile(text):
	file = open(__CONFIG__,'w')
	file.write(json.dumps(text,sort_keys=True,indent=2,separators=(',', ':'),ensure_ascii=False))
	file.close()
	print(__CONFIG__,'文件写入成功')

# 获取配置文件数据
def get_config_data():
	configs=[]
	if os.path.exists(__CONFIG__):
		fileData = open(__CONFIG__,'r')
		configs = json.loads(fileData.read())
	return configs

# 添加配置文件
def add_config():
	configs = get_config_data()
	try:
		project    		= input('\n项目名称：')
		local_path 		= input("\n本地项目路径：")

		print('\n本地项目路径下要上传的文件或文件夹')
		print('如有多个请用@符合隔开')
		project_name 	= input(">>>")
		print(strip_text(project_name))
		ssh_path 			= input("\n服务器项目路径：")
		hostname 			= input("\n服务器IP：")
		username 			= input("\n服务器用户名：")
		password 			= input("\n服务器密码：")
		port     			= int(input("\n上传端口："))

		print('\n本地项目路径下要要过滤不上传的文件')
		print('如有多个请用@符合隔开')
		ignore 	= input(">>>")
		print(strip_text(ignore))


		print('\n绝对过滤不上传的文件夹')
		print('如有多个请用@符合隔开')
		ignore_folder 	= input(">>>")
		print(strip_text(ignore_folder))


		config = {
			'project' 			: project.strip(),
			'local_path' 		: local_path.strip(),
			'project_name'	: strip_text(project_name),
			'ssh_path'			: ssh_path.strip(),
			'hostname'			: hostname.strip(),
			'username'			: username.strip(),
			'username'			: username.strip(),
			'password'			: password.strip(),
			'port' 					: port,
			'ignore'  			: strip_text(ignore),
			'ignore_folder' : strip_text(ignore_folder)
		}
		configs.append(config)
		writeJsonToFile(configs)
	except KeyboardInterrupt as key:
		print('取消添加配置')




# 查看配置文件
def read_config_data():
	configs = get_config_data()
	i=0
	for item in configs:
		print(i,':',item['project'])
		i = i+1



# 索引获取配置文件
def get_ssh_config():
	config = get_config_data()
	try:
		index = input('请输入要更新的服务索引：')
		index	= int(index)
		if index>len(config)-1:
			print(u'索引服务器不存在，请重新输入。')
			return get_ssh_config()
		else:
			return config[int(index)]
	except ValueError as v:
		print('请输入大于0的正整数值')
		get_ssh_config()
	except KeyboardInterrupt as key:
		print(key)

	# if type(index):


	

# 确认上传前的操作
def suer_upload():
	read_config_data()
	ssh_config = get_ssh_config()
	if not ssh_config:
		return
	try:
		bl = input('是否确认更新:%s:%s服务器？(yes/no)：'%(ssh_config['project'],ssh_config['hostname']))
		if bl.lower()=='yes' or bl.lower()=='y':
			if args.sheer:
				ssh_config['is_sheer_upload'] = 'yes'
			else:
				ssh_config['is_sheer_upload'] = 'no'
			ssh.get_file_folder_list(ssh_config)
		else:
			print('重新选择服务器上传：')
			suer_upload()
	except KeyboardInterrupt as key:
		print('取消上传')


if __name__ == '__main__':
	if args.add:
		add_config()
	elif args.look:
		read_config_data()
	elif args.upload:
		suer_upload()






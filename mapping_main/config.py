from ruamel import yaml


def parse_yaml(file: str) -> dict:
	''' Parse yaml file into dict '''
	try:
		info = yaml.safe_load(open(file))
		return info
	except Exception as e:
		print("Unable to find file....... ")
		return False


def get_host() -> dict:
	'''Get host '''
	info = parse_yaml('config.yaml')
	if info:
		try:
			return info['host']
		except Exception as e:
			print("Unable to find file..... ")
			return False
	else:
		return False

def get_port() -> dict:
	'''Get port '''
	info = parse_yaml('config.yaml')
	if info:
		try:
			return info['port']
		except Exception as e:
			print("Unable to find file..... ")
			return False
	else:
		return False


def get_url() -> dict:
	'''Get port '''
	info = parse_yaml('config.yaml')
	if info:
		try:
			return info['classification_url']
		except Exception as e:
			print("Unable to find file..... ")
			return False
	else:
		return False

def get_socket() -> dict:
	'''Get port '''
	info = parse_yaml('config.yaml')
	if info:
		try:
			return info['socket']
		except Exception as e:
			print("Unable to find socket url..... ")
			return False
	else:
		return False




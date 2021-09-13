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

def get_username() ->str:
    ''' Collecting username '''
    info = parse_yaml('./config.yaml')
    if info:
        try:
            return info['graph_username']
        except Exception as e:
            print("Unable to find username..... ")
            return False
    else:
        return False

def get_password() ->str:
    ''' Collecting password '''
    info = parse_yaml('./config.yaml')
    if info:
        try:
            return info['graph_password']
        except Exception as e:
            print("Unable to find password..... ")
            return False
    else:
        return False

def get_url() ->str:
    ''' Collecting url '''
    info = parse_yaml('./config.yaml')
    if info:
        try:
            return info['graph_url']
        except Exception as e:
            print("Unable to find url..... ")
            return False
    else:
        return False



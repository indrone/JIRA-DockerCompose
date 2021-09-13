
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 
import yaml
import config
import pandas as pd



def yaml_parse()-> dict:
	"""
 
	To parse yaml file

	Parameters
	----------
	None
		   

	Returns
	-------
	dict
		to get corpus of different class
		
 
	"""
	with open("corpus.yaml", 'r') as stream:
		try:
			corpus=yaml.safe_load(stream)
			#print(corpus)
			return(corpus)
		except yaml.YAMLError as exc:
			print(exc)
			return(exc)
			raise


def find_url_template(data: dict)-> str:
	"""
 
	To get dynamic mapping template
 
	Parameters
	----------
	data : dict
		meta dictionary including templateid
		   

	Returns
	-------
	str
		
 
	"""
	if not isinstance(data, dict):
		raise TypeError

	# if "Source" not in data:
	# 	raise KeyError
	#http://35.162.245.171:8086/api/templates

	if data['Source']['templateUrl']:
		print("Template URL ",data['Source']['templateUrl'])
		return data['Source']['templateUrl']

	else:
		return "Template URL Not found"

	# id:
	# 	# try:
	# 	# 	url="http://35.162.245.171:8086/api/templates"+str(data["Source"]["templateId"])+"/lineitems"

	# 	# 	print(url)
	# 	# 	return url
	# 	# except :
	# 	print("using fall back template Id")
	# 	url= config.Default_template_id
	# 	print(url)
	# 	return url

def roman_number(lineitem : str) -> str:
    """
 
    To remove roman numbers from lineitem
 
    Parameters
    ----------
    lineitem : str
        Input string of lineitem


    Returns
    -------
    sentance : str
        
    """
    # roman=["","I","II","III","IV","V","VI","VII","VIII","IX","X"]
    # remove_items=[".","-","+","/","(",")","*"]
    # str_=''.join([c for c in lineitem if c not in remove_items])
    # # print(str_)
    # sentance=""
    # for i in str_.split():
    #     if i.upper() in roman:
    #         pass
    #     else:
    #         sentance+=i+" "

    # if isinstance(sentance, str):
    #     sentance= sentance.lower().strip()

    # return sentance
    return lineitem.lower()


def template_api_to_dataframe(api_request_json: dict) -> object:
    """
 
    To identify the recommended template api json to dataframe
 
    Parameters
    ----------
    api_request_json : json 
        json of recommended template api 

    Returns
    -------
    Object:
        Dataframe of recommended template 
        
 
    """
    classname=[]
    subclassname=[]
    lineitems=[]
    coa=[]
    corpus=[]
    residual=[]
    classcode=[]
    subclasscode=[]
    try:
        for each in api_request_json['body']['lineitems']:
            if each['classname'] != None and each['formulae']== False:
                #print(each['classname'],each['label'],each['name'])
                classname.append(each['classname'])
                subclassname.append(each['subclassname'])
                lineitems.append(each['friendlyname'])
                coa.append(each['name'])
                corpus.append(each['aliases'])
                residual.append(each['residual'])
                classcode.append(each['classcode'])
                subclasscode.append(each['subclasscode'])

        label={"Class":classname, "Classcode":classcode, "Subclass":subclassname, "SubClasscode":subclasscode ,"Lineitem":lineitems,"chart_of_accounts":coa,"Corpus":corpus, "Residual":residual }
        df = pd.DataFrame(data=label)
        # print(df)
        # df.to_csv('temp.csv',index=False)
        return df

    except Exception as e:
        print(e)
        raise


def remaining_lineitems(template_dict:dict, mapped_lineitems:list)->list:

    total_lineitems = []
    try:
        for each in template_dict['body']['lineitems']:
            if each['classname'] != None and each['formulae']== False:
                
                total_lineitems.append({'classname':each['classname'], 'subclassname':each['subclassname'], 'componentcode':each['componentCode'], 'classcode': each['classcode'], 'subclasscode': each['subclasscode'], 'name':each['name'], 'label':each['label']})

        print("mapped_lineitems:::::", mapped_lineitems)
        unmapped_lineitems = [each2 for each2 in total_lineitems if each2['name'] not in mapped_lineitems]
        return unmapped_lineitems

    except Exception as e:
        print(e)
        raise


def normalize(a : str) -> float:
    """
 
    To get the string and convert into float removing irrelevantchar value
 
    Parameters
    ----------
    a : str
        string value   

    Returns
    -------
    float
        float number removing irrelevant char value
 
    """ 
    try:
        if len(a)==0 or len(a)>=15:
            return 0.0

        else:
            # a=[i.replace("(","-").replace(")","").replace("$","").replace(",","").replace("—","0").replace(" ","0") for i in a if "("]
            # a="".join(a)

            # retland_labelurn(float(a))

            a_temp= []
            for i in a:
                if "(":
                    a_temp.append(i.replace("(","-").replace(")","").replace("$","").replace(",","").replace("—","").replace(' ',"0"))

            a_new ="".join(a_temp)

            return(float(a_new))
   
   
    except ValueError:

        return (a)
        raise
    except AttributeError:
        return (a)
        raise


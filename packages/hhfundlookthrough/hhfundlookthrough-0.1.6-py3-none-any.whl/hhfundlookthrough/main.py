
import pandas as pd
import datetime
from hhfundlookthrough.hhfundlookthrough import *
from sqlalchemy import create_engine
import json



if __name__=='__main__':
	fundcode = '000979.OF'
	enddate = '20240212'
	with open("data.json", "r") as f:
		my_dict_from_file = json.load(f)
	df = getfitres(fundcode = fundcode,enddate = enddate,lookbackNdays = my_dict_from_file['lookbackNdays'], omega =  my_dict_from_file['omega'] ,engine = create_engine(my_dict_from_file['engine']))


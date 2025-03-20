from hhfundlookthrough.gamma.database import *
from hhfundlookthrough.gamma.optfunc import *
import pandas as pd
import datetime
from hhfundlookthrough.gamma.fitresults import *
import warnings
warnings.filterwarnings("ignore")
import json


def multgetfundcomp( code = None ):
	fundcode = code[0]
	enddate = code[1]
	print(fundcode,enddate )
	with open("data.json", "r") as f:
		my_dict_from_file = json.load(f)
	df = getfitres(fundcode=fundcode, enddate=enddate, lookbackNdays=my_dict_from_file['lookbackNdays'], omega=my_dict_from_file['omega'], engine = my_dict_from_file['engine'])
	if len(df)==0:
		pd.DataFrame([fundcode,enddate]).T.to_csv("./errorfund.csv", mode='a+', header=None)
	else:
		df.to_csv("./fundcomp.csv", mode='a+',header=None)


from multiprocessing import Process

class MtComp(Process ):
	def __init__(self, q):
		Process.__init__(self)
		self.q = q
	def run(self):
		while not self.q.empty():
			q_ = self.q.get(timeout=100)
			multgetfundcomp( code = q_)


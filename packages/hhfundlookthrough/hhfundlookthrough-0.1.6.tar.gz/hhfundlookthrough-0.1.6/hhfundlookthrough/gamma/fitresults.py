from hhfundlookthrough.gamma.database import *
from hhfundlookthrough.gamma.optfunc import *
import pandas as pd
import datetime


def getfitres(fundcode = None,enddate = None,lookbackNdays = 50 , omega = 0.05, engine = None ):
	'''

	:param fundcode: 基金代码
	:param enddate: 日期
	:param lookbackNdays: 回看天数
	:param omega: 惩罚系数
	:return: dataframe {F_PRT_STKVALUETONAV：占比 S_INFO_WINDCODE：股票   FUNFCODE：基金代码   ENDDATE：截至日期}
	'''
	DATA_DICT = download_fundinfo(fundcode = fundcode,enddate= enddate ,N = lookbackNdays,engine = engine )
	if DATA_DICT == {}:
		return pd.DataFrame()
	if DATA_DICT['ISSEA'] == 1:
		Seadict = GetSeasonDict(DATA_DICT=DATA_DICT)
		dfs =  seasonfillback(Seadict = Seadict)
		SEAMINICDICT =  GetSeaMinicDict(DATA_DICT = DATA_DICT, df = dfs )
		dfa = purefit(DATADICT = SEAMINICDICT, omega = omega)
	else:
		dfs = DATA_DICT['REC_STOCKPORT'][['S_INFO_STOCKWINDCODE','F_PRT_STKVALUETONAV' ]].rename(columns={'S_INFO_STOCKWINDCODE':'S_INFO_WINDCODE'})
		dfs = dfs[dfs['F_PRT_STKVALUETONAV']>0.001]
		SEAMINICDICT = GetSeaMinicDict(DATA_DICT=DATA_DICT, df= dfs )
		dfa = purefit(DATADICT = SEAMINICDICT, omega = omega)
	if type(dfa) != int :
		dfa['FUNFCODE'] = fundcode
		dfa['ENDDATE'] = enddate
		return dfa
	else:
		return pd.DataFrame()



if __name__ == '__main__':
	fundcode = '000979.OF'
	enddate = '20240401'
	lookbackNdays = 50
	df = getfitres(fundcode = fundcode,enddate = enddate,lookbackNdays = lookbackNdays, omega = 0.05 ,engine = None)






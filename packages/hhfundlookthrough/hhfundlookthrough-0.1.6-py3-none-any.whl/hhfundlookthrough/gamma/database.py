import pandas as pd
import datetime
import numpy as np
import copy
from hhfactor.algor.datetreatment import step_trade_dt



def download_fundinfo(fundcode = None,enddate= None, N= None ,engine = None ):
	"""
	download fund info
	:param fundcode: 基金代码
	:param enddate: 截至日期
	:param N: 回看天数
	:return: dict
	"""
	DATA_DICT = {}
	startdate = step_trade_dt(enddate , step=-N)

	#获取单个基金基本信息
	sql = "select F_INFO_WINDCODE,convert(nvarchar(100),F_INFO_FULLNAME) F_INFO_FULLNAME,F_INFO_ISINITIAL,F_INFO_ISSUEDATE,F_INFO_LISTDATE,F_INFO_DELISTDATE,convert(nvarchar(100),F_INFO_NAME) F_INFO_NAME ,convert(nvarchar(100),F_INFO_FIRSTINVESTTYPE) F_INFO_FIRSTINVESTTYPE,convert(nvarchar(100),F_INFO_CORP_FUNDMANAGEMENTCOMP) F_INFO_CORP_FUNDMANAGEMENTCOMP from ChinaMutualFundDescription where F_INFO_WINDCODE='%s'"%fundcode
	baseinfo = pd.read_sql(sql ,con =  engine)
	if len(baseinfo)== 0:
		print("数据库无基金基本数据")
		return {}
	DATA_DICT['Info'] = baseinfo

	#获取单个基金短期nav
	sql = "select F_INFO_WINDCODE,ANN_DATE,PRICE_DATE,F_NAV_UNIT,F_NAV_ADJUSTED from ChinaMutualFundNAV where F_INFO_WINDCODE='%s' and ANN_DATE >='%s'and ANN_DATE <='%s' order by ANN_DATE"%(fundcode,startdate,enddate )
	fundnav = pd.read_sql(sql ,con =  engine)
	DATA_DICT['REC_NAV'] = fundnav


	history_startdate = (datetime.datetime.strptime(enddate,'%Y%m%d' ) - datetime.timedelta(days=183)) .strftime('%Y%m%d')

	# 获取基金的过去一段时间的历史持仓
	sql = """select S_INFO_WINDCODE,F_PRT_ENDDATE,S_INFO_STOCKWINDCODE,F_PRT_STKVALUE,F_PRT_STKQUANTITY,F_PRT_STKVALUETONAV,ANN_DATE from ChinaMutualFundStockPortfolio where S_INFO_WINDCODE='%s' and ANN_DATE>='%s' and ANN_DATE<='%s' order by F_PRT_ENDDATE"""%(fundcode,history_startdate ,enddate)
	stockportfolio = pd.read_sql(sql ,con =  engine)
	stockpool = list(stockportfolio['S_INFO_STOCKWINDCODE'].drop_duplicates())


	# 获取A股和H股截止日的衍生
	sql = """
		   select S_INFO_WINDCODE,TRADE_DT,S_VAL_MV from AShareEODDerivativeIndicator  where TRADE_DT = '%s' order by S_INFO_WINDCODE,TRADE_DT
			""" %(startdate)
	todayasharedri = pd.read_sql(sql ,con =  engine)

	sql = """
		select S_INFO_WINDCODE,FINANCIAL_TRADE_DT as TRADE_DT ,S_VAL_MV from HKShareEODDerivativeIndex where FINANCIAL_TRADE_DT='%s' order by S_INFO_WINDCODE,FINANCIAL_TRADE_DT
		""" % ( startdate)
	todayhsharedridf = pd.read_sql(sql, con=engine)

	#股票衍生
	todaysharedri = todayasharedri._append(todayhsharedridf)

	#获取a股股票行业
	sql ="""
		select A.S_INFO_WINDCODE,A.SEC_IND_CODE,A.ENTRY_DT,A.REMOVE_DT,A.CUR_SIGN,convert(nvarchar(50),B.INDUSTRIESNAME) AS LEVEL1NAME,B.INDUSTRIESALIAS AS LEVEL1CODE from AShareSECNIndustriesClass A left join 
		(select INDUSTRIESCODE,INDUSTRIESNAME,INDUSTRIESALIAS,INDUSTRIESCODE_OLD from ASHAREINDUSTRIESCODE WHERE LEVELNUM = N'2' AND INDUSTRIESCODE LIKE N'12%%' ) B
		 on  left(SEC_IND_CODE,4)+'000000' = b.INDUSTRIESCODE_OLD where A.S_INFO_WINDCODE in %s"""%(str(tuple(list(todaysharedri['S_INFO_WINDCODE']) + stockpool )))
	astockindudf = pd.read_sql(sql, con=engine)

	#获取h股股票行业
	sql = f"""SELECT
		A.S_INFO_WINDCODE,
		A.WIND_IND_CODE,
		A.ENTRY_DT,
		A.REMOVE_DT,
		A.CUR_SIGN,
		CONVERT ( nvarchar ( 50 ), B.INDUSTRIESNAME ) AS LEVEL1NAME,
		B.INDUSTRIESALIAS AS LEVEL1CODE
	FROM
		HKStockWindIndustriesMembers A
		LEFT JOIN ( SELECT INDUSTRIESCODE, INDUSTRIESNAME, INDUSTRIESALIAS, INDUSTRIESCODE_OLD FROM ASHAREINDUSTRIESCODE WHERE LEVELNUM = N'2' AND INDUSTRIESCODE LIKE N'62%%' ) B ON LEFT ( WIND_IND_CODE, 4 ) + '000000' = b.INDUSTRIESCODE_OLD
		where A.S_INFO_WINDCODE in {(str(tuple(list(todaysharedri['S_INFO_WINDCODE']) + stockpool )))}"""
	hstockindudf = pd.read_sql(sql, con=engine)

	#合并a股h股所属行业
	stockindu = astockindudf[['S_INFO_WINDCODE','ENTRY_DT','REMOVE_DT','LEVEL1CODE']]._append(hstockindudf[['S_INFO_WINDCODE','ENTRY_DT','REMOVE_DT','LEVEL1CODE']])
	stockindu.fillna(enddate ,inplace=True)

	#获取起始日股价变化情况
	todaysharedri = todaysharedri.merge(stockindu,on='S_INFO_WINDCODE',how='left')
	todaysharedri = todaysharedri.sort_values(by=['LEVEL1CODE','S_VAL_MV'],ascending=False)

	#获取每日每个行业市值最大得前三个个股
	todaysharedri = todaysharedri.groupby('LEVEL1CODE').head(3)
	stockpool = stockpool + list(todaysharedri['S_INFO_WINDCODE'])
	DATA_DICT['STOCKPOOL'] = list(set(stockpool))


	# 提取最近一段时间的债券变化
	sql = f"select S_INFO_WINDCODE,TRADE_DT,S_DQ_PCTCHANGE from CBIndexEODPrices where S_INFO_WINDCODE = 'CBA00103.CS'  and TRADE_DT >= {startdate} and TRADE_DT<={enddate}  ORDER BY  S_INFO_WINDCODE,TRADE_DT"
	cbond_rec = pd.read_sql(sql, con=engine)
	DATA_DICT['REC_BONDPCT'] = cbond_rec

	def getstockpct(stockpool = None, startdate= None, enddate= None  ):
		#获取a股股价变化
		sql = """
				select S_INFO_WINDCODE,TRADE_DT,S_DQ_PCTCHANGE from AShareEODPrices where S_INFO_WINDCODE in %s and TRADE_DT>='%s' and TRADE_DT <= '%s' order by S_INFO_WINDCODE,TRADE_DT
				""" % (str(tuple(stockpool)), startdate,enddate)
		asharedf = pd.read_sql(sql, con=engine)
		#获取h股股价变化
		sql = """select S_INFO_WINDCODE,TRADE_DT,100*(S_DQ_ADJPRECLOSE-S_DQ_ADJCLOSE)/S_DQ_ADJCLOSE as S_DQ_PCTCHANGE from HKshareEODPrices where S_INFO_WINDCODE in %s and TRADE_DT>='%s' and TRADE_DT <= '%s' order by S_INFO_WINDCODE,TRADE_DT"""  % (str(tuple(stockpool)), startdate,enddate)
		hksharedf = pd.read_sql(sql, con=engine)
		#合并股价变化
		stockpctchange = asharedf._append(hksharedf)
		return stockpctchange


	#合并股价变化和行业
	stockpctchange =  getstockpct(stockpool, startdate, enddate  )
	stockpctchangeindu = stockpctchange.merge(stockindu,on ='S_INFO_WINDCODE', how = 'left' )
	stockpctchangeindu = stockpctchangeindu[(stockpctchangeindu['TRADE_DT']>=stockpctchangeindu['ENTRY_DT'])&(stockpctchangeindu['TRADE_DT']<=stockpctchangeindu['REMOVE_DT'])]

	DATA_DICT['REC_STOCKPCT'] = stockpctchangeindu

	reportseason = stockportfolio['F_PRT_ENDDATE'].max()
	DATA_DICT['REC_SEA'] = reportseason

	#获取最近一期的持仓
	stockportfolio_recent =stockportfolio [ stockportfolio['F_PRT_ENDDATE'] == reportseason ]
	DATA_DICT['REC_STOCKPORT'] = stockportfolio_recent

	#获取最近一期的行业组合情况
	sql = """select S_INFO_WINDCODE,F_PRT_ENDDATE,F_ANN_DATE,S_INFO_CSRCINDUSCODE,F_PRT_INDUSTONAV,convert(nvarchar(50),S_INFO_CSRCINDUSNAME) S_INFO_CSRCINDUSNAME from ChinaMutualFundIndPortfolio where S_INFO_WINDCODE = '%s' and F_PRT_ENDDATE ='%s'""" % (fundcode,reportseason )
	induportfolio_recent = pd.read_sql(sql, con=engine)
	DATA_DICT['REC_INDUPORT'] = induportfolio_recent

	#获取最近一期的资产组合情况
	sql = """select S_INFO_WINDCODE,F_PRT_ENDDATE,F_ANN_DATE,F_PRT_STOCKTONAV,F_PRT_CASHTONAV,F_PRT_BONDTONAV from ChinaMutualFundAssetPortfolio where S_INFO_WINDCODE = '%s' and F_PRT_ENDDATE ='%s'""" % (fundcode,reportseason )
	assetdf_recent = pd.read_sql(sql, con=engine)
	DATA_DICT['REC_ASTPORT'] = assetdf_recent
	zjhinduclass = {'A': '883018.WI', 'B': '883019.WI', 'C': '883020.WI', 'D': '883021.WI', 'E': '883022.WI',
					'F': '883023.WI', 'G': '883024.WI', 'H': '883025.WI', 'I': '883026.WI', 'J': '883027.WI',
					'K': '883028.WI', 'L': '883029.WI', 'M': '883030.WI', 'N': '883031.WI', 'O': '883036.WI',
					'P': '883035.WI', 'Q': '883032.WI', 'R': '882108.WI', 'S': '883188.WI', '10': '887101.WI',
					'15': '887102.WI', '20': '887103.WI', '25': '887104.WI', '30': '887105.WI', '35': '887106.WI',
					'40': '887107.WI', '45': '887108.WI', '50': '887109.WI', '55': '887110.WI', '60': '887202.WI'}
	zjhinduclass_dict = dict(zip(zjhinduclass.values(), zjhinduclass.keys()))

	DATA_DICT['ISSEA'] = 0
	# 如果是季报，需要进行季报补全操作，提取季报到季报发布之前一段时间的数据
	if len(stockportfolio_recent)<=15:


		seasonstartdate =  step_trade_dt(reportseason , step=-30)
		getstockpct_season = getstockpct(stockpool , seasonstartdate , reportseason  )
		getstockpct_season = getstockpct_season.merge(stockindu,on ='S_INFO_WINDCODE', how = 'left' )
		getstockpct_season = getstockpct_season[(getstockpct_season['TRADE_DT']>=getstockpct_season['ENTRY_DT'])&(getstockpct_season['TRADE_DT']<=getstockpct_season['REMOVE_DT'])]
		DATA_DICT['SEA_STOCKPCT'] = getstockpct_season
		sql = "select F_INFO_WINDCODE,ANN_DATE,PRICE_DATE,F_NAV_UNIT,F_NAV_ADJUSTED from ChinaMutualFundNAV where F_INFO_WINDCODE='%s' and ANN_DATE >='%s'and ANN_DATE <='%s' order by ANN_DATE" % (
		fundcode,seasonstartdate, reportseason )
		fundnav_season = pd.read_sql(sql, con=engine)
		DATA_DICT['SEA_NAV'] = fundnav_season
		# 提取证监会行业指数变动情况
		sql = f"""select S_INFO_WINDCODE,TRADE_DT,S_DQ_PCTCHANGE from AIndexWindIndustriesEOD where S_INFO_WINDCODE in {str(tuple(zjhinduclass.values()))} and TRADE_DT >= {seasonstartdate} and TRADE_DT<={reportseason} order by S_INFO_WINDCODE,TRADE_DT"""
		indupct_season = pd.read_sql(sql, engine)
		indupct_season['S_INFO_WINDCODE'] = indupct_season['S_INFO_WINDCODE'].replace(zjhinduclass_dict)
		DATA_DICT['SEA_INDUPCT'] = indupct_season
		# 提取季度的债券变化
		sql = f"select S_INFO_WINDCODE,TRADE_DT,S_DQ_PCTCHANGE from CBIndexEODPrices where S_INFO_WINDCODE = 'CBA00103.CS'  and TRADE_DT >= {seasonstartdate} and TRADE_DT<={reportseason}  ORDER BY  S_INFO_WINDCODE,TRADE_DT"
		cbond_seacon = pd.read_sql(sql, con=engine)
		DATA_DICT['SEA_BONDPCT'] = cbond_seacon
		DATA_DICT['ISSEA'] = 1




	sql = f"select S_INFO_WINDCODE,TRADE_DT,S_DQ_PCTCHANGE from CBIndexEODPrices where S_INFO_WINDCODE = 'CBA00103.CS'  and TRADE_DT >= {startdate} and TRADE_DT<={enddate}  ORDER BY  S_INFO_WINDCODE,TRADE_DT"
	cbond_seacon = pd.read_sql(sql, con=engine)
	DATA_DICT['REC_BONDPCT'] = cbond_seacon


	#提取证监会行业指数变动情况
	sql  = f"""select S_INFO_WINDCODE,TRADE_DT,S_DQ_PCTCHANGE from AIndexWindIndustriesEOD where S_INFO_WINDCODE in {str(tuple(zjhinduclass.values()))} and TRADE_DT >= {startdate} and TRADE_DT<={enddate} order by S_INFO_WINDCODE,TRADE_DT"""
	indupct = pd.read_sql(sql , engine)
	zjhinduclass_dict = dict(zip( zjhinduclass.values(),zjhinduclass.keys()))
	indupct['S_INFO_WINDCODE'] = indupct['S_INFO_WINDCODE'].replace(zjhinduclass_dict)
	DATA_DICT['REC_INDUPCT'] = indupct


	return DATA_DICT

def GetSeasonDict(DATA_DICT = None):

	datadict = copy.deepcopy(DATA_DICT)
	stockpool = datadict['STOCKPOOL']
	#season
	seanav = datadict['SEA_NAV']
	seanav['NavPct'] = 100*seanav['F_NAV_ADJUSTED'].pct_change(limit=1)
	seanav.rename(columns={'PRICE_DATE':'TRADE_DT'},inplace=True)
	seanav.set_index('TRADE_DT',inplace=True)
	seastock = datadict['SEA_STOCKPCT']
	pctmap = seastock.set_index(['TRADE_DT','S_INFO_WINDCODE']).S_DQ_PCTCHANGE.unstack().loc[:,stockpool]
	seabond = datadict['SEA_BONDPCT']
	seabond.set_index('TRADE_DT',inplace=True)
	seabond.rename(columns={'S_DQ_PCTCHANGE':'BONDPCT'},inplace=True)
	seanav = seanav[['NavPct']].join(pctmap ).join(seabond[['BONDPCT']])
	seanav = seanav.dropna(subset='NavPct')
	seanav = seanav[seanav.count(axis=1)>0.9*len(seanav.columns)]
	#seasonindu
	seastockindu = seastock.groupby('S_INFO_WINDCODE').LEVEL1CODE.last()
	seastockindu = seastockindu.loc[stockpool]
	# 前十大股票及其权重
	seasondf = datadict['REC_STOCKPORT'].copy()
	seasondf = seasondf.sort_values(by = 'F_PRT_STKVALUETONAV', ascending = False).iloc[:10]
	topstock = list(seasondf['S_INFO_STOCKWINDCODE'])
	topstockweight = list(seasondf['F_PRT_STKVALUETONAV'])
	topstockinduce = [stockpool.index(topstockcode_)  for topstockcode_ in topstock]
	#行业分布
	indudis = datadict['REC_INDUPORT'][['S_INFO_CSRCINDUSCODE', 'F_PRT_INDUSTONAV']]
	indudis['S_INFO_CSRCINDUSCODE'] = indudis['S_INFO_CSRCINDUSCODE'].apply(lambda x:x[-2:])
	indudis = indudis[indudis['F_PRT_INDUSTONAV']>1]
	#持仓情况
	assetportfolio = datadict['REC_ASTPORT'].fillna(0).iloc[0]
	#变量数量
	N = len(stockpool )+1
	#十大重仓行业和披露行业平衡，如果十大重仓行业高于披露行业则去除
	DataPortfolioItemp = seasondf.merge(seastockindu.to_frame('INDU'),left_on = 'S_INFO_STOCKWINDCODE', right_index =True )
	DataPortfolioItempx = DataPortfolioItemp.groupby('INDU',as_index=False)[ 'F_PRT_STKVALUETONAV'].sum()
	DataPortfolioItempx = DataPortfolioItempx.merge(indudis,left_on ='INDU',right_on = 'S_INFO_CSRCINDUSCODE', how='outer'  )
	rebalancedindu = DataPortfolioItempx[DataPortfolioItempx['F_PRT_STKVALUETONAV']<DataPortfolioItempx['F_PRT_INDUSTONAV']]

	Seadict = {
		'topstockweight':topstockweight,
		'assetportfolio':assetportfolio,
		'topstockinduce':topstockinduce,
		'rebalancedindu':rebalancedindu,
		'seanav':seanav,
		'seastockindu':seastockindu,
		'N' :N
	}
	return Seadict

def GetSeaMinicDict(DATA_DICT = None, df = None ):

	datadict = copy.deepcopy(DATA_DICT)
	stockpool = list(df.S_INFO_WINDCODE)[:-1]
	N = len(df)
	recnav = datadict['REC_NAV']
	recnav['NavPct'] = 100 * recnav['F_NAV_ADJUSTED'].pct_change(limit=1)
	recnav.rename(columns={'PRICE_DATE': 'TRADE_DT'}, inplace=True)
	recnav.set_index('TRADE_DT', inplace=True)
	recstock = datadict['REC_STOCKPCT']
	pctmap = recstock.set_index(['TRADE_DT', 'S_INFO_WINDCODE']).S_DQ_PCTCHANGE.unstack().loc[:, stockpool]
	recbond = datadict['REC_BONDPCT']
	recbond.set_index('TRADE_DT', inplace=True)
	recbond.rename(columns={'S_DQ_PCTCHANGE': 'BONDPCT'}, inplace=True)
	recnav = recnav[['NavPct']].join(pctmap).join(recbond[['BONDPCT']])
	recnav = recnav.dropna(subset='NavPct')
	recnav = recnav[recnav.count(axis=1) > 0.9 * len(recnav.columns)]
	recnav.fillna(0,inplace=True)
	stockindexweight = list(df.F_PRT_STKVALUETONAV)
	stockpoolall = list(df.S_INFO_WINDCODE)
	totalweight = np.sum(df.iloc[:-1].F_PRT_STKVALUETONAV)

	SEAMINICDICT = {
		'recnav':recnav,
		'stockindexweight':stockindexweight,
		'stockpoolall':stockpoolall,
		'N':N,
		'totalweight':totalweight
	}

	return SEAMINICDICT













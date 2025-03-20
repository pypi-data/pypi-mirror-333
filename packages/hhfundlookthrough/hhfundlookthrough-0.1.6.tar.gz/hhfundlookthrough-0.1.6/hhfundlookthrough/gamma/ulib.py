import pandas as pd
import datetime

def getwindmixfund(stdate='20240330' ,eddate='20240430', freq = 'W', windcode = '885001.WI',engine = None):
	df = pd.read_sql(
		"select a.S_CON_CODE,a.S_INFO_WINDCODE,a.S_CON_INDATE,a.S_CON_OUTDATE from CFundWindIndexMembers a , CFundWindIndexcomponent b where  b.S_INFO_WINDCODE = '%s' and a.S_CON_CODE = b.S_CON_CODE"%windcode,
		con=engine)
	df['S_CON_OUTDATE'] = pd.to_datetime(df['S_CON_OUTDATE'].fillna(datetime.datetime.now().strftime("%Y%m%d")))
	df['S_CON_INDATE'] = pd.to_datetime(df['S_CON_INDATE'])
	dftime = pd.DataFrame(1, index=pd.date_range(stdate, eddate, freq=freq), columns=df.S_INFO_WINDCODE)
	dftime = dftime.stack().reset_index(name='IS').rename(columns={'level_0': 'DT'})
	dftime = dftime.merge(df, on='S_INFO_WINDCODE', how='left')
	dftime = dftime[(dftime['DT'] >= dftime['S_CON_INDATE']) & (dftime['DT'] <= dftime['S_CON_OUTDATE'])]
	# 格式化日期
	dftime['DTSTR'] = dftime['DT'].dt.strftime('%Y%m%d')
	return dftime



zjhinduclass = {'A' :'883018.WI',
'B' :'883019.WI',
'C' :'883020.WI',
'D' :'883021.WI',
'E' :'883022.WI',
'F' :'883023.WI',
'G' :'883024.WI',
'H' :'883025.WI',
'I' :'883026.WI',
'J': '883027.WI',
'K': '883028.WI',
'L': '883029.WI',
'M' :'883030.WI',
'N' :'883031.WI',
'O' :'883036.WI',
'P' :'883035.WI',
'Q' :'883032.WI',
'R':'882108.WI',
'S':'883188.WI',
'10' :'887101.WI',
'15' :'887102.WI',
'20' :'887103.WI',
'25': '887104.WI',
'30' :'887105.WI',
'35' :'887106.WI',
'40' :'887107.WI',
'45' :'887108.WI',
'50' :'887109.WI',
'55' :'887110.WI',
'60' :'887202.WI'
				}

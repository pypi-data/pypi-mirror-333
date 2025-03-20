
import cvxpy as cp

# cp.installed_solvers()

import pandas as pd
import numpy as np



def seasonfillback(Seadict = None):

	topstockweight = Seadict['topstockweight']
	assetportfolio = Seadict['assetportfolio']
	topstockinduce = Seadict['topstockinduce']
	rebalancedindu = Seadict['rebalancedindu']
	seastockindu = Seadict['seastockindu']
	seanav = Seadict['seanav']
	N = Seadict['N']

	weights = cp.Variable(N)
	MINWEIGHT = np.min(topstockweight)
	TOTALWEIGHT = 100 - assetportfolio.F_PRT_CASHTONAV
	bondweight = assetportfolio.F_PRT_BONDTONAV
	constraints = [
		# 权重之和固定
		cp.sum(weights[:-1]) == TOTALWEIGHT,
		# 权重应该大于等于0
		weights >= 0,
		# 固定前10大持仓
		weights[topstockinduce] == topstockweight,
		weights[-1] == bondweight,
	]
	# 剩余持仓不超过第十个
	for i in list(set(np.arange(0, N - 1, 1)) - set(topstockinduce)):
		constraints.append(weights[i] <= MINWEIGHT)
	# # 行业限制
	# for ini in list(seastockindu.drop_duplicates()):
	for ini in list(rebalancedindu.S_INFO_CSRCINDUSCODE)[:3]:
		INDUSTONAV = rebalancedindu[rebalancedindu.S_INFO_CSRCINDUSCODE == ini].F_PRT_INDUSTONAV.iloc[0]
		constraints.append(cp.sum(weights[np.where(seastockindu == ini)[0]]) == INDUSTONAV)

	objective = cp.Minimize(
		cp.norm2((0.01 * seanav.iloc[:, 1:].values @ weights) - seanav.iloc[:, 0].values))
	prob = cp.Problem(objective, constraints)
	result = prob.solve(solver='SCS')
	if result >-10 and result<10:

		df = seastockindu.to_frame('Indu').reset_index()
		df['F_PRT_STKVALUETONAV'] = weights.value[:-1]
		df = df[df['F_PRT_STKVALUETONAV']>0.001]
		df.sort_values(by='F_PRT_STKVALUETONAV', ascending=False,inplace=True)
		df = df._append(pd.Series(['BONDPCT','BOND',weights.value[-1]], index=['S_INFO_WINDCODE', 'Indu','F_PRT_STKVALUETONAV']),
						ignore_index=True)
		return df
	else:
		return 0



def purefit(DATADICT = None, omega = 0.02):
	recnav = DATADICT['recnav']
	stockindexweight = DATADICT['stockindexweight']
	stockpoolall = DATADICT['stockpoolall']
	N = DATADICT['N']
	totalweight = DATADICT['totalweight']
	weights = cp.Variable(N)
	constraints = [
		# 权重范围
		cp.sum(weights) <= 95,
		cp.sum(weights) >= 60,
		weights >= 0,
		weights[np.arange(N-1)] <= 10
	]

	objective = cp.Minimize(
		cp.norm2((0.01 * recnav.iloc[:,1:].values @ weights) - recnav['NavPct'].values) + omega * cp.norm1(weights - stockindexweight) +  0.4 * omega * cp.norm1( cp.sum(weights) - totalweight) )
	prob = cp.Problem(objective, constraints)
	result = prob.solve(solver='SCS')
	if result>-10 and result<10:
		minic_df = pd.DataFrame([weights.value, stockpoolall],
								index=['F_PRT_STKVALUETONAV', 'S_INFO_WINDCODE']).T
		return minic_df
	else:
		return 0













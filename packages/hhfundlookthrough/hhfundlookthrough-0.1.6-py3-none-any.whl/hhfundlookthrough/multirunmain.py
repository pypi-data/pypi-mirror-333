

import pandas as pd
from sqlalchemy import create_engine
import datetime as dt
from dateutil.parser import parse
import time
from alpha.multirun import *
from multiprocessing import cpu_count, Process,Queue,Pool
import shutil



if __name__ == '__main__':
    time_start = time.time()
    import pandas as pd
    import datetime
    from gamma.ulib import getwindmixfund
    with open("data.json", "r") as f:
        my_dict_from_file = json.load(f)

    dftime = getwindmixfund(stdate='20240330' ,eddate='20240430', freq = 'W', windcode = '885001.WI', engine = create_engine(my_dict_from_file['engine']))
    num_processes = 6
    workQueue = Queue(8000)
    for i in range(20):
        workQueue.put([dftime.iloc[i].S_INFO_WINDCODE, dftime.iloc[i].DTSTR ]   )
    Process = []
    for _ in range(num_processes):
        print(_)
        p = MtComp(workQueue)
        Process.append(p)
    for p in Process:
        p.start()
    for p in Process:
        p.join()
    time_end  = time.time()
    time_spend = time_end - time_start
    print('cost time: %.3f s' % ( time_spend))


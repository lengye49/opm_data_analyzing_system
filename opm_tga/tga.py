import json
import grequests
from datetime import datetime as dt

sql_extreme = r"""select * from (select group_0, map_agg(date_time, amount_0) filter (where amount_0 is not null) data_map_0,
 sum(amount_0) filter (where is_finite(amount_0)) total_amount, count(1) over () group_num from (select timestamp 
 '2021-03-24' date_time, ta_ev."extreme_type" group_0, coalesce(MAX(ta_ev."floor"),0.0) amount_0 from (select *, if(
 "#vp@TimeZone" is not null and "#vp@TimeZone">=-12 and "#vp@TimeZone"<=14, date_add('second', cast((0-"#vp@TimeZone")
 *3600 as integer), "#event_time"), "#event_time") "@vpc_tz_#event_time" from (select * , try_cast((try("time"-"time"))
  as double) as "#vp@TimeZone" from ( v_event_15 ) logic_table)) ta_ev where ((( ( "$part_event" IN ( 
  's_extremesimulationfight' ) ) )) and (ta_ev."is_win" IN (1))) and (("$part_date" between '2020-11-28' and 
  '2021-03-25') and ("@vpc_tz_#event_time" >= timestamp '2020-11-29' and "@vpc_tz_#event_time" < date_add('day', 1, 
  TIMESTAMP '2021-03-24'))) group by ta_ev."extreme_type") GROUP BY group_0) ORDER BY total_amount DESC limit 1000"""

sql_stage = r"""select * from (select group_0, map_agg(date_time, amount_0) filter (where amount_0 is not null) 
data_map_0, sum(amount_0) filter (where is_finite(amount_0)) total_amount, count(1) over () group_num from (select 
ta_date_trunc('day',ta_ev."@vpc_tz_#event_time", 1) date_time, ta_ev."main_stage" group_0, coalesce(COUNT(DISTINCT 
ta_ev."#user_id"),0.0) amount_0 from (select *, if("#vp@TimeZone" is not null and "#vp@TimeZone">=-12 and 
"#vp@TimeZone"<=14, date_add('second', cast((0-"#vp@TimeZone")*3600 as integer), "#event_time"), "#event_time") 
"@vpc_tz_#event_time" from (select * , try_cast((try("time"-"time")) as double) as "#vp@TimeZone" from ( v_event_15 ) 
logic_table)) ta_ev where ((( ( "$part_event" IN ( 's_stage' ) ) )) and (ta_ev."main_stage" IN (1429,1489,1549,1609,
1669,1729,1789))) and (("$part_date" between '2020-09-28' and '2021-03-25') and ("@vpc_tz_#event_time" >= timestamp 
'2020-09-29' and "@vpc_tz_#event_time" < date_add('day', 1, TIMESTAMP '2021-03-24'))) group by ta_date_trunc('day',
ta_ev."@vpc_tz_#event_time", 1), ta_ev."main_stage") GROUP BY group_0) ORDER BY group_0 limit 1000"""


def get_extreme_floor(datalists):
    s = ''
    for dt in datalists:
        if dt[0] == '11':
            s += '标准塔: ' + str(int(dt[2])) + '\n'
        else:
            s += '类型塔' + str(int(dt[0])) + ': ' + str(int(dt[2])) + '\n'
    return s


def get_stage_desc(k, v):
    
    pass

def get_stage(datalists):
    s = ''
    for dt in datalists:
        s += str(dt[0]) + ': ' + str(dt[2]) + '\n'
    return s


def parse_tga_data(data):
    data_lists = []
    first = True
    for line in data.splitlines():
        if first:
            res = json.loads(line)
            ret_code = res['return_code']
            if ret_code != 0:
                print(f'Error code: {ret_code} Msg: {res["return_message"]}')
                exit(1)
            else:
                columns = res['data']['headers']
            first = False
        else:
            data_lists.append(json.loads(line))

    return data_lists


def get_tga_data(sql):

    url = "http://103.244.232.82:8992/querySql"
    data = {"token": "ZqDjVN5Jk1nmHzn0qRpcvE20ra0tcs0pNnd7kgMXiy86PblJNnbgt4T7uGkcIUef",
            "sql": sql}

    req_list = [  # 请求列表
        grequests.post(url, data=data),
    ]

    res_list = grequests.map(req_list)  # 并行发送，等最后一个运行完后返回

    for res in res_list:
        if res is None:
            # 请求失败
            print("请求出错!")
            exit(1)
        return parse_tga_data(res.text)


def get_max_extreme_floor():
    t1 = dt.now().strftime('%Y-%m-%d')
    sql_extreme.replace('2021-03-25', t1)
    data = get_tga_data(sql_extreme)
    result = get_extreme_floor(data)
    return result

def get_max_stage():
    t1 = dt.now().strftime('%Y-%m-%d')
    sql_stage.replace('2021-03-25', t1)
    data = get_tga_data(sql_stage)
    result = get_stage(data)
    return result

print(get_max_stage())
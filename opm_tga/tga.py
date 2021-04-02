import json
import grequests
from datetime import datetime as dt


def get_extreme_floor(datalists):
    s = '极限模拟战最高通关情况：\n'
    for dt in datalists:
        if int(dt[0]) == 11:
            s += '标准塔: ' + str(int(dt[2])) + '\n'
        else:
            s += '类型塔' + str(int(dt[0])) + ': ' + str(int(dt[2])) + '\n'
    return s


def get_stage_desc(k, v):
    if k == 1429.0:
        return '通关27-60: ' + v.strip('.0')
    elif k == 1489.0:
        return '通关28-60: ' + v.strip('.0')
    elif k == 1549.0:
        return '通关29-60: ' + v.strip('.0')
    elif k == 1609.0:
        return '通关30-60: ' + v.strip('.0')
    elif k == 1669.0:
        return '通关31-60: ' + v.strip('.0')
    elif k == 1729.0:
        return '通关32-60: ' + v.strip('.0')
    elif k == 1789.0:
        return '通关33-60: ' + v.strip('.0')
    elif k == 1849.0:
        return '通关34-60: ' + v.strip('.0')
    elif k == 1909.0:
        return '通关35-60: ' + v.strip('.0')
    pass


def get_stage(datalists):
    s = '副本最高通关情况：\n'
    for dt in datalists:
        s += get_stage_desc(dt[0], dt[2]) + '\n'
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
    sql = r"""select * from (select group_0, map_agg(date_time, amount_0) filter (where amount_0 is not null) data_map_0,
 sum(amount_0) filter (where is_finite(amount_0)) total_amount, count(1) over () group_num from (select timestamp 
 '2021-03-24' date_time, ta_ev."extreme_type" group_0, coalesce(MAX(ta_ev."floor"),0.0) amount_0 from (select *, if(
 "#vp@TimeZone" is not null and "#vp@TimeZone">=-12 and "#vp@TimeZone"<=14, date_add('second', cast((0-"#vp@TimeZone")
 *3600 as integer), "#event_time"), "#event_time") "@vpc_tz_#event_time" from (select * , try_cast((try("time"-"time"))
  as double) as "#vp@TimeZone" from ( v_event_15 ) logic_table)) ta_ev where ((( ( "$part_event" IN ( 
  's_extremesimulationfight' ) ) )) and (ta_ev."is_win" IN (1))) and (("$part_date" between '2020-11-28' and 
  '2021-03-25') and ("@vpc_tz_#event_time" >= timestamp '2020-11-29' and "@vpc_tz_#event_time" < date_add('day', 1, 
  TIMESTAMP '2021-03-24'))) group by ta_ev."extreme_type") GROUP BY group_0) ORDER BY total_amount DESC limit 1000"""

    t1 = dt.now().strftime('%Y-%m-%d')
    sql = sql.replace('2021-03-25', t1)
    print(sql)
    data = get_tga_data(sql)
    result = get_extreme_floor(data)
    return result


def get_max_stage():
    sql = r"""select * from (select group_0, map_agg(date_time, amount_0) filter (where amount_0 is not null) 
    data_map_0, sum(amount_0) filter (where is_finite(amount_0)) total_amount, count(1) over () group_num from (select 
    ta_date_trunc('day',ta_ev."@vpc_tz_#event_time", 1) date_time, ta_ev."main_stage" group_0, coalesce(COUNT(DISTINCT 
    ta_ev."#user_id"),0.0) amount_0 from (select *, if("#vp@TimeZone" is not null and "#vp@TimeZone">=-12 and 
    "#vp@TimeZone"<=14, date_add('second', cast((0-"#vp@TimeZone")*3600 as integer), "#event_time"), "#event_time") 
    "@vpc_tz_#event_time" from (select * , try_cast((try("time"-"time")) as double) as "#vp@TimeZone" from ( v_event_15 ) 
    logic_table)) ta_ev where ((( ( "$part_event" IN ( 's_stage' ) ) )) and (ta_ev."main_stage" IN (1429,1489,1549,1609,
    1669,1729,1789))) and (("$part_date" between '2020-09-28' and '2021-03-25') and ("@vpc_tz_#event_time" >= timestamp 
    '2020-09-29' and "@vpc_tz_#event_time" < date_add('day', 1, TIMESTAMP '2021-03-24'))) group by ta_date_trunc('day',
    ta_ev."@vpc_tz_#event_time", 1), ta_ev."main_stage") GROUP BY group_0) ORDER BY group_0 limit 1000"""
    t1 = dt.now().strftime('%Y-%m-%d')
    sql = sql.replace('2021-03-25', t1)
    print(sql)
    data = get_tga_data(sql)
    result = get_stage(data)
    return result


def get_max_player_level():
    sql = r"""select * from (select map_agg(date_time, amount_0) filter (where amount_0 is not null) data_map_0, 
    sum(amount_0) filter (where is_finite(amount_0)) total_amount, count(1) over () group_num from (select timestamp 
    '2021-03-25' date_time, coalesce(MAX(ta_ev."after_player_level"),0.0) amount_0 from (select *, if("#vp@TimeZone" 
    is not null and "#vp@TimeZone">=-12 and "#vp@TimeZone"<=14, date_add('second', cast((0-"#vp@TimeZone")*3600 as 
    integer), "#event_time"), "#event_time") "@vpc_tz_#event_time" from (select * , try_cast((try("time"-"time")) as 
    double) as "#vp@TimeZone" from ( v_event_15 ) logic_table)) ta_ev where (( ( "$part_event" IN ( 's_player_level_up'
     ) ) )) and (("$part_date" between '2021-02-23' and '2021-03-25') and ("@vpc_tz_#event_time" >= timestamp 
     '2021-02-24' and "@vpc_tz_#event_time" < date_add('day', 1, TIMESTAMP '2021-03-25'))) ) ) ORDER BY total_amount 
     DESC limit 1000"""
    t1 = dt.now().strftime('%Y-%m-%d')
    sql = sql.replace('2021-03-25', t1)
    print(sql)
    data = get_tga_data(sql)
    return '最大玩家等级: ' + str(int(data[0][1]))


def get_max_hero_level():
    sql = r"""select * from (select map_agg(date_time, amount_0) filter (where amount_0 is not null) data_map_0, 
    sum(amount_0) filter (where is_finite(amount_0)) total_amount, count(1) over () group_num from (select timestamp 
    '2021-03-25' date_time, coalesce(MAX(ta_ev."connect_level"),0.0) amount_0 from (select *, if("#vp@TimeZone" is not 
    null and "#vp@TimeZone">=-12 and "#vp@TimeZone"<=14, date_add('second', cast((0-"#vp@TimeZone")*3600 as integer), 
    "#event_time"), "#event_time") "@vpc_tz_#event_time" from (select * , try_cast((try("time"-"time")) as double) as 
    "#vp@TimeZone" from ( v_event_15 ) logic_table)) ta_ev where ((( ( "$part_event" IN ( 's_connect_upgrade' ) ) )) 
    and (ta_ev."connect_level" > 4.2E+2)) and (("$part_date" between '2021-02-23' and '2021-03-25') and 
    ("@vpc_tz_#event_time" >= timestamp '2021-02-24' and "@vpc_tz_#event_time" < date_add('day', 1, TIMESTAMP 
    '2021-03-25'))) ) ) ORDER BY total_amount DESC limit 1000"""
    t1 = dt.now().strftime('%Y-%m-%d')
    sql = sql.replace('2021-03-25', t1)
    print(sql)
    data = get_tga_data(sql)
    return '最大战意连协等级: ' + str(int(data[0][1]))


# print(get_max_hero_level())
def get_all_stats():
    s = get_max_stage() + '\n' \
        + get_max_extreme_floor() + '\n' \
        + get_max_player_level() + '\n' \
        + get_max_hero_level()
    return s


if __name__ == '__main__':
    print(get_max_stage())
    print(get_max_extreme_floor())
    print(get_max_hero_level())
    print(get_max_player_level())

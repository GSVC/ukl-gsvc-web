# -*- coding: utf-8 -*-


# import mysql.connector
import json
from bson import json_util
import mysql.connector
from .SqlPack.SQLModel import qureResultAsJson
from .SqlPack.SqlLinkInfo import DataApiFuncSqlLink as Sql

Sql_Info = Sql['NewVsimTestInfo']['query']


def getJosonData(sysStr, Database, query_str):
    """==========================================
    sql查询接口函数
    :param sysStr:
    :param Database:
    :param query_str:
    :return:
    =============================================="""
    jsonResults = qureResultAsJson(sysStr=sysStr,
                                   Database=Database,
                                   query_str=query_str,
                                   where=[])
    return jsonResults


def get_new_vsim_info(person, country, imsi):
    """

    :param person:
    :param country:
    :param imsi:
    :return:
    """
    jsonResults = []
    query_person = person
    query_country = country
    query_imsi = imsi
    errInfo = ""
    country_str = " `country_iso`='" + query_country + "' "
    if query_person:
        person_str = " AND `person_test`= '" + query_person + "' "
    else:
        person_str = ""
    if query_imsi:
        imsi_str = " AND `imsi` LIKE " + "'" + query_imsi + "%' "
    else:
        imsi_str = ""
    try:
        query_str = (
            "SELECT  "
            "`id_newvsimtest` AS 'id_newvsimtest', "
            "`person_supplier`, "
            "`person_test`, "
            "`card_info`, "
            "(case when `vsim_type`=0 then '本国卡' else '多国卡' end) as 'vsim_type', "
            "`country_cn`, "
            "`country_iso`, "
            "`operator`, "
            "`plmn`, "
            "(CASE WHEN `rat`='4' THEN 'GSM' "
            "      WHEN `rat`='8' THEN 'WCDM' "
            "      WHEN `rat`='16' THEN 'LTE' "
            "      WHEN `rat`='12' THEN 'GSM/WCDMA' "
            "      WHEN `rat`='24' THEN 'WCDMA/LTE' "
            "      WHEN `rat`='28' THEN 'GSM/WCDMA/LTE' "
            " END) AS 'rat', "
            "`config_change`, "
            "`imsi`, "
            "`user_code`, "
            "`imei`, "
            "`device_type`, "
            "`success_time`, "
            "`change_time`, "
            "`register_operator`, "
            "`eplmn` as 'eplmn', "
            "(CASE WHEN `register_rat`='4' THEN 'GSM' "
            "      WHEN `register_rat`='8' THEN 'WCDM' "
            "      WHEN `register_rat`='16' THEN 'LTE' "
            "      WHEN `register_rat`='12' THEN 'GSM/WCDMA' "
            "      WHEN `register_rat`='24' THEN 'WCDMA/LTE' "
            "      WHEN `register_rat`='28' THEN 'GSM/WCDMA/LTE' "
            " END) AS 'register_rat', "
            "`lac`, "
            "`cellid`, "
            "(case when `service_usability` = 0 then '否' else '是' end) as 'service_usability', "
            "(CASE WHEN `stability_onehour` = 0 THEN '否' ELSE '是' END) AS 'stability_onehour', "
            "`agree_mbr`, "
            "(CASE WHEN `agree_consistency`= 0 then '否' else '是' end) as 'agree_consistency', "
            "`fail_reason`, "
            "`remark` as 'remark' "
            "FROM `vsim_test_info` as i "
            "WHERE " + country_str + person_str + imsi_str
        )
        #print query_str
        db = Sql_Info['db']
        database = Sql_Info['database']
        jsonResults = getJosonData(sysStr=db, Database=database, query_str=query_str)
    except KeyError as keyerr:
        errInfo = ("KeyError:{}".format(keyerr))
    except mysql.connector.Error as err:
        errInfo = ("Something went wrong: {}".format(err))
    if errInfo:
        DicResults = {'info': {'err': True, 'errinfo': errInfo}, 'data': []}

        return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)

    else:
        if not jsonResults:
            DicResults = {'info': {'err': True, 'errinfo': "No Query Data"}, 'data': []}

            return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
        else:
            DicResults = {'info': {'err': False, 'errinfo': errInfo}, 'data': jsonResults}

            return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)


def get_new_vsim_test_info(person, country, imsi):
    """

    :param person:
    :param country:
    :param imsi:
    :return:
    """

    newVsimTestInfo = get_new_vsim_info(person, country, imsi)

    return newVsimTestInfo

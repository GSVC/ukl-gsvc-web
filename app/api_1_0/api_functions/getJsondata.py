#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .SqlPack.SQLModel import qureResultAsJson





def getJosonData(sysStr, Database, query_str):


    jsonResults = qureResultAsJson(sysStr=sysStr,
                                   Database=Database,
                                   query_str=query_str,
                                   where=[])
    return jsonResults


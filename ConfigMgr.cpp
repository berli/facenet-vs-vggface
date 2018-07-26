/*************************************************************************
    > File Name: ConfigMgr.cpp
    > Author: libo
    > Created Time: Thu 12 Jul 2018 02:58:56 PM CST
 ************************************************************************/

#include "ConfigMgr.h"
#include "Config.h"
#include <boost/thread.hpp>

int ConfigMgr::getServant(vector<string>&avServant)
{
	TC_ThreadRLock Rlock(cServantLock);
	for(auto e:cMapServant)
		avServant.push_back(e.first);

	return 0;
}

void ConfigMgr::setServant(const string&asServant)
{
	TC_ThreadWLock Wlock(cServantLock);
	cMapServant[asServant] = ""; //预留
		
	cSignal.notify();
}

void ConfigMgr::init()
{
	boost::thread update(&ConfigMgr::updateThread, ConfigMgr::getInstance());

	getServant();
}

void ConfigMgr::updateThread()
{
	LOG_DEBUG<<"updateThread starting..."<<endl;

	while(true)
	{
		TC_Mysql lMysql;
    	lMysql.init(ConfigInit::getInstance()->getDBConf());
    
		{
			TC_ThreadRLock Rlock(cServantLock);
        	for(auto e: cMapServant)
        	{
        		insertServant(e.first);
        	}
		}

		cSignal.wait();
	}

}

int ConfigMgr::insertServant(const string&asServant)
{
	TC_Mysql lMysql;
	lMysql.init(ConfigInit::getInstance()->getDBConf());

	char lsSql[1024] = "";
	snprintf(lsSql, sizeof(lsSql), "insert into servant (name) values('%s')", asServant.c_str());
	LOG_DEBUG<<lsSql<<endl;

	try
	{
		lMysql.execute(lsSql);
	}
	catch(exception&e)
	{
		LOG_ERROR<<e.what()<<endl;
		return -1;
	}
	catch(...)
	{
		LOG_ERROR<<"unknow exception..."<<endl;
		return -2;
	}

	return 0;
}


taf::Int32 ConfigMgr::getServant()
{
	char lsTemp[10240] ="";

	try
	{
		TC_Mysql lMysql;
		lMysql.init(ConfigInit::getInstance()->getDBConf());
	
		LOG_DEBUG<<"init db"<<endl;
	
		TC_Mysql::MysqlData loData;
		snprintf(lsTemp, sizeof(lsTemp), "select name from servant");

		LOG_DEBUG<<"sql:"<<lsTemp<<endl;
		loData = lMysql.queryRecord(lsTemp);

		LOG_DEBUG<<"result size:"<<loData.size()<<endl;


		for(size_t i = 0; i < loData.size(); i++ )
		{
			LOG_DEBUG<<loData[i]["name"]<<endl;
		
			TC_ThreadWLock Wlock(cServantLock);
			cMapServant[ loData[i]["name"]] = ""; //预留
		}

		return 0;
	}
	catch(exception&e)
	{
		LOG_ERROR<<e.what()<<endl;
		return -1;
	}
	catch(...)
	{
		LOG_ERROR<<"unkonw exception"<<endl;
		return -2;
	}

	return 1;
}



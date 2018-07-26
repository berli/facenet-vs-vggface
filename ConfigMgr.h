/*************************************************************************
    > File Name: ConfigMgr.h
    > Author: libo
    > Created Time: Thu 12 Jul 2018 12:48:22 PM CST
 ************************************************************************/

#include<iostream>
#include "util/tc_singleton.h"
#include "util/tc_thread_rwlock.h"
#include "util/tc_mysql.h"
#include "Log.h"
#include "Semaphore.h"
#include<iostream>
#include<map>
using namespace taf;
using namespace std;

class ConfigMgr: public TC_Singleton<ConfigMgr, CreateUsingNew,  DefaultLifetime>
{
public:
	ConfigMgr()
	{
	}

	virtual ~ConfigMgr()
	{
	}

	int getServant(vector<string>&avServant);

	void setServant(const string&asServant);

	void init();

	void updateThread();
	
	taf::Int32 getServant();

	int insertServant(const string&asServant);

protected:

	TC_ThreadRWLocker  cServantLock;
	map<string,string> cMapServant;
	Semaphore          cSignal;
};


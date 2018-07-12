/*************************************************************************
    > File Name: Semphore.h
    > Author: berli
    > Mail: berli@tencent.com 
    > Created Time: 2018年07月12日 星期四 14时46分49秒
 ************************************************************************/
#include <semaphore.h>
#include<iostream>
using namespace std;

class Semaphore
{
public:
	Semaphore()
	{
		sem_init(&cSem, 0, 0);
	}

	~Semaphore()
	{
		sem_destory(&cSem);
	}

	void notify()
	{
		sem_post(&cSem);
	}

	void wait()
	{
		sem_wait(&cSem);
	}

protected:
	sem_t cSem;
};

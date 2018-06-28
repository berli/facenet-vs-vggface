/*************************************************************************
    > File Name: HttpClient.h
    > Author: berli
    > Mail: berli@tencent.com 
    > Created Time: Wed 12 Dec 2012 05:33:53 PM CST
 ************************************************************************/
#ifndef HTTP_CLIENT_H_2012_12_12
#define HTTP_CLIENT_H_2012_12_12

#include <iostream>
#include <string>

using namespace std;

#include "curl/curl.h"

class HttpClient
{

public:

    HttpClient();  
    virtual ~HttpClient();  


    static int InitHttp();

    int Post(const string&asURL, const string&asBody, string&asResponse, const bool&abXml=false);
    
	int Get(const string&asURL,  string&asResponse);

	int Put(const string&asUrl, const string&asParam, string&asResponse, const string&asMethod="PUT");

	int Upload(const string&asUrl, const string&asFile, string&asResponse, const string&asParam = "files");
   
	void SetHttpProxy(const string&asProxy);
   
	void SetHttpProxyPort(const size_t&aiProxyPort);

	void setHeader(const string&asHeader);

	void SetTimeout(const size_t&aiTimeout);

private:

    int InitHttp( const string& url, string &asResponse);

    static long Writer(void *data, int size, int nmemb, string &asResponse);

protected:

    CURL *cpCurl;
    char csError[1024];
    string csProxy;
    size_t ciPort;

	string csHeader;

	size_t ciTimeout;
};
#endif


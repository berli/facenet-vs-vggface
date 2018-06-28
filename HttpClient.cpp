/*************************************************************************
    > File Name: HttpClient.cpp
    > Author: berli
    > Mail: berli@tencent.com 
    > Created Time: Wed 12 Dec 2012 05:54:46 PM CST
 ************************************************************************/

#include "Log.h"
#include "HttpClient.h"

HttpClient::HttpClient(): ciPort(0)
{
    cpCurl = NULL;
	ciTimeout = 6000;
}

HttpClient::~HttpClient()
{
    curl_easy_cleanup(cpCurl);
}

int HttpClient::InitHttp()
{
    CURLcode code;

    code = curl_global_init(CURL_GLOBAL_ALL);
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to global init default, code:"<< code <<endl;
        return code;
    } 

    return 0;
}

void HttpClient::SetHttpProxy(const string&asProxy)
{
    csProxy.clear();
    csProxy = asProxy;
}
    
void HttpClient::SetHttpProxyPort(const size_t&aiProxyPort)
{
    ciPort = aiProxyPort;
}

void HttpClient::SetTimeout(const size_t&aiTimeout)
{
    ciTimeout = aiTimeout*1000;
}

void HttpClient::setHeader(const string&asHeader)
{
	csHeader = asHeader;
}

int HttpClient::InitHttp( const string& url, string &asResponse)
{
    
    CURLcode code;
    cpCurl = curl_easy_init();
    code = curl_easy_setopt(cpCurl, CURLOPT_ERRORBUFFER, csError);
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to set error buffer:"<< code <<endl;
        return code;
    }
    
    curl_easy_setopt(cpCurl, CURLOPT_VERBOSE, 1);
    code = curl_easy_setopt(cpCurl, CURLOPT_URL, url.c_str());
    if (code != CURLE_OK)
    {
        LOG_ERROR<<"Failed to set URL"<<csError<<endl;
        return code;
    }
    code = curl_easy_setopt(cpCurl, CURLOPT_FOLLOWLOCATION, 1);
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to set redirect option:"<< csError <<endl;
        return code;
    }
    code = curl_easy_setopt(cpCurl, CURLOPT_WRITEFUNCTION, HttpClient::Writer);
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to set writer:"<< csError<<endl;
        return code;
    }
    code = curl_easy_setopt(cpCurl, CURLOPT_WRITEDATA, &asResponse);
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to set write data:"<<  csError <<endl;
        return code;
    }
    code = curl_easy_setopt(cpCurl, CURLOPT_FORBID_REUSE, 0L); 
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to set write data:"<<  csError <<endl;
        return code;
    }
    code = curl_easy_setopt(cpCurl, CURLOPT_SSL_VERIFYPEER, false);//turn off curl's verification of the certificate 
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to :turn off curl's verification of the certificate"<<  csError <<endl;
        return code;
    }
    code = curl_easy_setopt(cpCurl, CURLOPT_DNS_USE_GLOBAL_CACHE, false );
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to CURLOPT_DNS_USE_GLOBAL_CACHE:"<<  csError <<endl;
        return code;
    }
    code = curl_easy_setopt(cpCurl, CURLOPT_NOSIGNAL, 1L);
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to CURLOPT_DNS_USE_GLOBAL_CACHE:"<<  csError <<endl;
        return code;
    }
    code = curl_easy_setopt(cpCurl, CURLOPT_TIMEOUT_MS, ciTimeout);//set timeout  
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to CURLOPT_TIMEOUT"<<  csError <<endl;
    
        return code;
    }
    if(csProxy.size() > 0 && ciPort > 0)
    {
        code = curl_easy_setopt(cpCurl, CURLOPT_PROXY, csProxy.c_str());//set proxy
        if (code != CURLE_OK)
        {
            LOG_ERROR<< "Failed to CURLOPT_PROXY"<<  csError <<endl;
        
            return code;
        }
        code = curl_easy_setopt(cpCurl, CURLOPT_PROXYPORT, ciPort);//set proxy port 
        if (code != CURLE_OK)
        {
            LOG_ERROR<< "Failed to CURLOPT_PROXYPORT"<<  csError <<endl;
        
            return code;
        }

    }
        
    struct curl_slist *headers=NULL;
	if( csHeader.size() > 0 )
	{
        headers = curl_slist_append(headers, csHeader.c_str());  
        curl_easy_setopt(cpCurl, CURLOPT_HTTPHEADER, headers);

        LOG_DEBUG<<"Add selfDefine Header..."<<endl;
	}

    return 0;
}
    
    
long HttpClient::Writer(void *data, int size, int nmemb, string &asResponse)
{
    long sizes = size * nmemb;
    //asResponse.clear();
    asResponse.append((char*)data, sizes); 

    return sizes;
}

int HttpClient::Post(const string&asURL, const string&asBody, string&asResponse, const bool&abXml)
{
    CURLcode code;

    if ( InitHttp(asURL, asResponse) !=0)
    {
        LOG_ERROR<< "Failed to global init default" <<endl;;
        return -1;
    }

    code = curl_easy_setopt(cpCurl, CURLOPT_POST, 1L); 
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to set write data:"<<  csError <<endl;
        return code;
    }
    code = curl_easy_setopt(cpCurl, CURLOPT_POSTFIELDS, asBody.c_str()); 
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to set write data:"<<  csError <<endl;
        return code;
    }
    code = curl_easy_setopt(cpCurl, CURLOPT_POSTFIELDSIZE, asBody.size()); 
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to set write data:"<<  csError <<endl;
        return code;
    }
    long retcode = 0;
    double length = 0;
    retcode = curl_easy_getinfo(cpCurl, CURLINFO_CONTENT_LENGTH_DOWNLOAD , &length); 
        
    struct curl_slist *headers=NULL;
    if( abXml )
    {
       
        headers = curl_slist_append(headers, "Content-Type: text/xml; charset=utf-8\nSOAPAction:");  
        //headers = curl_slist_append(NULL, "Content-Type: text/xml; charset=utf-8");  
        //headers = curl_slist_append(headers, "SOAPAction:");  
        
        curl_easy_setopt(cpCurl, CURLOPT_HTTPHEADER, headers);

        LOG_DEBUG<<"Add SOAPAction Header..."<<endl;
    }

    code = curl_easy_perform(cpCurl);
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to get url:"<< asURL<<"error:"<<csError<<endl;
        curl_slist_free_all(headers);
   
        return code;
    }
        
    curl_slist_free_all(headers);

    code = curl_easy_getinfo(cpCurl, CURLINFO_RESPONSE_CODE , &retcode); 
    if ( (code == CURLE_OK) && retcode == 200 )
    {
        LOG_WARN<<"Succ, Expected body length:"<<length<<" actual length:"<<asResponse.size()<< endl;
        return 0;
    }
    else
    {
        LOG_ERROR<<"http return code:"<<retcode<<" Expected body length:"<<length<<" actual length:"<<asResponse.size()<< endl;

        return code;
    }

    return -1;
    

}

int HttpClient::Get(const string&asURL, string&asResponse)
{
    CURLcode code;

    if ( InitHttp(asURL,  asResponse) !=0)
    {
        LOG_ERROR<< "Failed to global init default" <<endl;;
        return -1;
    }
    code = curl_easy_perform(cpCurl);
    if (code != CURLE_OK)
    {
        LOG_ERROR<< "Failed to get url:"<< asURL<<"error:"<<csError<<endl;
        return -1;
    }
    long retcode = 0;
    code = curl_easy_getinfo(cpCurl, CURLINFO_RESPONSE_CODE , &retcode); 
    if ( (code == CURLE_OK) && retcode == 200 )
    {
        return 0;
    }
    else
    {
        //LOG_ERROR<<getStatusCode(retcode)<<endl;
        return -1;
    }

    return -1;

}
	
int HttpClient::Upload(const string&asUrl, const string&asFile, string&asResponse, const string&asParam)
{
    if ( InitHttp(asUrl,  asResponse) !=0)
    {
        LOG_ERROR<< "Failed to global init default" <<endl;;
        return -1;
    }

	if( access(asFile.c_str(), R_OK) != 0 )
	{
		LOG_ERROR<<"read "<<asFile<<" failed!"<<endl;
		return -2;
	}

	struct curl_httppost *formpost = 0;
	struct curl_httppost *lastptr  = 0;

	curl_formadd(&formpost, &lastptr, CURLFORM_PTRNAME, "reqformat", CURLFORM_PTRCONTENTS, "plain", CURLFORM_END);
	curl_formadd(&formpost, &lastptr, CURLFORM_PTRNAME, asParam.c_str(), CURLFORM_FILE, asFile.c_str(), CURLFORM_END);
	curl_easy_setopt(cpCurl, CURLOPT_HTTPPOST, formpost);

	int liRet = curl_easy_perform(cpCurl);

	return liRet;
}

int HttpClient::Put(const string&asUrl, const string&asParam, string&asResponse, const string&asMethod)
{
    if ( InitHttp(asUrl,  asResponse) !=0)
    {
        LOG_ERROR<< "Failed to global init default" <<endl;;
        return -1;
    }

	curl_easy_setopt(cpCurl, CURLOPT_CUSTOMREQUEST, asMethod.c_str()); 
	
	curl_easy_setopt(cpCurl, CURLOPT_POSTFIELDS, asParam.c_str()); 

	int liRet = curl_easy_perform(cpCurl);

	return liRet;
}


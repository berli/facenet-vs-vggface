#include <iostream>  
using namespace std;  
  
class Test    
{    
    public:    
        Test(int a)  
        {  
            Test::a = a;  
        }  
    friend Test operator+ (Test&,int);  
    friend int operator+ (int, Test&);  
    public:  
        int a;  
};

int operator + (int a, Test&temp)
{  
    return (a + temp.a);  
}

Test operator + (Test &temp1,int temp2)  
{  
    Test result(temp1.a + temp2);  
    return result;  
}  

int main()  
{  

  Test a(100);  
    a = a + 10;//正确  
    cout<<a.a<<endl;  

    a = 10 + a;//OK
    cout<<a.a<<endl;  
    //system("pause");  
}


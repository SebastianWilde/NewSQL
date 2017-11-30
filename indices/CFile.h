#ifndef CFILE_H
#define CFILE_H

#include <iostream>
#include <fstream>
// #include <thread>
#include <vector>
#include <stdio.h>
#include <string>
#include <algorithm>    // std::remove_if
using namespace std;
typedef string T;
// typedef unsigned long T;
string space(int n)
{
    string aux="";
    for (int i= 0;i<n;i++)
    {
        aux+=" ";
    }
    return aux;
}

vector<int> str_find(string cad,string fin)
{
    vector<int> fi;
    int pos = cad.find(fin);
    while (pos != -1)
    {
        pos = cad.find(fin,pos+1);
        fi.push_back(pos);
    }
    fi.push_back(pos);
    return fi;

}

class CFile{
public:
    // vector<thread> m_threads;
    vector<string> m_vector ;
    vector<string> m_vector2 ;
    // vector<string> zeros;
    // int n;
    // T m_part;
    // T N;
    int n_bytes;
    int len_col;
    string name_file;
    CFile(string);
    void save_file();
    void generate_file();
    void fill_file(int);
    void write(string);
    void _delete(string);
    void update(string,string,int);
    int number_bytes();
    string read_file_p(unsigned long int);
    vector<T> read_file(int); 
};

CFile::CFile(string n_file)
{
    name_file = n_file +".csv";
    // N=20;
    // n = 4;
    // m_vector.resize(N) ;
    // m_vector2.resize(N) ;
    // zeros = {"0000","000","00","0",""};
    // m_part=N/n;

}

void CFile::update(string update,string data,int col)
{
    data = data + space(len_col-data.size());
    update = update + space(len_col-update.size());
    string line;
    ifstream fin;
    fin.open(name_file.c_str());
    ofstream temp;
    temp.open("temp.csv");
    int pos;
    if(col==1)
        pos = (col-1)*len_col;
    else
        pos = ((col-1)*len_col)+col-1;
        
    while(getline(fin,line))
    {
        //vector<int> finds = str_find(line,update);
        //if(find(finds.begin(), finds.end(), pos) != finds.end())
        if(line.find(update)==pos)
            line.replace(pos,len_col,data);
        temp << line <<endl;
    }
    temp.close();
    fin.close();
    remove(name_file.c_str());
    rename("temp.csv",name_file.c_str());
}

void CFile::_delete(string data)
{
    data = data + space(len_col-data.size());
    string line;
    ifstream fin;
    fin.open(name_file.c_str());
    ofstream temp;
    temp.open("temp.csv");
    while(getline(fin,line))
    {
        if (line.find(data)!=-1)
            line = space(line.size());
        //line.replace(line.find(data),data.length(),"");
        temp << line <<endl;
    }
    temp.close();
    fin.close();
    remove(name_file.c_str());
    rename("temp.csv",name_file.c_str());
}

void CFile::write(string data)
{
    FILE * pFile;
    pFile = fopen (name_file.c_str(),"a");
    if (pFile!=NULL)
    {
        fputs (data.c_str(),pFile);
        fclose (pFile);
    }
}

void CFile::save_file()
{
    // ofstream file("numbers.txt") ;
    // for(T i=0; i<N ;i++){
    //     file << m_vector[i]<<" ";
    //     file << m_vector2[i]<< "\n";
    // }
    // file.close();
}

void CFile::fill_file(int n_thread){
    // T size=0,i,j;
    // for(i=m_part*n_thread,j=N-i-1;i<m_part*(n_thread+1);i++,j--){
    //     m_vector[i]=to_string(i);
    //     size=m_vector[i].size();
    //     m_vector[i].insert(0,zeros[size-1]);   
    //     m_vector2[i]=to_string(j);
    //     size=m_vector2[i].size();
    //     m_vector2[i].insert(0,zeros[size-1]);   
    // }
}

void CFile::generate_file(){
    //cout<<N<<endl;
    // for (int i=0; i < n ; i++)
    // m_threads.push_back(thread(&CFile::fill_file,this,i));

    // for (int i=0; i < n ; i++)
    // m_threads[i].join();
    // save_file();
}

string CFile::read_file_p(unsigned long int pos)
{
    string data;
    FILE* ptr_file = fopen(name_file.c_str(),"r");
    fseek(ptr_file,pos,SEEK_SET);
    for (int i=0;i<n_bytes-1;i++)
        data+=getc(ptr_file);
    //int pos=ftell(ptr_file);
    fclose(ptr_file);
    return data;
}
int CFile::number_bytes()
{
    string line;
    cout<<"line:"<<line<<endl;
    ifstream is_file(name_file.c_str());
    getline (is_file,line);
    n_bytes=line.size()+1;
    is_file.close();
    // len_col=(n_bytes/4)-1;
    len_col=17;
    return n_bytes;
}

vector<T> CFile::read_file(int col )
{
    string line;
    vector<T> rpta;
    ifstream is_file(name_file.c_str());
    getline (is_file,line);
    while ( getline (is_file,line))
    {
        if(col==1)
            line=line.substr((col-1)*len_col,len_col);
        else
            line=line.substr(((col-1)*len_col)+col-1,len_col);
        
        line.erase(remove(line.begin(), line.end(),' '), line.end());       
        rpta.push_back(line);
    }
    is_file.close(); 
    return rpta;
}

#endif //CFILE

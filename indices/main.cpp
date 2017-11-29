/*
 g++ main.cpp -o sgbd
./sgbd i 
*/

#include "AvlTree.h"
#include "CFile.h"

#include <iostream>
#include <vector>
#include <time.h>
#include <stdio.h>
#include <string.h>

using namespace std;

typedef string t;
typedef unsigned long int N;
int n_bytes = 0;
int n_columna = 17;
template <class T>
struct Lless
{
	bool operator()(T a, T b)
	{
		return a < b;
	}
};

string space(int n)
{
	string aux="";
	for (int i= 0;i<n;i++)
	{
		aux+=" ";
	}
	return aux;
}

struct Trait
{
	typedef t T;
	typedef Lless<T> C;
};


int main(int argc, char* argv[])
{
	cout<<space(5);
	t data;
	int col;
	// string data;
	AvlTree<Trait> avltree;
	//CFile cfile;
	char op='1';
	clock_t t1 ,t2;

   	if (argc != 4)
   	{
		cout<<"Mal ingreso"<<endl;
		cout<<argv[0]<< " [g] [file_name]"<<endl ;
		cout<<argv[0]<< " [i] [col] [file_name]"<<endl;
		return 0;
	}

	/*
	if(*argv[1]=='g' ){
		cfile.generate_file();
		cout<<"generado"<<endl;
		return 0;
	}
	*/
	if(*argv[1]=='i'){
		col=int(strtol(argv[2], NULL, 10));
		string nombre_archivo = argv[3];
		cout<<"Trabajando sobre: "<<nombre_archivo<<endl;
		CFile cfile(nombre_archivo);

		/* INSERT */
		n_bytes=cfile.number_bytes();
		cout<<"n_bytes: "<<n_bytes<<endl;
		vector<T> m_vector = cfile.read_file(col);
		N i,j;
		for (i=0, j=n_bytes; i<m_vector.size();i++,j+=n_bytes)
			avltree.insert(m_vector[i],j);
			// avltree.insert(stol(m_vector[i]),j);
		
		/* PRINT */
		cout<<"save index\n";
		avltree.printLe2(avltree.root);	
		cout<<endl;
		
		/* FIND */
		char opcion;
		string menu = "f)find data\ni)insert data\nd)delete data\ne)exit\n";
		cout<<menu;
		cin>>opcion;
		while(opcion!='e')
		{
			if (opcion=='f')
			{
				cout<<"data: ";
				cin.ignore(); 
				getline(cin,data);
				cout<<data<<" se encuentra: "<<endl;
				vector<N> tmp;
				/* t1 */
				t1 = clock();
				if(avltree.find2(data,tmp)==false)
				{
					t1 = clock() - t1;
					cout<<"error no encontrado\n"; 
					return 0;
				}
		
				/* t2 */
				int i=0;
				t2 = clock();
				for(i=0;i<tmp.size();i++)
				{
					cout<<cfile.read_file_p(tmp[i])<<endl;
				}
				//cout<<tmp.front()<<" contiene: "<<cfile.read_file_p(tmp.front())<<endl;
				//cout<<tmp.front()<<" contiene: "<<cfile.read_file_p(tmp.front())<<endl;
				t2 = clock()-t2;			
				cout<<"tiempo get list: "<<((float)t1)/CLOCKS_PER_SEC<<endl;
				cout<<"tiempo busqueda en list : "<<((float)t2)/CLOCKS_PER_SEC<<endl;

			}
			else if (opcion=='i')
			{
				string id, nombre,apellido,edad,profesion,new_line;
				cout<<"id: ";
				cin>>id;
				cout<<"nombre: ";
				cin>>nombre;
				cout<<"apellido: ";
				cin>>apellido;
				cout<<"edad: ";
				cin>>edad;
				cout<<"profesion: ";
				cin>>profesion;
				new_line = id + space(n_columna-id.size())
							+","+nombre+space(n_columna-nombre.size())
							+","+apellido+space(n_columna-apellido.size())
							+","+edad+space(n_columna-edad.size())
							+","+profesion+space(n_columna-profesion.size())+" \n";
				cfile.write(new_line);
				cout<<"Insertando... "<<new_line<<endl;
				string insert = "";
				if (col==1) insert = id;
				else if(col==2) insert = nombre;
				else if (col==3) insert = apellido;
				else if (col==4) insert = edad;
				else insert = profesion;
				avltree.insert(insert,j);
				j+=n_bytes;
				cout<<"\nsave index\n";
				avltree.printLe2(avltree.root);
			}
			/*else if (opcion =='d')
			{
				string campo;
				cout<<"Borrar: ";
				cin>>campo;
				avltree.de

			}*/
			cout<<menu;
			cin>>opcion;
		}
	}

	return 0;
}

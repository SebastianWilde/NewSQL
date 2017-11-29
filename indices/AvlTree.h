#ifndef AVLTREE_H
#define AVLTREE_H

#include <iostream>
#include <vector>
#include <stack>
#include <queue>
#include <fstream>

using namespace std;
typedef unsigned long int N;

template <class T>
class CNode
{
	public:
	T m_data;
	// N m_dirr;
	vector<N> m_dirr;
	CNode<T>* m_nodes[2];
	int height;
	int factor;
	CNode(T _m_data)
	{
		this->m_data = _m_data;
		m_nodes[0]=m_nodes[1]=nullptr;
		height=1;
		factor=0;
	}
};

template <class Tr>
class AvlTree
{
	public:
	AvlTree();
	typedef typename Tr::T T;
	typedef typename Tr::C C;
	
	void add(T,N);
	void printIn(CNode<T>*); 	
	void printLe(CNode<T>*);
	void printLe2(CNode<T>*);
	bool find_node(T,CNode<T>**&);
	bool find(T,N&);
	bool find2(T,vector<N>&);
	bool insert(T,N);
	bool remove(T);
	
	CNode<T>* root;
	C cmp;
	stack <CNode<T>**> pila_balanceo;
	string file="tree.txt";
	
	void balance();
	void height(CNode<T>*&);
	void R(CNode<T>*&);
	void L(CNode<T>*&);
	void RR(CNode<T>**&);
	void LL(CNode<T>**&);
	void LR(CNode<T>**&);
	void RL(CNode<T>**&);

};

template <class Tr>
AvlTree<Tr>::AvlTree()
{
	root= NULL;
}

template <class Tr>
void AvlTree<Tr>::add(T x,N y)
{
	CNode<T>* tmp=root;
	if(!root)
		root= new CNode<T>(x,y);
	else
	{
		while(tmp->m_nodes[cmp(x,tmp->m_data)])
			tmp=tmp->m_nodes[cmp(x,tmp->m_data)];
		tmp->m_nodes[cmp(x,tmp->m_data)]= new CNode<T>(x,y);	
	}
}

template <class Tr>
void AvlTree<Tr>::printIn(CNode<T>* tmp)
{
	if(tmp->m_nodes[0])printIn(tmp->m_nodes[0]);
		cout<<tmp->m_data<<" "<<tmp->m_dirr<<endl;
	if(tmp->m_nodes[1])printIn(tmp->m_nodes[1]);
}

template <class Tr>
void AvlTree<Tr>::printLe(CNode<T>* tmp)
{
	ofstream os_file(file);
 	queue<CNode<T>*> m_queue;
    m_queue.push(tmp);
	string line;
	while (!m_queue.empty())
	{
        CNode<T> * tmp = m_queue.front();
        m_queue.pop();
        line=(tmp->m_data)+" "+to_string(tmp->m_dirr)+"\n";
		cout<<line;
        os_file<<line;
		if (tmp->m_nodes[1]) 
            m_queue.push(tmp->m_nodes[1]);
        if (tmp->m_nodes[0])
            m_queue.push(tmp->m_nodes[0]);
    }
	os_file.close();
}

template <class Tr>
void AvlTree<Tr>::printLe2(CNode<T>* tmp)
{    
	ofstream os_file(file) ;
 	queue<CNode<T>*> m_queue;
    m_queue.push(tmp);
	string line,aux;
	while (!m_queue.empty())
	{
        aux="";
        CNode<T> * tmp = m_queue.front();
        m_queue.pop();
		line=(tmp->m_data)+" ";
		for(int i=0;i<tmp->m_dirr.size();i++)
			aux+=to_string(tmp->m_dirr[i])+" ";
        line+=aux+"\n";
		// cout<<line;
        os_file<<line;
		if (tmp->m_nodes[1]) 
            m_queue.push(tmp->m_nodes[1]);
        if (tmp->m_nodes[0])
            m_queue.push(tmp->m_nodes[0]);
    }
	os_file.close();
}
template <class Tr>
bool AvlTree<Tr>::find_node(T x, CNode<T>** &tmp)
{
	for(tmp=&root; *tmp and (*tmp)->m_data != x; tmp=&((*tmp)->m_nodes[cmp(x ,(*tmp)->m_data)])) 
		pila_balanceo.push(tmp);
	return *tmp!=0;
}

template <class Tr>
bool AvlTree<Tr>::find(T x, N & data)
{
	CNode<T>** tmp=nullptr;
	if(!find_node_(x,tmp)) return false;
	data=(*tmp)->m_dirr;
	return true; 
}

template <class Tr>
bool AvlTree<Tr>::find2(T x, vector<N> & data)
{
	CNode<T>** tmp=nullptr;
	if(!find_node(x,tmp)) return false;
	data=(*tmp)->m_dirr;
	return true; 
}

template <class Tr>
bool AvlTree<Tr>::insert(T x, N y)
{
	stack<CNode<T>**> clear;
	pila_balanceo=clear;
	CNode<T>**tmp;
	if(find_node(x,tmp)) 
	{
		(*tmp)->m_dirr.push_back(y);
		return 0;
	}
		// CNode<T>* newCNode= new CNode<T>(x, yy);
	CNode<T>* newCNode= new CNode<T>(x);
	newCNode->m_dirr.push_back(y);
	*tmp= newCNode;
	if(!pila_balanceo.empty()) 
		balance();
	return 1;
}

template <class Tr>
bool AvlTree<Tr>::remove(T x)
{
	stack<CNode<T>**> clear;
	pila_balanceo=clear;
	CNode<T>**tmp;
	CNode<T>*delete_node;
	if(!find_node(x,tmp)) 
		return 0;
	delete_node=(*tmp);
	if((*tmp)->m_nodes[0] and (*tmp)->m_nodes[1])
	{
		CNode<T>**q=NULL;
		tmp=&((*tmp)->m_nodes[0]);
		while((*tmp)->m_nodes[1])
			tmp=&((*tmp)->m_nodes[1]);
		q=tmp;
		swap((*q)->m_data,(delete_node)->m_data);
		tmp=q;
	}
	CNode<T>* delCNode= *tmp;
	*tmp= (*tmp)->m_nodes[(*tmp)->m_nodes[1]!=0];
	delete delCNode;
	if(!pila_balanceo.empty()) 
		balance();
	return 1;
}

template <class Tr>
void AvlTree<Tr>::height(CNode<T>*&tmp)
{
	int factor;
	int	h_izq = 0; int h_der = 0;
	CNode<T>*ptr_der = tmp->m_nodes[1];
	CNode<T>*ptr_izq = tmp->m_nodes[0];
	while (ptr_der)
	{
		h_der++;
		if (ptr_der->m_nodes[1]) ptr_der = ptr_der->m_nodes[1];
		else if (ptr_der->m_nodes[0])	ptr_der = ptr_der->m_nodes[0];
		else ptr_der = NULL;
	}
	while (ptr_izq){
		h_izq++;
		if (ptr_izq->m_nodes[0])	ptr_izq = ptr_izq->m_nodes[0];
		else if (ptr_izq->m_nodes[1])	ptr_izq = ptr_izq->m_nodes[1];
		else ptr_izq = NULL;
	}
	factor = h_der - h_izq;
	tmp->factor = factor;
}

template <class Tr>
void AvlTree<Tr>::L(CNode<T>*&tmp)
{	
	CNode<T>*raiz,*h_izq,*h_der,*n_izq,*n_der;
	raiz = tmp->m_nodes[1];	
	h_der = tmp->m_nodes[1]->m_nodes[1];	
	h_izq = tmp;	
	n_der = tmp->m_nodes[1]->m_nodes[0];	
	n_izq = tmp->m_nodes[0];		

	tmp = raiz;
	tmp->m_nodes[1] = h_der;
	tmp->m_nodes[0] = h_izq;
	tmp->m_nodes[0]->m_nodes[1] = n_der;
	tmp->m_nodes[0]->m_nodes[0] = n_izq;
}

template <class Tr>
void AvlTree<Tr>::R(CNode<T>*&tmp)
{
	CNode<T>*raiz,*h_izq,*h_der,*n_izq,*n_der;
	raiz = tmp->m_nodes[0];
	h_izq = tmp->m_nodes[0]->m_nodes[0];
	h_der = tmp;
	n_izq = tmp->m_nodes[0]->m_nodes[1];
	n_der = tmp->m_nodes[1];

	tmp = raiz;
	tmp->m_nodes[1] = h_der;
	tmp->m_nodes[0] = h_izq;
	tmp->m_nodes[1]->m_nodes[1] = n_der;
	tmp->m_nodes[1]->m_nodes[0] = n_izq;
}

template <class Tr>
void AvlTree<Tr>::LR(CNode<T>**&tmp)
{
	L((*tmp)->m_nodes[0]);
	R(*tmp);
}

template <class Tr>
void AvlTree<Tr>::RL(CNode<T>**&tmp)
{
	R((*tmp)->m_nodes[1]);
	L(*tmp);
}

template <class Tr>
void AvlTree<Tr>::RR(CNode<T>**&tmp)
{
	R(*tmp);
}

template <class Tr>
void AvlTree<Tr>::LL(CNode<T>**&tmp)
{
	L(*tmp);
}

template <class Tr>
void AvlTree<Tr>::balance()
{
	while (!pila_balanceo.empty()){
		height((*pila_balanceo.top()));
		if ((*pila_balanceo.top())->factor == (-2) or (*pila_balanceo.top())->factor == (2))
		{
			if ((*pila_balanceo.top())->factor == -2)
			{
				if ((*pila_balanceo.top())->m_nodes[0]->factor == 1)
					LR((pila_balanceo.top())),height((*pila_balanceo.top()));
				else
					RR((pila_balanceo.top())),height((*pila_balanceo.top()));
			}
			else if ((*pila_balanceo.top())->factor == 2)
			{  
				if ((*pila_balanceo.top())->m_nodes[1]->factor == -1)
					RL((pila_balanceo.top())),height((*pila_balanceo.top()));
				else 
					LL((pila_balanceo.top())),height((*pila_balanceo.top()));
			}
		}
		pila_balanceo.pop();
	}
}

#endif //AvlTree_H

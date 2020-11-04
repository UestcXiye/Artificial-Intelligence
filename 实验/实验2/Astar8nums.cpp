#include<bits/stdc++.h>
using namespace std;

int open_cnt=0;
int close_cnt=0;
int noresoult=0;
int open_node_cnt;  //open表节点个数 

struct Node
{
	int a[3][3];
	int x,y;
	int f,g,h;
	int flag;  //上一次移动方向 
	Node *father;
}start,End;

struct Open_Close
{
	int f;
	Node *np;
}open[10000],close[10000];

//判断是否有解：逆序数之和奇偶性相同，有解
bool isable()
{
	int s[9],e[9];
	int tf=0,ef=0,k=0;
	for(int i=0;i<3;i++)
	{
		for(int j=0;j<3;j++)
		{
			s[k]=start.a[i][j];
		    e[k]=End.a[i][j];
			k++;
		}
	}
	for(int i=0;i<9;i++)
	{
		for(int j=0;j<i;j++)
		{
			if (s[i]>s[j] && s[j]!=0) tf+=1;
			if (e[i]>e[j] && e[j]!=0) ef+=1;
		}
	}
	if((tf%2 == 1 && ef%2 == 1) || (tf%2 == 0 && ef%2 == 0)) return true;
	else return false;
}

//求h(n)
int a_start_h(Node *node)
{   
	int old_x,old_y,End_x,End_y;
	int h=0;
	for(int k=1;k<9;k++)
	{
		for(int i=0;i<3;i++)
		{
			for(int j=0;j<3;j++)
			{
				if(node->a[i][j] == k)  //相应开始点的下标
				{
					old_x=i;
					old_y=j;
				}
				if(End.a[i][j] == k)  //相应目标的结点下标
				{
					End_x=i;
					End_y=j;
				}
			}
		}
		//计算h(n)
		h+=abs(old_x-End_x)+abs(old_y-End_y);
	}
	return h;
}

//输入 
void input() 
{
	cout<<"请输入起始图："<<endl;
	for(int i=0;i<3;i++)
	{
		for(int j=0;j<3;j++)
		{
			cin>>start.a[i][j];
			if(start.a[i][j] == 0)
			{
				start.x=i;
				start.y=j;
			}
		}
	}
	cout<<endl;
	cout<<"请输入目标图："<<endl;
	for(int i=0;i<3;i++)
	{
		for(int j=0;j<3;j++)
		{
			cin>>End.a[i][j];
			if(End.a[i][j] == 0)
			{
				End.x=i;
				End.y=j;
			}
		}
	}
	cout<<endl;
	
	start.g=0;
	start.h=a_start_h(&start);
	start.f=start.g+start.h;
}

//打印过程
int print(Node *node)
{
	Node *p=node;
	if(p == &start) return 1;
	else print(p->father);
	cout<<"---------\n";
	
	for(int i=0;i<3;i++)
	{
		for(int j=0;j<3;j++)
		{
			cout<<p->a[i][j]<<" ";
		}
		printf("\n");
	}
	cout<<"---------\n\n";
}

//判断是否为目标节点 
bool isend(Node *node)
{         
	for(int i=0;i<3;i++)
	{
		for(int j=0;j<3;j++)
		{
			if(node->a[i][j]!=End.a[i][j]) return false;
		}
	}
	return true;
}

//open表排序
void sort(Open_Close *open)
{       
	int min=99999,min_flag=0;
	Open_Close temp;
	for(int i=0;i<=open_cnt;i++)
	{      
		if(min>open[i].f && open[i].f>0)
		{
			min=open[i].f;
			min_flag=i;
		}
	}
	temp=open[min_flag];            
	open[min_flag]=open[0];
	open[0]=temp;
}

//向四个方向扩展
void move(int flag,Node *node)
{    
	int temp;
	//左移 
	if(flag == 1 && node->x>0)
	{
		Node *n=new Node();
		for(int i=0;i<3;i++)
		{
			for(int j=0;j<3;j++)
			{
				n->a[i][j]=node->a[i][j];
			}
		}
		n->a[node->x][node->y]=node->a[node->x-1][node->y];
		n->a[node->x-1][node->y]=0;
		n->x=node->x-1;
		n->y=node->y;
		n->flag=3;
		n->father=node;
		//求 g(n)
		n->g=node->g+1; 
		
		n->h=a_start_h(n);
		//求 f(n)
		n->f=n->g+n->h; 
		
		open_cnt++;
		open_node_cnt++;
		//添加到open表
		open[open_cnt].np=n;        
		open[open_cnt].f=n->f;  
	}
	//上移 
	else if(flag == 2 && node->y<2)
	{
		Node *n=new Node();
		for(int i=0;i<3;i++)
		{
			for(int j=0;j<3;j++)
			{
				n->a[i][j]=node->a[i][j];
			}
		}
		n->a[node->x][node->y]=node->a[node->x][node->y+1];
		n->a[node->x][node->y+1]=0;
		n->x=node->x;
		n->y=node->y + 1;
		n->flag=4;
		n->father=node;
		//求 g(n)
		n->g=node->g+1;
		
		n->h=a_start_h(n);
		//求 f(n)
		n->f=n->g+n->h;
		
		open_cnt++;
		open_node_cnt++;
		//添加到open表
		open[open_cnt].np=n;
		open[open_cnt].f=n->f;   
	}
	//右移 
	else if(flag == 3 && node->x<2)
	{
		Node *n=new Node();
		for(int i=0;i<3;i++)
		{
			for(int j=0;j<3;j++)
			{
				n->a[i][j]=node->a[i][j];
			}
		}
		n->a[node->x][node->y]=node->a[node->x+1][node->y];
		n->a[node->x+1][node->y]=0;
		n->x=node->x + 1;
		n->y=node->y;
		n->flag=1;
		n->father=node;
		//求 g(n)
		n->g=node->g + 1; 
		             
		n->h=a_start_h(n);
		//求 f(n)
		n->f=n->g+n->h;
		
		open_cnt++;
		open_node_cnt++;
		//添加到open表
		open[open_cnt].np=n;        
		open[open_cnt].f=n->f;   
	}
	//下移 
	else if(flag == 4 && node->y>0)
	{
		Node *n=new Node();
		for(int i=0;i<3;i++)
		{
			for(int j=0; j<3; j++)
			{
				n->a[i][j]=node->a[i][j];
			}
		}
		n->a[node->x][node->y]=node->a[node->x][node->y-1];
		n->a[node->x][node->y-1]=0;
		n->x=node->x;
		n->y=node->y-1;
		n->flag=2;
		n->father=node;
		//求 g(n)
		n->g=node->g+1; 
		             
		n->h=a_start_h(n);
		//求f(n)
		n->f=n->g+n->h;
		
		open_cnt++;
		open_node_cnt++;
		//添加到open表
		open[open_cnt].np=n;
		open[open_cnt].f=n->f;  
	}
}

//节点扩展
void expand(Node *node)
{       
	for(int i=1;i<5;i++)
	{
		if(i!=node->flag) move(i,node);
	}
}


int main()
{
	input();
	//start放入open表
	open[0].np=&start;			
	open_node_cnt=1;
	if(isable())
	{
		while(true)
		{
			//open表不为空 
			if(isend(open[0].np))
			{
				cout<<"\n移动过程：\n";
				//打印过程 
				print(open[0].np);
				//输出移动步数 
				cout<<"该问题有解，一共用了"<<open[0].np->g<<"步"<<endl;
				break;
			}
			//扩展最优节点的子节点
			expand(open[0].np);
			open[0].np=NULL;
			open[0].f=-1;
			open_node_cnt--;
			//open表排序
			sort(open);
		}
	}
	else cout<<"该问题无解";

	return(0);
}

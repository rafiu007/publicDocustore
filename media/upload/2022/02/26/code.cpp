#include <bits/stdc++.h>

using namespace std;
	queue<int> q1, q2;

	int curr_size=0;


	void push(int x)
	{
		curr_size++;
		q2.push(x);

		while (!q1.empty()) {
			q2.push(q1.front());
			q1.pop();
		}
		queue<int> q = q1;
		q1 = q2;
		q2 = q;
	}

	void pop()
	{

		// if no elements are there in q1
		if (q1.empty())
			return;
		q1.pop();
		curr_size--;
	}

	int top()
	{
		if (q1.empty())
			return -1;
		return q1.front();
	}

	bool isEmpty()
	{
		return curr_size==0;
	}


// Driver code
int main()
{
	
  cout<<"hello"<<endl;
  
	push(1);
	push(2);
	push(3);

	cout << isEmpty()
		<< endl;
	cout << top() << endl;
	pop();
	cout << top() << endl;
	pop();
	cout << top() << endl;
  
  push(5);
  push(6);
  
  cout<< top()<<endl;

	cout << isEmpty()<< endl;
	return 0;
}




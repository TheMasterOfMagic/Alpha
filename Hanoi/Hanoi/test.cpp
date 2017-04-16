#include <math.h>
#include <stack>
#include <iostream>
using namespace std;

typedef stack<int> Column;
Column columns[3];
Column invert(Column c) {
	Column temp;
	while (!c.empty()) {
		temp.push(c.top());
		c.pop();
	}
	return temp;
}
void f(int id, int n,int&plate, int& from, int& to) {
	int T = id - (id&(id - 1));
	int k = id / T / 2;
	plate = (int)log2(T)+1;
	from = (plate + n) % 2 ? k % 3 + 1 : 3 - (k + 2) % 3;
	to = (plate + n) % 2 ? (k + 1) % 3 + 1 : 3 - k % 3;
}
void move(Column& from,Column& to) {
	to.push(from.top());
	from.pop();
}
void showColumns() {
	Column temp;
	for (int i = 0; i < 3; ++i) {
		temp = invert(columns[i]);
		cout << "柱" << i + 1 << ":";
		while (!temp.empty()) {
			cout << temp.top() << ' ';
			temp.pop();
		}
		cout << endl;
	}
}
void Hanoi(int mount) {
	const int totalSteps = pow(2, mount) - 1;
	int plate,from, to;
	showColumns();
	for (int id = 1; id <= totalSteps; ++id) {
		f(id, mount, plate,from, to);
		cout << "第" << id << "步，将盘" << plate << "从柱" << from << "移到柱" << to << endl;
		move(columns[from-1], columns[to-1]);
		showColumns();
	}
}
int main() {
	Column& column1 = columns[0];
	Column& column2 = columns[1];
	Column& column3 = columns[2];
	int n;
	while (1) {
		column1 = Column();
		column2 = Column();
		column3 = Column();
		cin >> n;
		for (int i = n; i >= 1; --i) column1.push(i);
		system("cls");
		Hanoi(n);
		
	}
}
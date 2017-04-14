#include <iostream>
using namespace std;

void move(int from, int to) {
	cout << from << " -> " << to << endl;
}
void Hanoi(int mount) {
	const int totalSteps = pow(2, mount) - 1;
	int id, from, to,times;
	for (int i = 1; i <= totalSteps; ++i) {
		id = i;
		for (times = 1; (id / times + 1) % 2; times *= 2);
		cout << id << '\t' << times << endl;
	}
}
int main() {
	int n=3;
	
	
	while (1) {
		cin >> n;
		system("cls");
		Hanoi(n);
	}
}
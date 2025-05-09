#include <iostream>
using namespace std;

/*void swapByValue(int a, int b) {
    int temp = a;
    a = b;
    b = temp;
    cout << "Inside swap: a = " << a << ", b = " << b << endl;
}

int main() {
    int x = 10, y = 20;
    cout << "Before swap: x = " << x << ", y = " << y << endl;
    swapByValue(x, y);
    cout << "After swap: x = " << x << ", y = " << y << endl;
    return 0;
}
*/

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void swapByReference(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
    cout << "Inside swap: a = " << a << ", b = " << b << endl;
}

int main() {
    int x = 10, y = 20;
    cout << "Before swap: x = " << x << ", y = " << y << endl;
    swapByReference(x, y);
    cout << "After swap: x = " << x << ", y = " << y << endl;
    return 0;
}


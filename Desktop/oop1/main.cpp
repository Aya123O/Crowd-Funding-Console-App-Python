#include <iostream>
using namespace std;

class Complex {
private:
    double real;
    double imaginary;

public:
    // Constructor to initialize the complex number
    Complex(double r = 0, double i = 0) {
        real = r;
        imaginary = i;
    }

    // Destructor
    ~Complex() {
        cout << "Complex number (" << real << " + " << imaginary << "i) is being destroyed Su" << endl;
    }

    // Getter and setter for real part
    double getReal() const {
        return real;
    }

    void setReal(double r) {
        real = r;
    }

    // Getter and setter for imaginary part
    double getImaginary() const {
        return imaginary;
    }

    void setImaginary(double i) {
        imaginary = i;
    }

    // Function to set both real and imaginary parts at once
    void setComplex(double r, double i) {
        real = r;
        imaginary = i;
    }

    // Add two complex numbers
    Complex add(const Complex& other) const {
        Complex result(real + other.getReal(), imaginary + other.getImaginary());
        return result;
    }

    // Subtract two complex numbers
    Complex subtract(const Complex& other) const {
        Complex result(real - other.getReal(), imaginary - other.getImaginary());
        return result;
    }

    // Display the complex number
    void display() const {
        if (real == 0 && imaginary == 0) {
            cout << "0" << endl;
        }
        else if (real == 0) {
            cout << imaginary << "i" << endl;
        }
        else if (imaginary == 0) {
            cout << real << endl;
        }
        else {
            if (imaginary < 0)
                cout << real << " - " << -imaginary << "i" << endl;
            else
                cout << real << " + " << imaginary << "i" << endl;
        }
    }
};

int main() {
    double realPart, imaginaryPart;


    cout << "Enter both real and imaginary parts of the first number : ";
    cin >> realPart >> imaginaryPart;
    Complex num1;
    num1.setComplex(realPart, imaginaryPart);


    cout << "Enter both real and imaginary parts of the second number : ";
    cin >> realPart >> imaginaryPart;
    Complex num2;
    num2.setComplex(realPart, imaginaryPart);


    Complex sum = num1.add(num2);
    cout << "The sum is: ";
    sum.display();

    Complex diff = num1.subtract(num2);
    cout << "The difference is: ";
    diff.display();

    return 0;
}

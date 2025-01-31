#ifndef PERSON_H
#define PERSON_H

#include <string>

class Person {
private:
    std::string name;
    int age;
    void doSomething() const;
public:
    Person(std::string n, int a);
    Person();
    std::string getName() const;
    void setName(const std::string &n);
};

#endif
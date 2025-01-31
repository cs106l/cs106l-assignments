#include "class.h"

Person::Person() {
    name = "";
    age = 1;
}

Person::Person(std::string n, int a) : name(n), age(a) {}

void Person::doSomething() const {}

std::string Person::getName() const{
    Person::doSomething();
    return name;
}

void Person::setName(const std::string &n) {
    Person::doSomething();
    name = n;
}


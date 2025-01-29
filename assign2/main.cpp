/*
 * CS106L Assignment 2: Marriage Pact
 * Created by Haven Whitney with modifications by Fabio Ibanez & Jacob Roberts-Baca.
 *
 * Welcome to Assignment 2 of CS106L! Please complete each STUDENT TODO
 * in this file. You do not need to modify any other files.
 *
 */

#include <fstream>
#include <iostream>
#include <queue>
#include <set>
#include <string>
#include <unordered_set>

#include "utils.h"

std::string kYourName = "sleepy joe"; // Don't forget to change this!

/**
 * Takes in a file name and returns a set containing all of the applicant names as a set.
 *
 * @param filename  The name of the file to read.
 *                  Each line of the file will be a single applicant's name.
 * @returns         A set of all applicant names read from the file.
 *
 * @remark Feel free to change the return type of this function (and the function
 * below it) to use a `std::unordered_set` instead. If you do so, make sure
 * to also change the corresponding functions in `utils.h`.
 */
std::set<std::string> get_applicants(std::string filename) {
  // STUDENT TODO: Implement this function. 
 /**/ auto set = std::set<std::string>();
  std::ifstream file(filename);
  std::string name;
  while(std::getline(file, name)) {
       set.insert(name);
  }
  return set;
}

/**
 * Takes in a set of student names by reference and returns a queue of names
 * that match the given student name.
 *
 * @param name      The returned queue of names should have the same initials as this name.
 * @param students  The set of student names.
 * @return          A queue containing pointers to each matching name.
 */
bool ShareInitials(std::string s ,std::string r){
   return s[0] == r[0];
}
std::queue<const std::string*> find_matches(std::string name, std::set<std::string>& students) {
  // STUDENT TODO: Implement this function.
  auto queue = std::queue<const std::string*>();
  for( auto item : students){
      if(ShareInitials(name,item)){
            std::string *ptr = new std::string{item};
            std::string elem = *ptr;
            queue.push(ptr);
      }
  }
  return queue;
}

/**
 * Takes in a queue of pointers to possible matches and determines the one true match!
 *
 * You can implement this function however you'd like, but try to do something a bit
 * more complicated than a simple `pop()`.
 *
 * @param matches The queue of possible matches.
 * @return        Your magical one true love.
 *                Will return "NO MATCHES FOUND." if `matches` is empty.
 */
std::string get_match(std::queue<const std::string*>& matches) {
  // STUDENT TODO: Implement this function.
  if(!matches.empty())
  {
      const std::string *item = matches.front();
      std::string elem = *item;
      return elem;
  }
  std::string str = "NO MATCHES FOUND.";
   return str;
}

/* #### Please don't modify this call to the autograder! #### */
int main() {
   // std::set<std::string>sets = get_applicants("/home/jeff/cs106l-assignments/assign2/students.txt");
    //std::queue<const std::string*>m = find_matches("A",sets);
  //  get_match(m);
   return run_autograder();
  // return 0;
}


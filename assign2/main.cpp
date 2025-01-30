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
#include <sstream>
#include <string>

#include "utils.h"

std::string kYourName = "kai yang"; // Don't forget to change this!

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
    std::set<std::string> applicants;  // Using unordered_set for efficiency
    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Could not open the file!" << std::endl;
        return applicants;
    }

    std::string line;
    while (std::getline(file, line)) {
        applicants.insert(line);  // Add name to the set
    }
    file.close();
    return applicants;
}

const std::string& getInitials(const std::string& name) {
    std::string token;
    std::istringstream tokenStream(name);
    std::getline(tokenStream, token, ' ');
    return token;
}

/**
 * Takes in a set of student names by reference and returns a queue of names
 * that match the given student name.
 *
 * @param name      The returned queue of names should have the same initials as this name.
 * @param students  The set of student names.
 * @return          A queue containing pointers to each matching name.
 */
std::queue<const std::string*> find_matches(std::string name, std::set<std::string>& students) {
  // STUDENT TODO: Implement this function.
    std::string target = getInitials(name);
    std::queue<const std::string*> q;
    for (const auto& stu : students) {
        std::string initial = getInitials(stu);
        if (initial == target) {
            q.push(&stu);
        }
    }
    return q;
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
    if (matches.empty()) {
        return "NO MATCHES FOUND.";
    }
    return *matches.front();
}

/* #### Please don't modify this call to the autograder! #### */
int main() { return run_autograder(); }

#ifndef CHURIKOV_FI_01_REQUEST_HPP
#define CHURIKOV_FI_01_REQUEST_HPP

#include <string>


enum CommandName {
    CREATE, INSERT, PRINT_TREE, CONTAINS, SEARCH
};

class Request {
public:
    virtual CommandName getCommandName() = 0;
};

class CreateRequest : public Request {
private:
    std::string trie_name;
public:
    explicit CreateRequest(std::string trie_name) : Request(), trie_name(std::move(trie_name)) {}

    CommandName getCommandName() override { return CREATE; }

    std::string getTrieName() { return trie_name; }
};

class InsertRequest : public Request {
private:
    std::string trie_name, value;
public:
    explicit InsertRequest(std::string trie_name, std::string value)
            : Request(), trie_name(std::move(trie_name)), value(std::move(value)) {}

    CommandName getCommandName() override { return INSERT; }

    std::string getTrieName() { return trie_name; }

    std::string getValue() { return value; }
};

class PrintTreeRequest : public Request {
private:
    std::string trie_name;
public:
    explicit PrintTreeRequest(std::string trie_name) : Request(), trie_name(std::move(trie_name)) {}

    CommandName getCommandName() override { return PRINT_TREE; }

    std::string getTrieName() { return trie_name; }
};

class ContainsRequest : public Request {
private:
    std::string trie_name, value;
public:
    explicit ContainsRequest(std::string trie_name, std::string value)
            : Request(), trie_name(std::move(trie_name)), value(std::move(value)) {}

    CommandName getCommandName() override { return CONTAINS; }

    std::string getTrieName() { return trie_name; }

    std::string getValue() { return value; }
};

class SearchRequest : public Request {
private:
    std::string trie_name;

    std::string word1, word2;

    bool reverse, between, match;
public:
    explicit SearchRequest(
            std::string trie_name,
            bool between, bool match,
            std::string word1, std::string word2,
            bool reverse) : Request(),
            trie_name(std::move(trie_name)),
            between(between), match(match),
            word1(std::move(word1)), word2(std::move(word2)),
            reverse(reverse) {}

    CommandName getCommandName() override { return SEARCH; }

    std::string getTrieName() { return trie_name; }

    std::string getWord1() { return word1; }

    std::string getWord2() { return word2; }

    bool getReverse() { return reverse; }

    bool getBetween() { return between; }

    bool getMatch() { return match; }
};

#endif

#ifndef CHURIKOV_FI_01_TRIE_HPP
#define CHURIKOV_FI_01_TRIE_HPP

#include <string>
#include <vector>
#include <map>

class Trie {
private:
    struct Node {
        std::map<char, Node *> children;
        bool isEnd;

        Node();
    };

    Node root{};
public:
    Trie() = default;

    void insert(std::string str);

    std::string print();

    bool contains(std::string str);

    std::vector<std::string> search(std::string word1, std::string word2, bool reverse, bool between, bool match);
};


#endif //CHURIKOV_FI_01_TRIE_HPP

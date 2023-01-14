#include "Trie.hpp"
#include <sstream>
#include <stack>
#include <list>


Trie::Node::Node() {
    children = std::map<char, Node *>();
    isEnd = false;
}

void Trie::insert(std::string str) {
    auto iter = str.begin();
    Node *curr = &root, *parent;
    while (iter != str.end() && curr->children.contains(*iter)) {
        curr = curr->children[*iter];
        ++iter;
    }
    while (iter != str.end()) {
        parent = curr;
        curr = new Node();
        parent->children.insert({*iter, curr});
        ++iter;
    }
    curr->isEnd = true;
}

std::string Trie::print() {
    std::list<bool> branch_is_over;
    std::stack<std::_Rb_tree_iterator<std::pair<const char, Trie::Node *>>> iterators, backs;
    backs.push(root.children.end());
    iterators.push(root.children.begin());

    std::stringstream ss;
    ss << "[root]";
    if (root.isEnd) ss << '!';
    ss << std::endl;

    while (iterators.size() != 1 || iterators.top() != backs.top()) {
        if (iterators.top() != backs.top()) {
            for (bool b: branch_is_over)
                if (!b)
                    ss << " |  ";
                else
                    ss << "    ";
            ss << " +--\"" << iterators.top()->first << '\"';
            if (iterators.top()->second->isEnd)
                ss << '!';
            ss << std::endl;
            branch_is_over.push_back(std::next(iterators.top()) == backs.top());
            backs.push(iterators.top()->second->children.end());
            iterators.push(iterators.top()->second->children.begin());
        } else {
            branch_is_over.pop_back();
            backs.pop();
            iterators.pop();
            ++(iterators.top());
        }
    }

    return ss.str();
}

bool Trie::contains(std::string str) {
    auto iter = str.begin();
    Node *curr = &root;
    while (true) {
        if (iter == str.end()) {
            return curr->isEnd;
        }
        if (!curr->children.contains(*iter)) {
            return false;
        }
        curr = curr->children[*iter];
        ++iter;
    }
}

std::vector<std::string> Trie::search(std::string word1, std::string word2, bool reverse, bool between, bool match) {
    std::vector<std::string> strings;

    if (!between && !match) {
        std::stack<std::_Rb_tree_iterator<std::pair<const char, Trie::Node *>>> iterators, backs;
        std::string prefix;
        backs.push(root.children.end());
        iterators.push(root.children.begin());
        if (root.isEnd)
            strings.emplace_back("");

        while (iterators.size() != 1 || iterators.top() != backs.top()) {
            if (iterators.top() != backs.top()) {
                prefix.push_back(iterators.top()->first);
                if (iterators.top()->second->isEnd)
                    strings.push_back(prefix);
                backs.push(iterators.top()->second->children.end());
                iterators.push(iterators.top()->second->children.begin());
            } else {
                prefix.pop_back();
                backs.pop();
                iterators.pop();
                ++(iterators.top());
            }
        }
    }
    if (between) {
        std::stack<std::_Rb_tree_iterator<std::pair<const char, Trie::Node *>>> iterators, backs;
        std::string prefix;
        backs.push(root.children.end());
        iterators.push(root.children.begin());
        if (root.isEnd)
            strings.emplace_back("");

        auto it1 = word1.begin();
        while (!(iterators.top()->first > *it1 || (iterators.top()->first == *it1 && (iterators.top()->second->children.empty() || it1 == --word1.end())))) {
            if (iterators.top()->first == *it1) {
                ++it1;
                prefix.push_back(iterators.top()->first);
                backs.push(iterators.top()->second->children.end());
                iterators.push(iterators.top()->second->children.begin());
            }
            else
                ++(iterators.top());
        }

        auto it2 = word2.begin();
        auto stop = root.children.begin(), stotop = root.children.end();
        while (!(stop->first > *it2 || (stop->first == *it2 && (stop->second->children.empty() || it2 == --word2.end())) || stop == stotop)) {
            if (stop->first == *it2) {
                ++it2;
                stotop = stop->second->children.end();
                stop = stop->second->children.begin();
            }
            else
                ++stop;
        }

        while ((iterators.size() != 1 || iterators.top() != backs.top())) {
            if (iterators.top() != backs.top()) {
                prefix.push_back(iterators.top()->first);
                if (iterators.top() == stop) {
                    if (iterators.top()->second->isEnd)
                        strings.push_back(prefix);
                    break;
                }
                if (iterators.top()->second->isEnd)
                    strings.push_back(prefix);
                backs.push(iterators.top()->second->children.end());
                iterators.push(iterators.top()->second->children.begin());
            } else {
                prefix.pop_back();
                backs.pop();
                iterators.pop();
                ++(iterators.top());
                if (iterators.top() == stop)
                    break;
            }
        }
    }
    if (match) {
        reverse = !reverse;

        std::stack<int> poses;
        std::stack<std::string> prefixes;
        std::stack<Trie::Node> nodes;

        nodes.push(root);
        prefixes.push("");
        poses.push(0);

        while (!nodes.empty()) {
            Trie::Node node = nodes.top();
            std::string prefix = prefixes.top();
            int pos = poses.top();

            nodes.pop();
            prefixes.pop();
            poses.pop();

            if ((pos == word1.length() || (pos >= word1.length()-1 && word1.ends_with('*'))) && node.isEnd) {
                strings.push_back(prefix);
            }

            if (!node.children.empty()) {
                if (pos <= word1.length()) {
                    if (word1[pos] == '?') {
                        for (auto & i : node.children) {
                            nodes.push(*i.second);
                            prefixes.push(prefix + i.first);
                            poses.push(pos + 1);
                        }
                    }
                    else {
                        if (node.children.contains(word1[pos])) {
                            nodes.push(*node.children[word1[pos]]);
                            prefixes.push(prefix + word1[pos]);
                            poses.push(pos + 1);
                        }
                    }
                }
                if (pos >= word1.length() - 1 && word1.ends_with('*')) {
                    for (auto & i : node.children) {
                        nodes.push(*i.second);
                        prefixes.push(prefix + i.first);
                        poses.push(pos + 1);
                    }
                }
            }
        }
    }

    std::sort(strings.begin(), strings.end());
    if (reverse)
        std::reverse(strings.begin(), strings.end());

    return strings;
}

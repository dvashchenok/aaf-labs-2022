#include "Parser.hpp"
#include <regex>


std::shared_ptr<ParsingResult> Parser::parse(const std::string &str) {
    std::smatch match;
    if (std::regex_search(str, match, std::regex(R"(^\s*EXIT\s*;$)", std::regex_constants::icase))) {
        return std::make_shared<ParsingResult>();
    }
    if (std::regex_search(str, match,
                          std::regex(R"(^\s*CREATE\s+([a-zA-Z][a-zA-Z0-9_]*)\s*;$)", std::regex_constants::icase))) {
        return std::make_shared<SuccessParsingResult>(std::make_shared<CreateRequest>(match.str(1)));
    }
    if (std::regex_search(str, match, std::regex(R"f(^\s*INSERT\s+([a-zA-Z][a-zA-Z0-9_]*)\s+"(.*)"\s*;$)f",
                                                 std::regex_constants::icase))) {
        return std::make_shared<SuccessParsingResult>(std::make_shared<InsertRequest>(match.str(1), match.str(2)));
    }
    if (std::regex_search(str, match, std::regex(R"(^\s*PRINT_TREE\s+([a-zA-Z][a-zA-Z0-9_]*)\s*;$)",
                                                 std::regex_constants::icase))) {
        return std::make_shared<SuccessParsingResult>(std::make_shared<PrintTreeRequest>(match.str(1)));
    }
    if (std::regex_search(str, match, std::regex(R"f(^\s*CONTAINS\s+([a-zA-Z][a-zA-Z0-9_]*)\s+"(.*)"\s*;$)f",
                                                 std::regex_constants::icase))) {
        return std::make_shared<SuccessParsingResult>(std::make_shared<ContainsRequest>(match.str(1), match.str(2)));
    }
    if (std::regex_search(str, match,
                          std::regex(R"(^\s*SEARCH\s+([a-zA-Z][a-zA-Z0-9_]*)(?:\s+WHERE\s+(BETWEEN\s+".*"\s*,\s*".*"|MATCH\s+".*"))?(?:\s+(ASC|DESC))?\s*;$)", std::regex_constants::icase))) {
        std::string trie_name = match.str(1);
        std::string ascdesc = match.str(3);
        bool reverse = std::regex_match(ascdesc, std::regex("DESC", std::regex_constants::icase));
        bool between = false;
        bool match_ = false;
        std::string word1{};
        std::string word2{};
        std::smatch m;
        std::string s = match.str(2);
        if (std::regex_match(s, std::regex(R"(MATCH\s+".*")", std::regex_constants::icase))) {
            std::regex_search(s, m, std::regex(R"f(MATCH\s+"(.*)")f", std::regex_constants::icase));
            word1 = m.str(1);
            match_ = true;
        }
        if (std::regex_match(s, std::regex(R"(BETWEEN\s+".*"\s*,\s*".*")", std::regex_constants::icase))) {
            std::regex_search(s, m, std::regex(R"f(BETWEEN\s+"(.*)"\s*,\s*"(.*)")f", std::regex_constants::icase));
            word1 = m.str(1);
            word2 = m.str(2);
            between = true;
        }
        return std::make_shared<SuccessParsingResult>(std::make_shared<SearchRequest>(trie_name, between, match_, word1, word2, reverse));
    }
    return std::make_shared<ErrorParsingResult>("Syntax error");
}

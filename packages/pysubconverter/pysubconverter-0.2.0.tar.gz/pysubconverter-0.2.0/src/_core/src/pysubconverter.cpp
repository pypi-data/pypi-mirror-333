#include "pysubconverter.hpp"

#include <filesystem>
#include <string>

#include <subconverter/handler/webget.h>
#include <subconverter/utils/system.h>
#include <subconverter/utils/urlencode.h>

namespace fs = std::filesystem;

namespace _core {
void init_config() {
    if (!fileExist(global.prefPath)) {
        if (fileExist("pref.toml"))
            global.prefPath = "pref.toml";
        else if (fileExist("pref.yml"))
            global.prefPath = "pref.yml";
        else if (!fileExist("pref.ini")) {
            if (fileExist("pref.example.toml")) {
                fileCopy("pref.example.toml", "pref.toml");
                global.prefPath = "pref.toml";
            }
            else if (fileExist("pref.example.yml")) {
                fileCopy("pref.example.yml", "pref.yml");
                global.prefPath = "pref.yml";
            }
            else if (fileExist("pref.example.ini"))
                fileCopy("pref.example.ini", "pref.ini");
        }
    }
    readConf();
    if (!global.updateRulesetOnRequest)
        refreshRulesets(global.customRulesets, global.rulesetsContent);

    std::string env_api_mode = getEnv("API_MODE");
    std::string env_managed_prefix = getEnv("MANAGED_PREFIX");
    std::string env_token = getEnv("API_TOKEN");
    global.APIMode = tribool().parse(toLower(env_api_mode)).get(global.APIMode);
    if (!env_managed_prefix.empty())
        global.managedConfigPrefix = env_managed_prefix;
    if (!env_token.empty())
        global.accessToken = env_token;
}

void update_config(const std::map<std::string, std::string> &arguments) {
    auto type_it = arguments.find("type");
    auto data_it = arguments.find("data");

    if (type_it != arguments.end() && data_it != arguments.end()) {
        std::string type = type_it->second;
        std::string data = data_it->second;

        if (type == "form" || type == "direct")
            fileWrite(global.prefPath, data, true);
    }
    else {
        throw std::runtime_error("Invalid arguments, type and data are required.");
    }
}

std::string subconverter(const std::map<std::string, std::string> &arguments) {
    Request request;
    for (auto &item : arguments) {
        request.argument.emplace(item.first, item.second);
    }
    Response response;
    return ::subconverter(request, response);
}

void flush_cache() {
    flushCache();
}

std::string sub_to_clashr(const std::map<std::string, std::string> &arguments) {
    Request request;
    for (auto &item : arguments) {
        request.argument.emplace(item.first, item.second);
    }
    Response response;
    return simpleToClashR(request, response);
}

std::string surge_to_clashr(const std::map<std::string, std::string> &arguments) {
    Request request;
    for (auto &item : arguments) {
        request.argument.emplace(item.first, item.second);
    }
    Response response;
    return surgeConfToClash(request, response);
}

std::string get_ruleset(const std::map<std::string, std::string> &arguments) {
    Request request;
    for (auto &item : arguments) {
        request.argument.emplace(item.first, item.second);
    }
    Response response;
    return getRuleset(request, response);
}

std::string get_profile(const std::map<std::string, std::string> &arguments) {
    Request request;
    for (auto &item : arguments) {
        request.argument.emplace(item.first, item.second);
    }
    Response response;
    return getProfile(request, response);
}

std::string render(const std::map<std::string, std::string> &arguments) {
    Request request;
    for (auto &item : arguments) {
        request.argument.emplace(item.first, item.second);
    }
    Response response;
    return renderTemplate(request, response);
}

std::string get(const std::map<std::string, std::string> &arguments) {
    auto url_it = arguments.find("url");
    if (url_it == arguments.end()) {
        throw std::runtime_error("Invalid arguments, url is required.");
    }
    std::string url = urlDecode(url_it->second);
    return webGet(url, "");
}

std::string get_local(const std::map<std::string, std::string> &arguments) {
    auto path_it = arguments.find("path");
    if (path_it == arguments.end()) {
        throw std::runtime_error("Invalid arguments, path is required.");
    }
    std::string path = urlDecode(path_it->second);
    return fileGet(path);
}

} // namespace _core

#pragma once

#include <subconverter/handler/settings.h>
#include "subconverter/handler/interfaces.h"

namespace _core {

void init_config();

void update_config(const std::map<std::string, std::string> &arguments);

std::string subconverter(const std::map<std::string, std::string> &arguments);

void flush_cache();

std::string sub_to_clashr(const std::map<std::string, std::string> &arguments);

std::string surge_to_clashr(const std::map<std::string, std::string> &arguments);

std::string get_ruleset(const std::map<std::string, std::string> &arguments);

std::string get_profile(const std::map<std::string, std::string> &arguments);

std::string render(const std::map<std::string, std::string> &arguments);

std::string get(const std::map<std::string, std::string> &arguments);

std::string get_local(const std::map<std::string, std::string> &arguments);

} // namespace _core

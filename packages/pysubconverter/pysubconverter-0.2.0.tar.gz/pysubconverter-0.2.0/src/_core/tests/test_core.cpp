#include <gmock/gmock-matchers.h>
#include <gtest/gtest.h>

#include "_core.hpp"
#include "pysubconverter.hpp"
#include "utils.hpp"

TEST(_core, version) {
    auto version = _core::ProjectVersion();
    EXPECT_TRUE(!version.empty());
}

using _core_rc_test = test::utils::rc_dir_test;

TEST_F(_core_rc_test, subconverter) {
    auto config_dir = this->test_data_dir_ / "config";
    std::filesystem::current_path(config_dir);
    _core::init_config();
    std::vector<std::string> urls = {
        "ss://YWVzLTI1Ni1nY206VEV6amZBWXEySWp0dW9T@127.0.0.1:0123#fake 1",
        "ss://YWVzLTI1Ni1nY206VEV6amZBWXEySWp0dW9T@127.0.0.1:0123#fake 2",
        "ss://YWVzLTI1Ni1nY206VEV6amZBWXEySWp0dW9T@127.0.0.1:0123#fake 3",
    };
    auto url =
        std::accumulate(std::next(urls.begin()), urls.end(), urls.front(), [](auto a, auto b) { return a + "|" + b; });
    std::map<std::string, std::string> arguments;
    arguments.emplace("target", "clash");
    arguments.emplace("url", url);
    auto result = _core::subconverter(arguments);
    EXPECT_THAT(result, testing::HasSubstr("proxies"));
    for (size_t i = 1; i <= urls.size(); ++i)
        EXPECT_THAT(result, ::testing::HasSubstr("fake " + std::to_string(i)));
}

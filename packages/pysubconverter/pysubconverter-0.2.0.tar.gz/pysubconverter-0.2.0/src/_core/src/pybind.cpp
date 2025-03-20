#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "_core.hpp"
#include "pysubconverter.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
    m.doc() = R"pbdoc(
      Pybind11 _core plugin
      -----------------------
      .. currentmodule:: _core
    )pbdoc";

    m.def("version", []() { return _core::ProjectVersion(); }, R"pbdoc(
        The _core plugin version.
    )pbdoc");

    py::class_<Settings> settings_cls(m, "Settings", R"pbdoc(Global unique settings for subconverter.)pbdoc");
    settings_cls.def(py::init<>())
        .def_readwrite("pref_path",
                       &Settings::prefPath,
                       py::doc(R"pbdoc(Preferred path to be read for subconverter.)pbdoc"));

    m.attr("settings") = py::cast(global, py::return_value_policy::reference);

    m.def("init_config",
          _core::init_config,
          py::doc(R"pbdoc(initialize the configuration directory from subconverter.)pbdoc"));

    m.def("subconverter", _core::subconverter, py::arg("arguments"), py::doc(R"pbdoc(convert to subscription format

Args:
    arguments (dict): subscription conversion arguments.
Returns:
    str: converted subscription.)pbdoc"));

    m.def("update_config",
          _core::update_config,
          py::arg("arguments"),
          py::doc(R"pbdoc(update the configuration from subconverter.)pbdoc"));

    m.def("flush_cache", _core::flush_cache, py::doc(R"pbdoc(flush the cache.)pbdoc"));

    m.def("sub_to_clashr",
          _core::sub_to_clashr,
          py::arg("arguments"),
          py::doc(R"pbdoc(convert subscription to clashroyale format

Args:
    arguments (dict): subscription conversion arguments.
Returns:
    str: converted clashroyale subscription.)pbdoc"));

    m.def("surge_to_clashr",
          _core::surge_to_clashr,
          py::arg("arguments"),
          py::doc(R"pbdoc(convert surge to clashroyale format

Args:
    arguments (dict): surge conversion arguments.
Returns:
    str: converted clashroyale subscription.)pbdoc"));

    m.def("get_ruleset",
          _core::get_ruleset,
          py::arg("arguments"),
          py::doc(R"pbdoc(get the ruleset from subconverter.)pbdoc"));

    m.def("get_profile",
          _core::get_profile,
          py::arg("arguments"),
          py::doc(R"pbdoc(get the profile from subconverter.)pbdoc"));

    m.def("render", _core::render, py::arg("arguments"), py::doc(R"pbdoc(render the subscription.)pbdoc"));

    m.def("get", _core::get, py::arg("arguments"), py::doc(R"pbdoc(get from the url.)pbdoc"));

    m.def("get_local", _core::get_local, py::arg("arguments"), py::doc(R"pbdoc(get from the local file.)pbdoc"));
}

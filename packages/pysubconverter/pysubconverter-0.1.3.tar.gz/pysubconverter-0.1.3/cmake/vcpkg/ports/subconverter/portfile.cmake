vcpkg_check_linkage(ONLY_STATIC_LIBRARY)

vcpkg_from_github(
    OUT_SOURCE_PATH SOURCE_PATH
    REPO tindy2013/subconverter
    REF "${VERSION}"
    SHA512 9f4dfa97da1ce2cb664d61625e542eea2629ea347c1476e99b78b8b77e516696ff79f243218087f4fce53c3bb43f48f87f1dfd84b1eeb5f4531bf103492b5e71
    HEAD_REF master
    PATCHES
        fix_build_and_install.patch
)

file(COPY "${CMAKE_CURRENT_LIST_DIR}/unofficial-subconverter-config.cmake.in" DESTINATION "${SOURCE_PATH}")

file(GLOB ambiguous_file "${SOURCE_PATH}/base/rules/DivineEngine/Surge/Ruleset/StreamingMedia/Video/*coveryPlus.list")
message(STATUS "Renaming ambiguous file ${ambiguous_file} to ${SOURCE_PATH}/base/rules/DivineEngine/Surge/Ruleset/StreamingMedia/Video/DiscoveryPlus.list")
file(RENAME ${ambiguous_file} "${SOURCE_PATH}/base/rules/DivineEngine/Surge/Ruleset/StreamingMedia/Video/DiscoveryPlus.list")

vcpkg_cmake_configure(
    SOURCE_PATH "${SOURCE_PATH}"
    OPTIONS
        -DBUILD_STATIC_LIBRARY=ON
)

vcpkg_cmake_install()
vcpkg_fixup_pkgconfig()
vcpkg_copy_pdbs()

vcpkg_cmake_config_fixup(PACKAGE_NAME unofficial-subconverter CONFIG_PATH share/unofficial-subconverter)

vcpkg_install_copyright(FILE_LIST "${SOURCE_PATH}/LICENSE")

file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include" "${CURRENT_PACKAGES_DIR}/debug/share")

add_subdirectory(lemon)
add_subdirectory(pybind11)

if(IPRM_INCLUDE_STUDIO_CXX_IMPL)
    add_subdirectory(graphviz)
    add_subdirectory(K-Editor)
    add_subdirectory(qt)
endif()

if(IPRM_INCLUDE_STUDIO_RUST_IMPL)
    add_subdirectory(corrosion-rs)
endif()

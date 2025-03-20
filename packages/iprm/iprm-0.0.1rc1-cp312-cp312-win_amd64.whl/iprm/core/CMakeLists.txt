pybind11_add_module(core
    src/bindings.cpp
    src/typeflags.hpp
    src/object.hpp
    src/object.cpp
    src/session.hpp
    src/session.cpp
)


add_custom_command(TARGET core
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "$<TARGET_FILE:core>"
        "${CMAKE_CURRENT_SOURCE_DIR}/$<TARGET_FILE_NAME:core>"
)
if(WIN32 AND (${CMAKE_BUILD_TYPE} STREQUAL "Debug" OR ${CMAKE_BUILD_TYPE} STREQUAL "RelWithDebInfo"))
    add_custom_command(TARGET core POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different
            "${CMAKE_CURRENT_BINARY_DIR}/core.pdb"
            "${CMAKE_CURRENT_SOURCE_DIR}/core.pdb"
    )
endif()

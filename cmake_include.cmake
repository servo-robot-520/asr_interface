if (NOT ROS2_WS_SOURCE_BUILD OR NOT TARGET asr_interface)
    find_package(asr_interface REQUIRED)
endif ()

if (ROS2_WS_SOURCE_BUILD AND TARGET asr_interface)
    # 在源码聚合构建中，依赖包尚未安装到 install/，因此直接使用构建树中的
    # typesupport target 与源码 include 目录。
    rosidl_get_typesupport_target(asr_interface_CPP_TYPESUPPORT_TARGET
            asr_interface
            "rosidl_typesupport_cpp"
    )
    rosidl_get_typesupport_target(asr_interface_FASTRTPS_CPP_TYPESUPPORT_TARGET
            asr_interface
            "rosidl_typesupport_fastrtps_cpp"
    )
    rosidl_get_typesupport_target(asr_interface_INTROSPECTION_CPP_TYPESUPPORT_TARGET
            asr_interface
            "rosidl_typesupport_introspection_cpp"
    )
    if (asr_interface_CPP_TYPESUPPORT_TARGET MATCHES "-NOTFOUND$"
            OR asr_interface_FASTRTPS_CPP_TYPESUPPORT_TARGET MATCHES "-NOTFOUND$"
            OR asr_interface_INTROSPECTION_CPP_TYPESUPPORT_TARGET MATCHES "-NOTFOUND$")
        message(FATAL_ERROR "The in-tree asr_interface target does not provide rosidl typesupport targets.")
    endif ()
    if (NOT DEFINED asr_interface_SOURCE_DIR
            OR NOT IS_DIRECTORY "${asr_interface_SOURCE_DIR}/include")
        message(FATAL_ERROR "The in-tree asr_interface source include directory is unavailable.")
    endif ()
    target_link_libraries(${PROJECT_NAME} PUBLIC
            ${asr_interface_CPP_TYPESUPPORT_TARGET}
    )
    target_include_directories(${PROJECT_NAME} PUBLIC
            "$<BUILD_INTERFACE:${asr_interface_SOURCE_DIR}/include>")
else ()
    ament_target_dependencies(${PROJECT_NAME} asr_interface)
endif ()

if (ROS2_WS_SOURCE_BUILD)
    target_link_libraries(${PROJECT_NAME} PUBLIC
            "-Wl,--no-as-needed"
            ${asr_interface_FASTRTPS_CPP_TYPESUPPORT_TARGET}
            ${asr_interface_INTROSPECTION_CPP_TYPESUPPORT_TARGET}
            "-Wl,--as-needed"
    )
endif ()

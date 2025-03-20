#
# Attempt to find the python package that uses the same python executable as
# `EXECUTABLE` and is one of the `SUPPORTED_VERSIONS`.
#
macro (find_python_from_executable EXECUTABLE SUPPORTED_VERSIONS)
  file(REAL_PATH ${EXECUTABLE} EXECUTABLE)
  set(Python_EXECUTABLE ${EXECUTABLE})
  find_package(Python COMPONENTS Interpreter Development.Module)
  if (NOT Python_FOUND)
    message(FATAL_ERROR "Unable to find python matching: ${EXECUTABLE}.")
  endif()
  set(_VER "${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}")
  set(_SUPPORTED_VERSIONS_LIST ${SUPPORTED_VERSIONS} ${ARGN})
  if (NOT _VER IN_LIST _SUPPORTED_VERSIONS_LIST)
    message(FATAL_ERROR
      "Python version (${_VER}) is not one of the supported versions: "
      "${_SUPPORTED_VERSIONS_LIST}.")
  endif()
  message(STATUS "Found python matching: ${EXECUTABLE}.")
endmacro()

#
# Run `EXPR` in python.  The standard output of python is stored in `OUT` and
# has trailing whitespace stripped.  If an error is encountered when running
# python, a fatal message `ERR_MSG` is issued.
#
function (run_python OUT EXPR ERR_MSG)
  execute_process(
    COMMAND
    "${Python_EXECUTABLE}" "-c" "${EXPR}"
    OUTPUT_VARIABLE PYTHON_OUT
    RESULT_VARIABLE PYTHON_ERROR_CODE
    ERROR_VARIABLE PYTHON_STDERR
    OUTPUT_STRIP_TRAILING_WHITESPACE)

  if(NOT PYTHON_ERROR_CODE EQUAL 0)
    message(FATAL_ERROR "${ERR_MSG}: ${PYTHON_STDERR}")
  endif()
  set(${OUT} ${PYTHON_OUT} PARENT_SCOPE)
endfunction()

# Run `EXPR` in python after importing `PKG`. Use the result of this to extend
# `CMAKE_PREFIX_PATH` so the torch cmake configuration can be imported.
macro (append_cmake_prefix_path PKG EXPR)
  run_python(_PREFIX_PATH
    "import ${PKG}; print(${EXPR})" "Failed to locate ${PKG} path")
  list(APPEND CMAKE_PREFIX_PATH ${_PREFIX_PATH})
endmacro()

#
# Get additional GPU compiler flags from torch.
#
function (get_torch_gpu_compiler_flags OUT_GPU_FLAGS GPU_LANG)
  if (${GPU_LANG} STREQUAL "CUDA")
    #
    # Get common NVCC flags from torch.
    #
    run_python(GPU_FLAGS
      "from torch.utils.cpp_extension import COMMON_NVCC_FLAGS; print(';'.join(COMMON_NVCC_FLAGS))"
      "Failed to determine torch nvcc compiler flags")

    if (CUDA_VERSION VERSION_GREATER_EQUAL 11.8)
      list(APPEND GPU_FLAGS "-DENABLE_FP8_E5M2")
    endif()
  endif()
  set(${OUT_GPU_FLAGS} ${GPU_FLAGS} PARENT_SCOPE)
endfunction()

# Macro for converting a `gencode` version number to a cmake version number.
macro(string_to_ver OUT_VER IN_STR)
  string(REGEX REPLACE "\([0-9]+\)\([0-9]\)" "\\1.\\2" ${OUT_VER} ${IN_STR})
endmacro()

#
# Override the GPU architectures detected by cmake/torch and filter them by
# `GPU_SUPPORTED_ARCHES`. Sets the final set of architectures in
# `GPU_ARCHES`.
#
# Note: this is defined as a macro since it updates `CMAKE_CUDA_FLAGS`.
#
macro(override_gpu_arches GPU_ARCHES GPU_LANG GPU_SUPPORTED_ARCHES)
  set(_GPU_SUPPORTED_ARCHES_LIST ${GPU_SUPPORTED_ARCHES} ${ARGN})
  message(STATUS "${GPU_LANG} supported arches: ${_GPU_SUPPORTED_ARCHES_LIST}")

  if(${GPU_LANG} STREQUAL "CUDA")
    #
    # Setup/process CUDA arch flags.
    #
    # The torch cmake setup hardcodes the detected architecture flags in
    # `CMAKE_CUDA_FLAGS`.  Since `CMAKE_CUDA_FLAGS` is a "global" variable, it
    # can't modified on a per-target basis, e.g. for the `punica` extension.
    # So, all the `-gencode` flags need to be extracted and removed from
    # `CMAKE_CUDA_FLAGS` for processing so they can be passed by another method.
    # Since it's not possible to use `target_compiler_options` for adding target
    # specific `-gencode` arguments, the target's `CUDA_ARCHITECTURES` property
    # must be used instead.  This requires repackaging the architecture flags
    # into a format that cmake expects for `CUDA_ARCHITECTURES`.
    #
    # This is a bit fragile in that it depends on torch using `-gencode` as opposed
    # to one of the other nvcc options to specify architectures.
    #
    # Note: torch uses the `TORCH_CUDA_ARCH_LIST` environment variable to override
    # detected architectures.
    #
    message(DEBUG "initial CMAKE_CUDA_FLAGS: ${CMAKE_CUDA_FLAGS}")

    # Extract all `-gencode` flags from `CMAKE_CUDA_FLAGS`
    string(REGEX MATCHALL "-gencode arch=[^ ]+" _CUDA_ARCH_FLAGS
      ${CMAKE_CUDA_FLAGS})

    # Remove all `-gencode` flags from `CMAKE_CUDA_FLAGS` since they will be modified
    # and passed back via the `CUDA_ARCHITECTURES` property.
    string(REGEX REPLACE "-gencode arch=[^ ]+ *" "" CMAKE_CUDA_FLAGS
      ${CMAKE_CUDA_FLAGS})

    # If this error is triggered, it might mean that torch has changed how it sets
    # up nvcc architecture code generation flags.
    if (NOT _CUDA_ARCH_FLAGS)
      message(FATAL_ERROR
        "Could not find any architecture related code generation flags in "
        "CMAKE_CUDA_FLAGS. (${CMAKE_CUDA_FLAGS})")
    endif()

    message(DEBUG "final CMAKE_CUDA_FLAGS: ${CMAKE_CUDA_FLAGS}")
    message(DEBUG "arch flags: ${_CUDA_ARCH_FLAGS}")

    # Initialize the architecture lists to empty.
    set(${GPU_ARCHES})

    # Process each `gencode` flag.
    foreach(_ARCH ${_CUDA_ARCH_FLAGS})
      # For each flag, extract the version number and whether it refers to PTX
      # or native code.
      # Note: if a regex matches then `CMAKE_MATCH_1` holds the binding
      # for that match.

      string(REGEX MATCH "arch=compute_\([0-9]+a?\)" _COMPUTE ${_ARCH})
      if (_COMPUTE)
        set(_COMPUTE ${CMAKE_MATCH_1})
      endif()

      string(REGEX MATCH "code=sm_\([0-9]+a?\)" _SM ${_ARCH})
      if (_SM)
        set(_SM ${CMAKE_MATCH_1})
      endif()

      string(REGEX MATCH "code=compute_\([0-9]+a?\)" _CODE ${_ARCH})
      if (_CODE)
        set(_CODE ${CMAKE_MATCH_1})
      endif()

      # Make sure the virtual architecture can be matched.
      if (NOT _COMPUTE)
        message(FATAL_ERROR
          "Could not determine virtual architecture from: ${_ARCH}.")
      endif()

      # One of sm_ or compute_ must exist.
      if ((NOT _SM) AND (NOT _CODE))
        message(FATAL_ERROR
          "Could not determine a codegen architecture from: ${_ARCH}.")
      endif()

      if (_SM)
        set(_VIRT "")
        set(_CODE_ARCH ${_SM})
      else()
        set(_VIRT "-virtual")
        set(_CODE_ARCH ${_CODE})
      endif()

      # Check if the current version is in the supported arch list.
      string_to_ver(_CODE_VER ${_CODE_ARCH})
      if (NOT _CODE_VER IN_LIST _GPU_SUPPORTED_ARCHES_LIST)
        message(STATUS "discarding unsupported CUDA arch ${_VER}.")
        continue()
      endif()

      # Add it to the arch list.
      list(APPEND ${GPU_ARCHES} "${_CODE_ARCH}${_VIRT}")
    endforeach()
  endif()
  message(STATUS "${GPU_LANG} target arches: ${${GPU_ARCHES}}")
endmacro()

#
# Define a target named `GPU_MOD_NAME` for a single extension. The
# arguments are:
#
# DESTINATION <dest>         - Module destination directory.
# LANGUAGE <lang>            - The GPU language for this module, e.g CUDA,
#                              etc.
# SOURCES <sources>          - List of source files relative to CMakeLists.txt
#                              directory.
#
# Optional arguments:
#
# ARCHITECTURES <arches>     - A list of target GPU architectures in cmake
#                              format.
#                              Refer `CMAKE_CUDA_ARCHITECTURES` documentation
#                              for more info.
#                              ARCHITECTURES will use cmake's defaults if
#                              not provided.
# COMPILE_FLAGS <flags>      - Extra compiler flags passed to NVCC.
# INCLUDE_DIRECTORIES <dirs> - Extra include directories.
# LINK_LIBRARIES <libraries> - Extra link libraries.
#
# Note: optimization level/debug info is set via cmake build type.
#
function (define_gpu_static_target GPU_MOD_NAME)
  cmake_parse_arguments(PARSE_ARGV 1
    GPU
    ""
    "DESTINATION;LANGUAGE"
    "SOURCES;ARCHITECTURES;COMPILE_FLAGS;INCLUDE_DIRECTORIES;LIBRARIES")

  add_library(${GPU_MOD_NAME} STATIC "${GPU_SOURCES}")

  # Set position independent code property
  set_property(TARGET ${GPU_MOD_NAME} PROPERTY POSITION_INDEPENDENT_CODE ON)

  if (GPU_ARCHITECTURES)
    set_target_properties(${GPU_MOD_NAME} PROPERTIES
      ${GPU_LANGUAGE}_ARCHITECTURES "${GPU_ARCHITECTURES}")
  endif()

  set_property(TARGET ${GPU_MOD_NAME} PROPERTY CXX_STANDARD 17)

  target_compile_options(${GPU_MOD_NAME} PRIVATE
    $<$<COMPILE_LANGUAGE:${GPU_LANGUAGE}>:${GPU_COMPILE_FLAGS} -fPIC>)

  target_compile_definitions(${GPU_MOD_NAME} PRIVATE
    "-DTORCH_EXTENSION_NAME=${GPU_MOD_NAME}")

  target_include_directories(
    ${GPU_MOD_NAME} PRIVATE
    csrc/include/vajra
    csrc/third_party/flashinfer
    csrc/third_party/fmt/include
    csrc/third_party/ddsketch/include
    csrc/third_party/glog
    csrc/third_party/tokenizers-cpp/include
    ${Python_INCLUDE_DIRS}
    ${GPU_INCLUDE_DIRECTORIES}
  )

  target_link_libraries(${GPU_MOD_NAME} PRIVATE ${TORCH_LIBRARIES}
    ${GPU_LIBRARIES} glog::glog fmt::fmt-header-only tokenizers_cpp)

  install(TARGETS ${GPU_MOD_NAME} LIBRARY DESTINATION ${GPU_DESTINATION})
endfunction()

function (define_gpu_extension_target GPU_MOD_NAME)
  cmake_parse_arguments(PARSE_ARGV 1
    GPU
    "WITH_SOABI"
    "DESTINATION;LANGUAGE"
    "SOURCES;ARCHITECTURES;COMPILE_FLAGS;INCLUDE_DIRECTORIES;LIBRARIES")

  if (GPU_WITH_SOABI)
    set(GPU_WITH_SOABI WITH_SOABI)
  else()
    set(GPU_WITH_SOABI)
  endif()

  Python_add_library(${GPU_MOD_NAME} MODULE "${GPU_SOURCES}" ${GPU_WITH_SOABI})

  if (GPU_ARCHITECTURES)
    set_target_properties(${GPU_MOD_NAME} PROPERTIES
      ${GPU_LANGUAGE}_ARCHITECTURES "${GPU_ARCHITECTURES}")
  endif()

  set_property(TARGET ${GPU_MOD_NAME} PROPERTY CXX_STANDARD 17)

  target_compile_options(${GPU_MOD_NAME} PRIVATE
    $<$<COMPILE_LANGUAGE:${GPU_LANGUAGE}>:${GPU_COMPILE_FLAGS}>)

  target_compile_definitions(${GPU_MOD_NAME} PRIVATE
    "-DTORCH_EXTENSION_NAME=${GPU_MOD_NAME}")

  target_include_directories(
    ${GPU_MOD_NAME} PRIVATE
    csrc/include/vajra
    csrc/third_party/flashinfer
    csrc/third_party/fmt/include
    csrc/third_party/ddsketch/include
    csrc/third_party/glog
    csrc/third_party/tokenizers-cpp/include
    ${Python_INCLUDE_DIRS}
    ${GPU_INCLUDE_DIRECTORIES}
  )

  target_link_libraries(${GPU_MOD_NAME} PRIVATE ${TORCH_LIBRARIES}
    ${GPU_LIBRARIES} glog::glog fmt::fmt-header-only nlohmann_json::nlohmann_json tokenizers_cpp)

  install(TARGETS ${GPU_MOD_NAME} LIBRARY DESTINATION ${GPU_DESTINATION})
endfunction()
# Add a function to set the correct compiler flags for test targets
function(set_test_compile_flags TARGET_NAME)
    # Make sure we're using the same ABI settings as PyTorch
    target_compile_definitions(${TARGET_NAME} PRIVATE
        _GLIBCXX_USE_CXX11_ABI=0
    )
    
    # Set C++ standard
    set_property(TARGET ${TARGET_NAME} PROPERTY CXX_STANDARD 17)
    set_property(TARGET ${TARGET_NAME} PROPERTY CXX_STANDARD_REQUIRED ON)
    
    # Add any other needed flags
    if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        target_compile_options(${TARGET_NAME} PRIVATE
            -fPIC
            -Wall
            -Wextra
        )
    endif()
endfunction()

# Modify the add_test_suite function to add test-specific compile flags
function(add_test_suite SUITE_NAME SOURCE_DIR)
    # Separate CPP and CUDA source files
    file(GLOB_RECURSE CPP_TEST_SOURCES "${SOURCE_DIR}/*.cpp")
    file(GLOB_RECURSE CUDA_TEST_SOURCES "${SOURCE_DIR}/*.cu")
    
    if(CPP_TEST_SOURCES OR CUDA_TEST_SOURCES)
        set(ALL_TEST_SOURCES ${CPP_TEST_SOURCES} ${CUDA_TEST_SOURCES})
        add_executable(${SUITE_NAME}_tests ${ALL_TEST_SOURCES})
        
        # First apply our test-specific compiler flags
        set_test_compile_flags(${SUITE_NAME}_tests)
        
        target_include_directories(${SUITE_NAME}_tests PRIVATE 
            ${CMAKE_CURRENT_SOURCE_DIR}/csrc
            ${CMAKE_CURRENT_SOURCE_DIR}/csrc/include/vajra
            ${CMAKE_CURRENT_SOURCE_DIR}/csrc/third_party/flashinfer
            ${CMAKE_CURRENT_SOURCE_DIR}/csrc/third_party/fmt/include
            ${CMAKE_CURRENT_SOURCE_DIR}/csrc/third_party/tokenizers-cpp/include
            ${CMAKE_CURRENT_SOURCE_DIR}/csrc/third_party/ddsketch/include
            ${CMAKE_CURRENT_SOURCE_DIR}/csrc/third_party/glog
            ${CMAKE_CURRENT_SOURCE_DIR}/csrc/third_party/googletest/googletest/include
            ${CMAKE_CURRENT_SOURCE_DIR}/csrc/third_party/googletest/googlemock/include
            ${Python_INCLUDE_DIRS}
        )
        
        # Link with static libraries depending on the suite
        if(${SUITE_NAME} STREQUAL "kernel")
            target_link_libraries(${SUITE_NAME}_tests PRIVATE
                _kernels_common
                _kernels_static
                ${TORCH_LIBRARIES}
                GTest::GTest
                GTest::Main
                GMock::GMock
                fmt::fmt
                glog::glog
                nlohmann_json::nlohmann_json
                pthread
                tokenizers_cpp
            )
        elseif(${SUITE_NAME} STREQUAL "native")
            target_link_libraries(${SUITE_NAME}_tests PRIVATE
                _kernels_common
                _native_static
                Flashinfer::Flashinfer
                ${TORCH_LIBRARIES}
                GTest::GTest
                GTest::Main
                GMock::GMock
                fmt::fmt
                glog::glog
                nlohmann_json::nlohmann_json
                pthread
                tokenizers_cpp
            )
        else()
            target_link_libraries(${SUITE_NAME}_tests PRIVATE
                _kernels_common
                _kernels_static
                _native_static
                Flashinfer::Flashinfer
                ${TORCH_LIBRARIES}
                GTest::GTest
                GTest::Main
                GMock::GMock
                fmt::fmt
                glog::glog
                nlohmann_json::nlohmann_json
                pthread
                tokenizers_cpp
            )
        endif()
        
        # Add Python definitions
        target_compile_definitions(${SUITE_NAME}_tests PRIVATE
            TORCH_EXTENSION_NAME="${SUITE_NAME}_tests"
            PY_MAJOR_VERSION=${Python_VERSION_MAJOR}
            PY_MINOR_VERSION=${Python_VERSION_MINOR}
        )
        
        # Only set CUDA properties for CUDA files
        if(CUDA_TEST_SOURCES)
            foreach(cuda_source ${CUDA_TEST_SOURCES})
                set_source_files_properties(${cuda_source} PROPERTIES LANGUAGE CUDA)
            endforeach()
            
            # Apply CUDA flags ONLY to CUDA files
            if(VAJRA_GPU_FLAGS)
                set_source_files_properties(${CUDA_TEST_SOURCES} PROPERTIES 
                    COMPILE_FLAGS "${VAJRA_GPU_FLAGS}")
            endif()
            
            if (VAJRA_GPU_ARCHES)
                set_target_properties(${SUITE_NAME}_tests PROPERTIES
                    ${VAJRA_GPU_LANG}_ARCHITECTURES "${VAJRA_GPU_ARCHES}")
            endif()
        endif()
        
        # Apply Python linkage to tests
        link_python_to_target(${SUITE_NAME}_tests)
        
        # Add test to CTest with JUnit XML output
        add_test(
            NAME ${SUITE_NAME}_tests 
            COMMAND ${SUITE_NAME}_tests --gtest_output=xml:test_reports/${SUITE_NAME}_tests_results.xml
        )

        # Create directory for test reports if it doesn't exist
        add_custom_command(
            TARGET ${SUITE_NAME}_tests POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E make_directory test_reports
        )
    endif()
endfunction()

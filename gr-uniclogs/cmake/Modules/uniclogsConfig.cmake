INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_UNICLOGS uniclogs)

FIND_PATH(
    UNICLOGS_INCLUDE_DIRS
    NAMES uniclogs/api.h
    HINTS $ENV{UNICLOGS_DIR}/include
        ${PC_UNICLOGS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    UNICLOGS_LIBRARIES
    NAMES gnuradio-uniclogs
    HINTS $ENV{UNICLOGS_DIR}/lib
        ${PC_UNICLOGS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(UNICLOGS DEFAULT_MSG UNICLOGS_LIBRARIES UNICLOGS_INCLUDE_DIRS)
MARK_AS_ADVANCED(UNICLOGS_LIBRARIES UNICLOGS_INCLUDE_DIRS)


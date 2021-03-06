cmake_minimum_required(VERSION 2.8.3)
project(loop_fusion)

set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_CXX_FLAGS "-std=c++11")
#-DEIGEN_USE_MKL_ALL")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g")

if ($ENV{ROS_DISTRO} STREQUAL "indigo")

find_package(catkin REQUIRED COMPONENTS
    roscpp
    std_msgs
    nav_msgs
    camera_models
    cv_bridge_new
    roslib
    )

elseif ($ENV{ROS_DISTRO} STREQUAL "kinetic")

find_package(catkin REQUIRED COMPONENTS
    roscpp
    std_msgs
    nav_msgs
    camera_models
    cv_bridge
    roslib
    )

endif()

# customize opencv dir
      set( OpenCV_DIR /opt/opencv3/share/OpenCV )
      find_package(OpenCV 3.4.1 REQUIRED
                 PATHS /opt/opencv3
                 NO_DEFAULT_PATH)
MESSAGE("OpenCV include dir: " ${OpenCV_INCLUDE_DIRS})
MESSAGE("OpenCV libs: " ${OpenCV_LIBS})

set( Ceres_DIR /opt/ceres/lib/cmake/Ceres )
find_package(Ceres REQUIRED)
MESSAGE("Ceres includes: " ${CERES_INCLUDE_DIRS})
MESSAGE("Ceres libs: " ${CERES_LIBRARIES})

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
find_package(Eigen3)

include_directories(${catkin_INCLUDE_DIRS} ${CERES_INCLUDE_DIRS}  ${EIGEN3_INCLUDE_DIR})

catkin_package()

add_executable(loop_fusion_node
    src/pose_graph_node.cpp
    src/pose_graph.cpp
    src/keyframe.cpp
    src/utility/CameraPoseVisualization.cpp
    src/ThirdParty/DBoW/BowVector.cpp
    src/ThirdParty/DBoW/FBrief.cpp
    src/ThirdParty/DBoW/FeatureVector.cpp
    src/ThirdParty/DBoW/QueryResults.cpp
    src/ThirdParty/DBoW/ScoringObject.cpp
    src/ThirdParty/DUtils/Random.cpp
    src/ThirdParty/DUtils/Timestamp.cpp
    src/ThirdParty/DVision/BRIEF.cpp
    src/ThirdParty/VocabularyBinary.cpp
    )

target_link_libraries(loop_fusion_node ${catkin_LIBRARIES}  ${OpenCV_LIBS} ${CERES_LIBRARIES}) 

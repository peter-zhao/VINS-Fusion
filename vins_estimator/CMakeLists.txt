cmake_minimum_required(VERSION 2.8.3)
project(vins)

set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_CXX_FLAGS "-std=c++11")
#-DEIGEN_USE_MKL_ALL")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g")

if ($ENV{ROS_DISTRO} STREQUAL "indigo")

	find_package(catkin REQUIRED COMPONENTS
	    roscpp
	    std_msgs
	    geometry_msgs
	    nav_msgs
	    tf
	    cv_bridge_new
	    camera_models
	    image_transport)

elseif ($ENV{ROS_DISTRO} STREQUAL "kinetic")

	find_package(catkin REQUIRED COMPONENTS
	    roscpp
	    std_msgs
	    geometry_msgs
	    nav_msgs
	    tf
	    cv_bridge
	    camera_models
	    image_transport)

endif()    
  
# customize opencv dir
set( OpenCV_DIR /opt/opencv3/share/OpenCV )
find_package(OpenCV 3.4.1 REQUIRED
                 PATHS /opt/opencv3
                 NO_DEFAULT_PATH)
MESSAGE("OpenCV include dir: " ${OpenCV_INCLUDE_DIRS})
MESSAGE("OpenCV libs: " ${OpenCV_LIBS})

# message(WARNING "OpenCV_VERSION: ${OpenCV_VERSION}")

set( Ceres_DIR /opt/ceres/lib/cmake/Ceres )
find_package(Ceres REQUIRED)

include_directories(${catkin_INCLUDE_DIRS} ${CERES_INCLUDE_DIRS})

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
find_package(Eigen3)
# set( EIGEN3_INCLUDE_DIR /opt/eigen33/include/eigen3/ )
MESSAGE("EIGEN include dir: " ${EIGEN3_INCLUDE_DIR})

include_directories(
  ${catkin_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIR}
)

catkin_package()

add_library(vins_lib
    src/estimator/parameters.cpp
    src/estimator/estimator.cpp
    src/estimator/feature_manager.cpp
    src/factor/pose_local_parameterization.cpp
    src/factor/projectionTwoFrameOneCamFactor.cpp
    src/factor/projectionTwoFrameTwoCamFactor.cpp
    src/factor/projectionOneFrameTwoCamFactor.cpp
    src/factor/marginalization_factor.cpp
    src/utility/utility.cpp
    src/utility/visualization.cpp
    src/utility/CameraPoseVisualization.cpp
    src/initial/solve_5pts.cpp
    src/initial/initial_aligment.cpp
    src/initial/initial_sfm.cpp
    src/initial/initial_ex_rotation.cpp
    src/featureTracker/feature_tracker.cpp)
target_link_libraries(vins_lib ${catkin_LIBRARIES} ${OpenCV_LIBS} ${CERES_LIBRARIES})


add_executable(vins_node src/rosNodeTest.cpp)
target_link_libraries(vins_node vins_lib) 

add_executable(kitti_odom_test src/KITTIOdomTest.cpp)
target_link_libraries(kitti_odom_test vins_lib) 

add_executable(kitti_gps_test src/KITTIGPSTest.cpp)
target_link_libraries(kitti_gps_test vins_lib) 


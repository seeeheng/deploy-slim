# A slimmer Dockerfile with Ubuntu 18 + ROS Melodic.

# Instructions for use:
1. Choose image you need and build it.
`docker build -f ros-gpu.dockerfile -t cmu-melodic-gpu:1.0 .`
2. Run using ./run.sh, or by the following command:
```
docker run -it \
    --gpus all\
    --env DISPLAY=$DISPLAY \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --privileged \
    <dockertaghere>
```
3. Verify your container's gui is working through a simple test:
roscore  >& /dev/null & rosrun rviz rviz

# CubeSLAM setup
1. Create a catkin_ws and source folder
`mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/src`
2. Source the right setup.bash (/opt/ros/<ros-distribution>/setup.bash)
`source /opt/ros/melodic/setup.bash`
3. Initialize workspace
`catkin_init_workspace`
4. Get cube_slam repository and go into it
`git clone https://github.com/shichaoy/cube_slam && cd cube_slam`
5. Install g2o
`./install_dependenices.sh`
6. Install dependencies for build
```
sudo apt-get update
sudo apt install ros-melodic-pcl-ros
sudo apt install ros-melodic-image-geometry
```
7. Install Pangolin
```
sudo apt install libglew-dev
sudo apt install pkg-config
sudo apt install libegl1-mesa-dev libwayland-dev libxkbcommon-dev wayland-protocols
    
cd ~
git clone https://github.com/stevenlovegrove/Pangolin.git
cd Pangolin
mkdir build && cd build
cmake ..
cmake --build .
```
8a. Add vector and numeric headers in cube_slam files
Go into `/home/developer/catkin_ws/src/cube_slam/detect_3d_cuboid/src/matrix_utils.cpp` and `/home/developer/catkin_ws/src/cube_slam/detect_3d_cuboid/include/detect_3d_cuboid/matrix_utils.h` and affix these to the top of the files:
```
#include <vector>
#include <numeric>
```
8b. Add unistd, stdio and stdlib headers in cube_slam files

Go into `/home/developer/catkin_ws/src/cube_slam/orb_object_slam/src/System.cc`, `vim /home/developer/catkin_ws/src/cube_slam/orb_object_slam/src/Viewer.cc`,
`vim /home/developer/catkin_ws/src/cube_slam/detect_3d_cuboid/src/box_proposal_detail.cpp, and `vim /home/developer/catkin_ws/src/cube_slam/orb_object_slam/src/LoopClosing.cc` and affix these to the top of the files:
```
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
```

9. Make
cd ~/catkin_ws && catkin_make -j4
    
# Interestingness Setup

1. Get Interestingness
```
mkdir -p catkin_ws/src && cd catkin_ws/src
git clone https://github.com/wang-chen/interestingness_ros
cd interestingness_ros
git submodule init
git submodule update
```
2. Download model
```
mkdir saves && cd saves
wget https://github.com/wang-chen/interestingness/releases/download/v2.0/vgg16.pt \
https://github.com/wang-chen/interestingness/releases/download/v2.0/vgg16.pt.SubTF.n100usage.mse
cd ..
mkdir -p data/datasets/SubT && cd data/datasets/SubT
docker cp 250b5:/home/developer/ ~/catkin_ws/src/interestingness_ros/data/
```
    
3. Copy rosbags from host to docker container
From host machine:
```
docker cp <path-to-data> <container_id>:<location>
copy into src/interestingness_ros/data
```
    
4. Setup Python 3 and cv-bridge with Python 3 for ROS Melodic
```
cd ~
mkdir -p catkin_ws_build/src && cd catkin_ws_build/src
sudo apt-get update
sudo apt-get install python3-pip python3-yaml
sudo pip3 install rospkg catkin_pkg
sudo apt-get install python-catkin-tools python3-dev python3-numpy
catkin config -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.6m -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.6m.so
catkin config --install
git clone -b melodic https://github.com/ros-perception/vision_opencv.git
cd ~/catkin_build_ws
catkin build cv_bridge
source install/setup.bash --extend
```

5. Put the following in .bashrc:
```
source /opt/ros/melodic/setup.bash
source ~/catkin_ws/devel/setup.bash
source ~/catkin_build_ws/install/setup.bash --extend # for cv bridge
export ROS_PYTHON_VERSION=3
```
    
6. Get requirements
```
sudo apt install ros-melodic-husky-gazebo
pip3 install --upgrade pip
pip3 install -r /catkin_ws/src/interestingness_ros/interestingness/requirements.txt
```
    
7. Miscellaneous Setup
- Ensure launch files bag location is changed, if needed. (interestingness_ros/launch/subtf_bags.launch, line 4 <arg name="datalocation">)
- Ensure correct robot is being used in launch file.(interestingness_ros/launch/subtf_bags.launch ,line 322 $(arg <>))

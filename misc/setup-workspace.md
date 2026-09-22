
 Create a ROS workspace for the VNAV 


```python
$ mkdir -p ~/vnav_ws/src
$ cd ~/vnav_ws/
$ catkin init
Initializing catkin workspace in `/home/antonap/vnav_ws`.
--------------------------------------------------------------
Profile:                     default
Extending:             [env] /opt/ros/noetic
Workspace:                   /home/antonap/vnav_ws
--------------------------------------------------------------
Build Space:       [missing] /home/antonap/vnav_ws/build
Devel Space:       [missing] /home/antonap/vnav_ws/devel
Install Space:      [unused] /home/antonap/vnav_ws/install
Log Space:         [missing] /home/antonap/vnav_ws/logs
Source Space:       [exists] /home/antonap/vnav_ws/src
DESTDIR:            [unused] None
--------------------------------------------------------------
Devel Space Layout:          linked
Install Space Layout:        None
--------------------------------------------------------------
Additional CMake Args:       None
Additional Make Args:        None
Additional catkin Make Args: None
Internal Make Job Server:    True
Cache Job Environments:      False
--------------------------------------------------------------
Whitelisted Packages:        None
Blacklisted Packages:        None
--------------------------------------------------------------
Workspace configuration appears valid.
--------------------------------------------------------------
```

Getting the Lab code
Go the folder where you cloned the Labs codebase and run git pull. This command will update the folder with the latest code. Let’s suppose we have the codebase in ~/labs. In ~/labs/lab2 you now have the two_drones_pkg folder, which is a ROS package. Copy this folder in your VNAV workspace and build the workspace as follows:

```python
cp -a ~/labs/lab2/two_drones_pkg ~/vnav_ws/src
```

Building the code
Building the code is as easy as running:

```python
catkin build
```

Now that you built the code you see that catkin added a bunch of new folders. In order to use our workspace, we need to make ROS aware of all the components by sourcing the corresponding environment. This is done by running the following in every single terminal where you intend to use the workspace:


```python
source devel/setup.bash
```


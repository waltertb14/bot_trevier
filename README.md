## Bot Trevier
This project implements differential robot for a robot, counts with differential controler, localization algoritmo
required packages:
https://github.com/joshnewans/ball_tracker.git

Run Gazebo simulation:
ros2 launch bot_trevier launch_robot.launch.py

Run ball tracker:
ros2 launch bot_trevier ball_tracker.launch.py sim_mode:=true

VIew rviz simulation:
rviz2 -d src/bot_trevier/config/main.rviz
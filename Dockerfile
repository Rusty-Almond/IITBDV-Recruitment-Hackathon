ARG ROS_DISTRO=humble
FROM osrf/ros:humble-desktop

LABEL maintainer="Vishwam008 <patelvishwam08@gmail.com>"

SHELL ["/bin/bash", "-c"]

# ------------------------------------------------
# Base utilities
# ------------------------------------------------

RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    vim \
    nano \
    dbus-x11 \
    python3-pip \
    sudo \
    libyaml-cpp-dev

# ------------------------------------------------
# Install Gazebo Ignition (Fortress for Humble)
# ------------------------------------------------

RUN apt-get update && apt-get install -y \
    ros-humble-ros-gz \
    ros-humble-ros-gz-sim \
    ros-humble-ros-gz-bridge \
    ros-humble-xacro \
    ros-humble-joint-state-publisher

# ------------------------------------------------
# Create non-root user
# ------------------------------------------------

ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -m --uid $USER_UID --gid $USER_GID $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

# ------------------------------------------------
# ROS environment
# ------------------------------------------------

RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

WORKDIR /home/devuser

CMD ["bash"]

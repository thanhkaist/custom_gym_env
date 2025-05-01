# CUSTOM GYM ENV

Code for making gym environment with mujoco physic simulation from scratch


## Install environment 

```bash
apt-get install -y \
    curl \
    git \
    libgl1-mesa-dev \
    libgl1-mesa-glx \
    libglew-dev \
    libosmesa6-dev \
    software-properties-common \
    net-tools \
    vim \
    virtualenv \
    wget \
    xpra

conda create -n gym_env python==3.10
conda activate gym_env

conda install -c conda-forge patchelf
conda install -c conda-forge libstdcxx-ng 


pip install "cython<3.0"
pip3 install -U 'mujoco-py<2.2,>=2.1'
pip install mujoco==2.3.7
pip install gym==0.23.1

## Add this in bashrc for enable mujoco
export LD_LIBRARY_PATH="/home/dockeruser/.mujoco/mujoco210/bin:${LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH="/usr/local/nvidia/lib64:${LD_LIBRARY_PATH}"

mkdir -p ~/.mujoco \
    && wget https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz -O mujoco.tar.gz \
    && tar -xf mujoco.tar.gz -C ~/.mujoco \
    && rm mujoco.tar.gz

cd ~/.mujoco && wget https://www.roboti.us/file/mjkey.txt 
```

## Layout 

```
custom_gym_env/
├── my_mujoco_env.py           # Gym env
├── assets/
│   └── my_robot.xml           # MJCF model                
├── register.py                # Register for using gym.make
├── test_env.py                # Script to run the env directly
└── test_env_register.py       # Script to run the env with gym.make

```

## Supported features

- Fixed floor, body with 2 joints (slider, hinge)
- Mass (or Inertia) `mass="0.1"`
- Joint dampling (`damping="0.1"`: resists joint motion ), Joint Friction (`frictionloss="0.02"`: resists joint motion), Geom Friction (`friction="1.0 0.005 0.0001"`="sliding torsional1 torsional2": surface contact friction=> sliding: resistance to translational sliding,torsional1, torsional2: friction against rotational movement)
- global friction settings: `<option timestep="0.01" gravity="0 0 -9.8" viscosity="0.002" />`
- contact enable `<geom ... contype="1" conaffinity="1" /> `


## How to run


```
python test_env.py
python test_env_register.py
```

## Q&A

> 1. How can i use URDF model? 

Convert URDF to MJCF with tool [urdf2mjcf](https://github.com/kscalelabs/urdf2mjcf?tab=readme-ov-file) then include the robot in your main xml

```xml
    <!-- Include your MJCF robot (probably inside a <worldbody>) (Make sure my_robot.xml has no <mujoco> header and there is only one <worldbody> in the final merged xml) -->
    <include file="my_robot.xml"/>
```

# SO101 in LIBERO / robosuite

This workspace registers SO101 as a robosuite robot for LIBERO-style tasks.
For SO101 direct sim-to-real references and related prior work, see
`../../../docs/SO101_SIM_TO_REAL_REFERENCES.md`.

The implementation keeps SO101's native embodiment:

```text
arm:     shoulder_pan, shoulder_lift, elbow_flex, wrist_flex, wrist_roll
gripper: gripper
action:  5 joint-position deltas + 1 jaw command = 6D
```

This is intentionally not Panda-compatible 7D OSC control. LIBERO's task,
camera, reset, BDDL, and dataset flow are reused, but the robot action and
proprioception schema follow SO101.

## Generated robosuite XML

The source MJCF remains:

```bash
mujoco/model/so101/so101_new_calib.xml
```

The LeRobot integration generates two robosuite-facing MJCF files:

```bash
mujoco/model/so101/so101_robosuite.xml  # 5DOF arm
mujoco/model/so101/so101_gripper.xml    # 1DOF SO101 jaw gripper
```

The generated arm XML removes the original moving jaw body from the arm and
adds robosuite's `right_hand` mount body. The generated gripper XML contains
the original SO101 moving jaw joint, actuator, and end-effector sites.

## Environment

Use the `lerobot` conda environment:

```bash
conda activate lerobot
export MUJOCO_GL=egl
```

Quick checks:

```bash
python -m compileall \
  lerobot/src/lerobot/envs/libero_robot_utils.py \
  lerobot/src/lerobot/envs/libero_so101.py \
  lerobot/src/lerobot/envs/libero.py \
  lerobot/src/lerobot/envs/configs.py

python -c "from lerobot.envs.libero_so101 import register_so101; print(register_so101())"
```

Minimal LIBERO reset and step:

```bash
python -c "import numpy as np; from lerobot.envs.configs import LiberoEnv; cfg=LiberoEnv(task='libero_object', task_ids=[0], robot='SO101', observation_height=64, observation_width=64, init_states=False); env=cfg.create_envs(1)['libero_object'][0]; obs, _=env.reset(); obs, r, term, trunc, info=env.step(np.zeros(env.action_space.shape, dtype=np.float32)); print(env.action_space, obs['robot_state']['joints']['pos'].shape, obs['robot_state']['gripper']['qpos'].shape); env.close()"
```

Expected vector-env shapes:

```text
action_space: (1, 6)
joint_pos:    (1, 5)
gripper_qpos: (1, 1)
```

GUI sanity check:

```bash
cd /data/seongwoong/git_repo/arm
./run_so101_libero_gui.sh
```

The GUI script uses LIBERO BDDL tasks and robosuite rendering, but it is not a
dataset collector or expert policy. It moves the SO101 end effector toward
LIBERO object poses to verify that the robot registration, placement, gripper,
and renderer are connected correctly.

## Practical Notes

Panda LIBERO checkpoints will not load directly into this SO101 environment
because the action and proprioception dimensions are different. Train or
retarget policies with the SO101 schema.

Dataset collection needs an action source that can solve or attempt the LIBERO
task with SO101: teleoperation, a scripted expert, or a trained SO101 policy.
Saving random joint motion or the GUI sanity-check motion does not produce a
useful LIBERO-style training dataset.

The current SO101 gripper model uses the original MJCF jaw hinge. LeRobot's real
SO101 gripper convention (`0 = closed`, `100 = open`) is not automatically the
same as this MJCF joint range; bridge code is needed before transferring a sim
policy to hardware.

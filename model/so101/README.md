# SO101 Robot - URDF and MuJoCo Description

This repository contains the URDF and MuJoCo (MJCF) files for the SO101 robot.

## Overview

- The robot model files were generated using the [onshape-to-robot](https://github.com/Rhoban/onshape-to-robot) plugin from a CAD model designed in Onshape.
- The generated URDFs were modified to allow meshes with relative paths instead of `package://...`.
- Base collision meshes were removed due to problematic collision behavior during simulation and planning.

## Calibration Methods

The MuJoCo file `scene.xml` supports two differenly calibrated SO101 robot files:

- **New Calibration (Default)**: Each joint's virtual zero is set to the **middle** of its joint range. Use -> `so101_new_calib.xml`. 
- **Old Calibration**: Each joint's virtual zero is set to the configuration where the robot is **fully extended horizontally**. Use -> `so101_old_calib.xml`.

To switch between calibration methods, modify the included robot file in `scene.xml`.

## Motor Parameters

Motor properties for the STS3215 motors used in the robot are adapted from the [Open Duck Mini project](https://github.com/apirrone/Open_Duck_Mini).

## Gripper Note

In LeRobot, the gripper is represented as a **linear joint**, where:

* `0` = fully closed
* `100` = fully open

This hardware mapping is **not yet reflected** in the current URDF and MuJoCo
files.

For LIBERO / robosuite simulation, the integration keeps the SO101 MJCF jaw
hinge as a 1DOF gripper model. See `LIBERO_SO101.md`.

For SO101 sim-to-real references and related prior work, see
`../../../docs/SO101_SIM_TO_REAL_REFERENCES.md`.

## Local Check

This workspace includes `check_model.py`, a small loader for validating the MJCF
and mesh paths:

```bash
python -m pip install mujoco
python mujoco/model/so101/check_model.py
```

For notes on using SO101 with a LIBERO-like LeRobot dataset schema, see
`LIBERO_SO101.md`. For the broader SO101 / sim-to-real reference map, see
`../../../docs/SO101_SIM_TO_REAL_REFERENCES.md`.

---

Feel free to open an issue or contribute improvements!

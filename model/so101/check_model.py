#!/usr/bin/env python3
"""Load-check the SO101 MuJoCo model.

Run from the workspace root after installing the MuJoCo Python package:

    python mujoco/model/so101/check_model.py
"""

from __future__ import annotations

from pathlib import Path

import mujoco


MODEL_DIR = Path(__file__).resolve().parent
SCENE_XML = MODEL_DIR / "scene.xml"


def names(model: mujoco.MjModel, obj_type: mujoco.mjtObj, count: int) -> list[str]:
    return [mujoco.mj_id2name(model, obj_type, i) or f"<unnamed:{i}>" for i in range(count)]


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(SCENE_XML))
    data = mujoco.MjData(model)

    mujoco.mj_forward(model, data)
    mujoco.mj_step(model, data)

    print(f"loaded: {SCENE_XML}")
    print(f"nq={model.nq} nv={model.nv} nu={model.nu} ngeom={model.ngeom}")
    print("joints:", ", ".join(names(model, mujoco.mjtObj.mjOBJ_JOINT, model.njnt)))
    print("actuators:", ", ".join(names(model, mujoco.mjtObj.mjOBJ_ACTUATOR, model.nu)))


if __name__ == "__main__":
    main()

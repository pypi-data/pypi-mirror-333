# Copyright (c) 2022 NVIDIA CORPORATION.  All rights reserved.
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import math
import os

import torch

import warp as wp

from ...environment import IntegratorType, run_env
from ...warp_env import WarpEnv
from .utils.torch_utils import normalize, quat_conjugate, quat_from_angle_axis, quat_mul, quat_rotate


class Ant(WarpEnv):
    sim_name = "Ant" + "DFlex"
    env_offset = (0.0, 0.0, 2.5)

    integrator_type = IntegratorType.FEATHERSTONE
    sim_substeps_featherstone = 16
    featherstone_settings = dict(angular_damping=0.0, update_mass_matrix_every=sim_substeps_featherstone)

    eval_fk = True
    eval_ik = False if integrator_type == IntegratorType.FEATHERSTONE else True

    frame_dt = 1.0 / 60.0
    up_axis = "Y"
    ground_plane = True

    state_tensors_names = ("joint_q", "joint_qd")
    control_tensors_names = ("joint_act",)

    def __init__(self, num_envs=64, episode_length=1000, early_termination=True, **kwargs):
        num_obs = 37
        num_act = 8
        super().__init__(num_envs, num_obs, num_act, episode_length, early_termination, **kwargs)

        self.action_scale = 200.0
        self.termination_height = 0.27
        self.action_penalty = 0.0
        self.joint_vel_obs_scaling = 0.1

    def create_modelbuilder(self):
        builder = super().create_modelbuilder()
        builder.rigid_contact_margin = 0.05
        return builder

    def create_articulation(self, builder):
        wp.sim.parse_mjcf(
            os.path.join(self.asset_dir, "dflex/ant.xml"),
            builder,
            density=1000.0,
            stiffness=0.0,
            damping=1.0,
            contact_ke=4.0e3,
            contact_kd=1.0e3,
            contact_kf=3.0e2,
            contact_mu=0.75,
            contact_restitution=0.0,
            limit_ke=1.0e3,
            limit_kd=1.0e1,
            # armature=0.05,
            armature_scale=5,
            enable_self_collisions=True,
            up_axis="y",
        )

        builder.joint_axis_mode = [wp.sim.JOINT_MODE_FORCE] * len(builder.joint_axis_mode)
        builder.joint_act[:] = [0.0] * len(builder.joint_act)

        builder.joint_q[7:] = [0.0, 1.0, 0.0, -1.0, 0.0, -1.0, 0.0, 1.0]
        builder.joint_q[:7] = [0.0, 0.7, 0.0, *wp.quat_from_axis_angle(wp.vec3(1.0, 0.0, 0.0), -math.pi * 0.5)]
        builder.joint_q[1] = 0.75  # start_height

    def init_sim(self):
        super().init_sim()
        # self.print_model_info()

        with torch.no_grad():
            self.joint_act = wp.to_torch(self.model.joint_act).view(self.num_envs, -1).clone()
            self.joint_act_indices = ...

            self.start_joint_q = self.state.joint_q.view(self.num_envs, -1).clone()
            self.start_joint_qd = self.state.joint_qd.view(self.num_envs, -1).clone()

            self.start_pos = self.start_joint_q[:, :3]
            self.start_rot = list(wp.quat_from_axis_angle((1.0, 0.0, 0.0), -math.pi * 0.5))
            self.start_rotation = torch.tensor(self.start_rot, device=self.device)

            self.x_unit_tensor = torch.tensor([1, 0, 0], dtype=torch.float, device=self.device)
            self.y_unit_tensor = torch.tensor([0, 1, 0], dtype=torch.float, device=self.device)
            self.z_unit_tensor = torch.tensor([0, 0, 1], dtype=torch.float, device=self.device)

            self.x_unit_tensor = self.x_unit_tensor.repeat((self.num_envs, 1))
            self.y_unit_tensor = self.y_unit_tensor.repeat((self.num_envs, 1))
            self.z_unit_tensor = self.z_unit_tensor.repeat((self.num_envs, 1))

            # initialize some data used later on
            # todo - switch to z-up
            self.up_vec = self.y_unit_tensor.clone()
            self.heading_vec = self.x_unit_tensor.clone()
            self.inv_start_rot = quat_conjugate(self.start_rotation).repeat((self.num_envs, 1))

            self.basis_vec0 = self.heading_vec.clone()
            self.basis_vec1 = self.up_vec.clone()

            self.targets = torch.tensor([10000.0, 0.0, 0.0], device=self.device).repeat((self.num_envs, 1))

    @torch.no_grad()
    def randomize_init(self, env_ids):
        joint_q = self.state.joint_q.view(self.num_envs, -1)
        joint_qd = self.state.joint_qd.view(self.num_envs, -1)

        N = len(env_ids)
        num_joint_q = 15
        num_joint_qd = 14

        joint_q[env_ids, 3:7] = self.start_rotation.clone()

        joint_q[env_ids, 0:3] += 0.1 * (torch.rand(size=(N, 3), device=self.device) - 0.5) * 2.0
        angle = (torch.rand(N, device=self.device) - 0.5) * math.pi / 12.0
        axis = torch.nn.functional.normalize(torch.rand((N, 3), device=self.device) - 0.5)
        joint_q[env_ids, 3:7] = quat_mul(joint_q[env_ids, 3:7], quat_from_angle_axis(angle, axis))
        joint_q[env_ids, 7:] += 0.2 * (torch.rand(size=(N, num_joint_q - 7), device=self.device) - 0.5) * 2.0
        joint_qd[env_ids, :] = 0.5 * (torch.rand(size=(N, num_joint_qd), device=self.device) - 0.5)

        # com -> twist velocity
        ang_vel, lin_vel = joint_qd[env_ids, 0:3], joint_qd[env_ids, 3:6]
        joint_qd[env_ids, 3:6] = lin_vel + torch.cross(joint_q[env_ids, 0:3], ang_vel, dim=-1)

    def pre_physics_step(self, actions):
        actions = actions.view(self.num_envs, -1)
        actions = torch.clip(actions, -1.0, 1.0)
        self.actions = actions
        acts = self.action_scale * actions

        acts = -acts  # invert the action direction to match dflex

        if self.joint_act_indices is ...:
            self.control.assign("joint_act", acts.flatten())
        else:
            joint_act = self.scatter_actions(self.joint_act, self.joint_act_indices, acts)
            self.control.assign("joint_act", joint_act.flatten())

    def compute_observations(self):
        joint_q = self.state.joint_q.clone().view(self.num_envs, -1)
        joint_qd = self.state.joint_qd.clone().view(self.num_envs, -1)

        _torso_pos = joint_q[:, 0:3]
        torso_pos = joint_q[:, 0:3] - self.env_offsets
        torso_rot = joint_q[:, 3:7]
        lin_vel = joint_qd[:, 3:6]
        ang_vel = joint_qd[:, 0:3]

        # convert the linear velocity of the torso from twist representation to the velocity of the center of mass in world frame
        lin_vel = lin_vel - torch.cross(_torso_pos, ang_vel, dim=-1)

        to_target = self.targets + (self.start_pos - self.env_offsets) - torso_pos
        to_target[:, 1] = 0.0

        target_dirs = normalize(to_target)
        torso_quat = quat_mul(torso_rot, self.inv_start_rot)

        up_vec = quat_rotate(torso_quat, self.basis_vec1)
        heading_vec = quat_rotate(torso_quat, self.basis_vec0)

        obs_buf = [
            torso_pos[:, 1:2],  # 0
            torso_rot,  # 1:5
            lin_vel,  # 5:8
            ang_vel,  # 8:11
            joint_q.view(self.num_envs, -1)[:, 7:],  # 11:19
            self.joint_vel_obs_scaling * joint_qd.view(self.num_envs, -1)[:, 6:],  # 19:27
            up_vec[:, 1:2],  # 27
            (heading_vec * target_dirs).sum(dim=-1).unsqueeze(-1),  # 28
            self.actions.clone(),  # 29:37
        ]
        self.obs_buf = torch.cat(obs_buf, dim=-1)

    def compute_reward(self):
        up_reward = 0.1 * self.obs_buf[:, 27]
        heading_reward = self.obs_buf[:, 28]
        height_reward = self.obs_buf[:, 0] - self.termination_height
        progress_reward = self.obs_buf[:, 5]

        rew = (
            progress_reward
            + up_reward
            + heading_reward
            + height_reward
            + torch.sum(self.actions**2, dim=-1) * self.action_penalty
        )

        reset_buf, progress_buf = self.reset_buf, self.progress_buf
        max_episode_steps, early_termination = self.episode_length, self.early_termination
        truncated = progress_buf > max_episode_steps - 1
        reset = torch.where(truncated, torch.ones_like(reset_buf), reset_buf)
        if early_termination:
            terminated = self.obs_buf[:, 0] < self.termination_height
            reset = torch.where(terminated, torch.ones_like(reset), reset)
        else:
            terminated = torch.where(torch.zeros_like(reset), torch.ones_like(reset), reset)
        self.rew_buf, self.reset_buf, self.terminated_buf, self.truncated_buf = rew, reset, terminated, truncated


if __name__ == "__main__":
    run_env(Ant)

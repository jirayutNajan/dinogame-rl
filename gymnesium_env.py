import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
from dinogame import DinoGame, Action

class DinoGameEnv(gym.Env):

    metadata = {"render_modes": ["human"]}

    def __init__(self, render_mode=None) -> None:
        super().__init__()
        self.render_mode = render_mode

        # initialize game
        self.game = DinoGame()

        # action idle, jump, sit
        self.action_space = spaces.Discrete(3)

        # observation space
        self.observation_space = spaces.Box(
            low=np.array([0.0, -10.0, -10.0], dtype=np.float32),
            high=np.array([20.0, 999.0, 999.0], dtype=np.float32),
            dtype=np.float32
        )

        # if render mode is human draw a gui
        if self.render_mode == "human":
            pygame.init()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)

        if seed is not None:
            np.random.seed(seed)

        observation = self.game.reset()
        info = {"score": self.game.score}

        if self.render_mode == "human":
            self.render()

        return observation, info

    def step(self, action):
        # map integer action to Action enum
        game_action = Action(action)
        
        if self.render_mode == "human":
            print(f"AI Action: {game_action.name}")

        # truncate คือเงื่อนไขบังคับจบเกม แบบไม่ใช่้ game over
        observation, reward, terminated, truncated, info = self.game.take_action(game_action)
        
        if self.render_mode == "human":
            self.render()

        return observation, reward, terminated, truncated, info

    # TODO: understand later; WTF is this code
    def render(self):
        if self.render_mode == "human":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    return

            self.game.render()

    def close(self):
        self.game.close()

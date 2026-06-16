from stable_baselines3 import PPO
from gymnesium_env import DinoGameEnv

def train_dino(timesteps=100000, render=False):
    """Train dinao AI with PPO"""

    print("Training dinao with PPO")
    print(f"Total timesteps: {timesteps}")
    print("-" * 40)

    # Create environment
    render_mode = "human" if render else None
    env = DinoGameEnv(render_mode=render_mode)

    # Create PPO model
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=0.0003,
        n_steps=2048,
        batch_size=64,
        gamma=0.99,
    )

    # Train the model
    print("Starting training...")
    model.learn(total_timesteps=timesteps)

    # Save the model
    model.save("dinao_model")
    print("Model saved as 'dinao_model'")

    env.close()
    return model

def play_trained_model(model_path="dinao_model", episodes=5):
    """Watch the trained model play"""

    print(f"Loading model: {model_path}")

    # Create environment with rendering
    env = DinoGameEnv(render_mode="human")

    # Load model
    model = PPO.load(model_path, env=env)

    print(f"Watching trained agent play {episodes} episodes...")
    print("Close the window to stop early")

    scores = []
    for episode in range(episodes):
        obs, info = env.reset()
        done = False

        print(f"Episode {episode + 1}:")

        while not done:
            # Get action from model
            action, _ = model.predict(obs, deterministic=True)

            # Take step
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

        score = info.get('score', 0)
        scores.append(score)
        print(f"Score: {score}")

    env.close()

    print(f"\nResults:")
    print(f"Average Score: {sum(scores)/len(scores):.2f}")
    print(f"Best Score: {max(scores)}")

    return scores

def main():
    """Main function with simple command line interface"""
    import sys

    if len(sys.argv) == 1:
        # Default training
        train_dino()
    elif sys.argv[1] == "train":
        # Custom training
        timesteps = int(sys.argv[2]) if len(sys.argv) > 2 else 100000
        render = "--render" in sys.argv
        train_dino(timesteps, render)
    elif sys.argv[1] == "play":
        # Play trained model
        model_path = sys.argv[2] if len(sys.argv) > 2 else "dinao_model"
        episodes = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        play_trained_model(model_path, episodes)
    else:
        print("Usage:")
        print("  python trainning.py                    # Train with defaults")
        print("  python trainning.py train 200000       # Train for 200k steps")
        print("  python trainning.py train 50000 --render # Train with rendering")
        print("  python trainning.py play               # Watch trained model")
        print("  python trainning.py play dinao_model 3 # Watch model play 3 games")

if __name__ == "__main__":
    main()

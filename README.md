# racing-evolutionary-agent

<i>Winner of RythmHack's Most Creative Use of AI and ML Prize Track.</i>

Train your own self-driving race car!  
This game uses the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm to evolve neural networks capable of navigating a pre-designed race track. Tweak parameters, experiment with evolution, and watch each AI generation get better at cornering, avoiding walls, and maintaining speed.

## Features
- AI driver learns automatically through evolution
- Neural networks dynamically grow and mutate (NEAT)
- Interactive gameplay with menu-driven configuration
- Real-time stats and performance display

## Installation

### Requirements
- **Python 3.10 — 3.12** recommended
- **pip** installed

### 1.  Clone the repo
   ```sh
   git clone https://github.com/jmagali/racing-evolutionary-agent.git
   ```
### 2.  In the terminal, navigate to the directory where the repository was cloned, e.g.,
   ```sh
   C:\Users\User\pygame-projects\racing-evolutionary-agent
   ```
### 3.  Install the required Python libraries
   ```sh
   pip install -r requirements.txt # This installs the required libraries
   ```
### 4.  Run the game
   ```sh
   python menu.py # This is the main file
   ```
## How It Works
Each car is controlled by a small neural network. NEAT evolves:
- network weights
- network connections
- hidden nodes (topology)

Cars that drive farther score higher and pass their “genes” to the next generation through:
- crossover
- mutation
- speciation to preserve innovation

Over time, the population learns to race aggressively and efficiently.

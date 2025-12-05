# ⚽ FIFA World Cup 2026 Draw Simulator

A Monte Carlo simulation of the FIFA World Cup 2026 draw with all official restrictions.

## 🎯 What does it do?

This project simulates **100,000 draws** of the FIFA World Cup 2026 and calculates the probability of each possible group combination, with special focus on **Argentina's group**.

### Key Features:
- ✅ Respects all FIFA confederation restrictions (max 2 UEFA, max 1 others per group)
- ✅ Fixed host countries (Mexico/A, Canada/B, USA/D)
- ✅ Handles double-confederation teams (playoff scenarios)
- ✅ Statistical analysis with concentration metrics
- ✅ 100% reproducible results with configurable random seed
- ✅ Complete CSV exports for further analysis

---

## 📊 Project Structure

```
world-cup-2026-draw-simulation/
├── data/                           # Input data
│   ├── bombos.csv                 # Teams organized by pots
│   └── confederaciones.csv        # Team confederations
├── code/                           # Source code modules
│   ├── __init__.py               
│   ├── config.py                  # Configuration parameters
│   ├── data_loader.py             # Data loading and validation
│   ├── simulator.py               # Draw simulation logic
│   ├── analyzer.py                # Statistical analysis
│   └── utils.py                   # Utility functions (export, etc.)
├── output/                         # Generated results (CSVs)
├── notebooks/                      # Jupyter notebooks
│   └── demo_world_cup_draw.ipynb  # Interactive demo
├── run_simulation.py               # Main execution script
├── requirements.txt                # Python dependencies
├── .gitignore
└── README.md                       # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/world-cup-2026-draw-simulation.git
cd world-cup-2026-draw-simulation
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the simulation**
```bash
python run_simulation.py
```

Results will be generated in the `output/` folder as CSV files.

---

## 📈 How it Works

### 1. **Draw Rules**
- 12 groups (A to L)
- 4 teams per group (1 from each pot)
- Draw order: Pot 1 → Pot 4 → Pot 3 → Pot 2

### 2. **Confederation Restrictions**
- **UEFA**: Maximum 2 teams per group
- **Other confederations**: Maximum 1 team per group
- Teams with double confederation (playoffs) can satisfy either restriction

### 3. **Monte Carlo Simulation**
- Runs 100,000 valid draws
- Tracks all possible combinations for Argentina's group
- Calculates probability of each scenario
- Execution time: ~2-3 minutes on modern hardware

---

## 📊 Output Files

The simulation generates timestamped CSV files in the `output/` folder:

1. **`resultados_completos_YYYYMMDD_HHMMSS.csv`**
   - All possible group combinations for Argentina
   - Includes frequency and probability for each

2. **`top_100_combinaciones_YYYYMMDD_HHMMSS.csv`**
   - Top 100 most likely scenarios

3. **`analisis_pot_2_YYYYMMDD_HHMMSS.csv`**
   - Probability of each Pot 2 team facing Argentina

4. **`analisis_pot_3_YYYYMMDD_HHMMSS.csv`**
   - Probability of each Pot 3 team facing Argentina

5. **`analisis_pot_4_YYYYMMDD_HHMMSS.csv`**
   - Probability of each Pot 4 team facing Argentina

6. **`simulation_summary_YYYYMMDD_HHMMSS.csv`**
   - Overall statistics and metrics

### Example Output:
```
Top 3 most likely groups for Argentina:
#1. Argentina + Morocco + Panama + Haiti (0.0234%)
#2. Argentina + Croatia + Egypt + Cape Verde (0.0228%)
#3. Argentina + Uruguay + Scotland + Ghana (0.0221%)
```

---

## ⚙️ Configuration

You can customize the simulation by editing `code/config.py`:

```python
# Number of simulations
NUM_SIMULATIONS = 100000

# Target team for analysis
TARGET_TEAM = 'Argentina'

# Random seed (set to None for true randomness)
RANDOM_SEED = 42

# Confederation restrictions
MAX_UEFA_PER_GROUP = 2
MAX_OTHER_CONF_PER_GROUP = 1
```

---

## 📓 Interactive Notebook

For an interactive experience, use the Jupyter notebook:

```bash
jupyter notebook notebooks/demo_world_cup_draw.ipynb
```

---

## 🛠️ Technical Details

- **Language**: Python 3.8+
- **Key Libraries**: pandas, numpy
- **Algorithm**: Monte Carlo simulation with constraint satisfaction
- **Validation**: Automatic data validation and integrity checks
- **Performance**: ~50,000 simulations/second on modern hardware

---

## 📝 Data Sources

- **Pots**: Based on FIFA rankings as of December 2025
- **Confederations**: Official FIFA confederation assignments
- **Rules**: FIFA World Cup 2026 official draw regulations

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License - Feel free to use and modify

---

## 👤 Author

**[Your Name]**
- Twitter: [@ari_schwartz]
- LinkedIn: [/arielschwartz97]
- GitHub: [@aschwartz97]

---

## 🙏 Acknowledgments

Data based on FIFA rankings and official World Cup 2026 regulations.

---

## 📧 Contact

For questions or suggestions, please open an issue or contact me directly.

---

**⭐ If you found this useful, please star the repository!**
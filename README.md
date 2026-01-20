# Smart Nutrition System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](#license)
[![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen)](#)

**A multi-objective genetic algorithm platform that generates optimal weekly meal plans within budget and caloric constraints.** Features heuristic-driven meal selection, real-time convergence visualization, and comprehensive nutritional analytics for institutional and personal dietary planning.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technical Architecture](#technical-architecture)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Core Algorithms](#core-algorithms)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

---

## Overview

**Smart Nutrition System** solves the complex problem of multi-objective meal planning through advanced optimization algorithms. Users specify their weekly budget and daily caloric targets, along with dietary preferences, and the system intelligently generates a balanced 7-day meal schedule that maximizes accuracy against their objectives while respecting constraints.

### Key Problem Statement
- **Combinatorial Complexity:** 100+ meals across 3 categories per day = billions of possible combinations
- **Multi-Objective Constraints:** Simultaneously optimize budget vs. nutrition
- **Real-World Variability:** Handle dietary restrictions, preferences, and meal variety requirements
- **Time Efficiency:** Generate optimal solutions in real-time for interactive user experience

### Solution Approach
Leverages **Genetic Algorithms (GA)** with domain-specific heuristics (smart sampling) to intelligently explore the meal solution space and converge to near-optimal schedules within seconds.

---

## Features

### Advanced Optimization Engine

| Feature | Description |
|---------|-------------|
| **Multi-Objective Optimization** | Balances budget (50%) and caloric targets (50%) simultaneously |
| **Genetic Algorithm Framework** | Chromosome-based 7-day scheduling with elitist selection, crossover, and adaptive mutation |
| **Smart Sampling Heuristics** | Context-aware meal selection based on user goals (heavy/light/standard) |
| **Soft Constraints** | Meal variety penalties prevent repetitive meal plans |
| **Real-Time Convergence** | Live fitness score tracking across 50-400 configurable generations |
| **Fitness Visualization** | Interactive learning curve showing optimization progress |

### Interactive Dashboard

- **Configuration Sidebar:** Adjust budget, caloric targets, dietary constraints, and algorithm hyperparameters
- **Live Metrics:** Real-time display of cost/calorie accuracy and AI confidence (%)
- **Schedule Table:** 7-day meal plan with daily nutritional and cost breakdown
- **Analytics Dashboard:** 
  - Daily cost consistency chart
  - Budget allocation pie chart (breakfast/lunch/dinner split)
  - Optimization convergence curve
- **Multi-Format Export:** Download meal plans as Excel or PDF reports

### Meal Database

- **120+ Items:** Diverse foods spanning economic to premium options
- **Three Categories:** Breakfast, Lunch, Dinner with cuisine variety
- **Graduated Pricing:** 10-600 EGP reflecting real market conditions
- **Wide Caloric Range:** 70-2000 kcal per meal for flexible targeting
- **Category Filtering:** Exclude food types (Chicken, Meat, Seafood, Dairy, Eggs, Vegetarian)

### Performance Metrics

| Metric | Purpose |
|--------|---------|
| **Optimization Accuracy** | Percentage adherence to budget and caloric targets (0-100%) |
| **Cost Delta** | Variance from target weekly budget in EGP |
| **Calorie Delta** | Daily caloric deviation from target in kcal |
| **Generations** | Configurable evolution iterations (50-400) |
| **Population Size** | Chromosome pool size for diversity (50-300) |

---

## Technical Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                  STREAMLIT UI LAYER                         │
│  (Sidebar Config → Dashboard → Export)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│           GENETIC ALGORITHM ENGINE                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. Population Initialization                        │   │
│  │    - Generate random 7-day schedules               │   │
│  │    - Apply smart sampling heuristics               │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 2. Fitness Evaluation                               │   │
│  │    - Calculate cost error (target vs. actual)       │   │
│  │    - Calculate calorie error                        │   │
│  │    - Apply variety constraints                      │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 3. Selection & Reproduction                         │   │
│  │    - Elitist: retain top-10 individuals            │   │
│  │    - Crossover: single-point day-boundary mixing   │   │
│  │    - Mutation: 20% day regeneration probability    │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│            DATA PROCESSING & ANALYSIS LAYER                 │
│  (Pandas, DataFrame Filtering, Aggregation)                 │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              PERSISTENCE LAYER                              │
│  (Excel I/O, PDF/Excel Export, Caching)                     │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### **1. WeeklySchedule Class (Chromosome)**
```python
class WeeklySchedule:
    - days: List[Dict] → 7 days × (Breakfast, Lunch, Dinner)
    - goal_type: str → 'heavy', 'light', 'standard'
    - fitness: float → Objective function score
    - total_cost: float → Weekly expenditure (EGP)
    - total_cal: float → Weekly caloric intake
    - accuracy: float → Percentage adherence to targets
```

**Key Methods:**
- `_get_smart_sample()` → Context-aware meal selection based on goal
- `_generate_day()` → Creates 3-meal day schedule
- `calculate_fitness()` → Computes weighted error and soft constraints

#### **2. Genetic Algorithm Loop**
```python
def run_genetic_algorithm(b_df, l_df, d_df, budget, cal_target, 
                         pop_size, generations, p_bar, status_txt):
    1. Auto-detect goal (Heavy/Light/Standard) from caloric target
    2. Initialize population with goal-aware heuristics
    3. FOR each generation:
       a. Evaluate fitness for all chromosomes
       b. Sort by fitness (selection pressure)
       c. Elite preservation (top-10)
       d. Breeding: Single-point crossover
       e. Mutation: Adaptive day regeneration
    4. Return best solution & convergence history
```

**Genetic Operators:**
- **Selection:** Elitist (preserve top 10%)
- **Crossover:** Single-point at random day boundary (1-6)
- **Mutation:** 20% probability per offspring
- **Replacement:** Generational model with elitism

#### **3. Objective Function (Fitness)**
$$f(\text{Schedule}) = -\left[\frac{|B_{\text{target}} - B_{\text{actual}}|}{B_{\text{target}}} \times 0.5 + \frac{|C_{\text{target}} - C_{\text{actual}}|}{C_{\text{target}}} \times 0.5 + V_{\text{penalty}}\right]$$

Where:
- $B$ = Weekly budget (EGP)
- $C$ = Weekly calories (kcal)
- $V_{\text{penalty}}$ = Variety constraint (5% per consecutive duplicate lunch)
- Negated for maximization (GA framework)

### Data Flow

```
Input (User Config)
    ↓
Load Database (Excel) → Filter by Constraints
    ↓
Initialize GA Population
    ↓
Evolution Loop (Generations)
    ├─ Fitness Evaluation
    ├─ Selection
    ├─ Genetic Operations
    └─ Real-time UI Updates
    ↓
Best Solution + Convergence History
    ↓
Analytics (Charts, Tables) + Export (PDF/Excel)
```

---

## Installation & Setup

### Prerequisites
- **Python 3.8+**
- **pip** package manager
- **Excel support** (for database generation)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/smart-nutrition-system.git
cd smart-nutrition-system
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Or manually install:**
```bash
pip install streamlit pandas openpyxl fpdf matplotlib scikit-learn
```

### Step 4: Generate Database
```bash
python create_db.py
```

This generates `Smart_System_db.xlsx` with 120+ meal items across categories and meal types.

### Step 5: Run Application
```bash
streamlit run app.py
```

The app will launch at `http://localhost:8501` in your default browser.

---

## Usage Guide

### Basic Workflow

#### **1. Configure Optimization Parameters**

In the left sidebar, adjust:

```
📊 Optimization Targets
├─ Weekly Budget (EGP): 500-10,000 [default: 3,000]
└─ Target Daily Calories: 1,200-5,000 [default: 2,500]

🥗 Dietary Constraints
└─ Exclude Categories: Multi-select from [Chicken, Meat, Seafood, Eggs, Dairy, Vegetarian]

⚙️ Algorithm Settings
├─ Generations: 50-400 [default: 150]
└─ Population Size: 50-300 [default: 100]
```

#### **2. Launch Optimization**
Click **"Run Optimization"** button to execute the genetic algorithm.

**Real-time Feedback:**
- Progress bar showing generation completion
- Live accuracy percentage display
- Processing time: 5-30 seconds depending on parameters

#### **3. Review Results**

**Metrics Cards:**
```
Total Cost      Daily Calories    AI Accuracy
2,850 EGP       2,480 kcal        94.3%
Δ +150 EGP      Δ -20 kcal
```

#### **4. Explore Analytics**

**Tab 1: Schedule**
- 7-day meal plan with daily cost and caloric breakdown
- Sortable and filterable table

**Tab 2: Analytics**
- Daily spending consistency chart
- Budget allocation (breakfast/lunch/dinner split)
- Convergence curve showing AI learning progress

**Tab 3: Export**
- Download as Excel spreadsheet
- Download as formatted PDF report

### Code Example: Custom Usage

```python
import pandas as pd
from app import load_and_filter_data, run_genetic_algorithm

# Load data
b_df, l_df, d_df = load_and_filter_data(excluded_categories=['Seafood'])

# Run optimization
best_plan, convergence_history = run_genetic_algorithm(
    b_df, l_df, d_df,
    budget=3000,           # Weekly budget in EGP
    cal_target=2500*7,     # Weekly calories (daily target × 7)
    pop_size=100,          # Population size
    generations=200,       # GA iterations
    p_bar=None,            # Progress bar (optional)
    status_txt=None        # Status text (optional)
)

# Access results
print(f"Weekly Cost: {best_plan.total_cost} EGP")
print(f"Weekly Calories: {best_plan.total_cal} kcal")
print(f"Accuracy: {best_plan.accuracy:.1f}%")

# Inspect meal plan
for i, day in enumerate(best_plan.days):
    print(f"\nDay {i+1}:")
    print(f"  Breakfast: {day['Breakfast']['Name']} ({day['Breakfast']['Cal']} kcal)")
    print(f"  Lunch: {day['Lunch']['Name']} ({day['Lunch']['Cal']} kcal)")
    print(f"  Dinner: {day['Dinner']['Name']} ({day['Dinner']['Cal']} kcal)")
```

---

## Core Algorithms

### Genetic Algorithm Details

#### **Chromosome Encoding**
Each solution is a 7-day meal plan (21 meal selections):

```
Chromosome = [Day₁, Day₂, Day₃, Day₄, Day₅, Day₆, Day₇]
Dayᵢ = {Breakfast, Lunch, Dinner}
Mealⱼ = {Name, Type, Category, Calories, Price}
```

#### **Fitness Function**

**Normalized Error Calculation:**
```
Cost Error = |Target Budget - Actual Cost| / Target Budget
Cal Error = |Target Calories - Actual Calories| / Target Calories
Variety Penalty = Σ(0.05 for each consecutive duplicate lunch)
Total Error = (Cost Error × 0.5) + (Cal Error × 0.5) + Variety Penalty
Fitness = -Total Error  [Negated for maximization]
```

**Accuracy Metric:**
```
Accuracy (%) = max(0, 100 × (1 - Total Error))
```

#### **Selection Strategy: Elitism**
- **Retain:** Top 10 individuals automatically carry to next generation
- **Breeding:** Select from top 20 individuals for crossover (tournament selection)
- **Survival:** Only fittest survive resource scarcity

#### **Crossover Operation: Single-Point**

```
Parent 1: [Day₁, Day₂, | Day₃, Day₄, Day₅, Day₆, Day₇]
Parent 2: [Day₁', Day₂', | Day₃', Day₄', Day₅', Day₆', Day₇']
          
Crossover Point: Random(1-6)

Child = [Day₁, Day₂, | Day₃', Day₄', Day₅', Day₆', Day₇']
```

#### **Mutation: Adaptive Regeneration**

```
IF random() < 0.2 THEN
    day_index = random(0-6)
    schedule.days[day_index] = _generate_day()  # New 3-meal day
```

### Smart Sampling Heuristic

**Goal-Aware Meal Selection:**

```python
def _get_smart_sample(df, goal_type):
    if goal_type == 'heavy':
        # Select from top 50% calorie meals
        limit = df['Cal'].quantile(0.5)
        subset = df[df['Cal'] >= limit]
        return subset.sample(1)
    
    elif goal_type == 'light':
        # Select from bottom 50% calorie meals
        limit = df['Cal'].quantile(0.5)
        subset = df[df['Cal'] <= limit]
        return subset.sample(1)
    
    else:
        # Standard: uniform random selection
        return df.sample(1)
```

**Auto-Goal Detection:**
```
Daily Target = Caloric Target / 7

IF Daily Target > 2,800 kcal  → HEAVY
ELIF Daily Target < 1,800 kcal → LIGHT
ELSE → STANDARD
```

---

## Project Structure

```
smart-nutrition-system/
│
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
│
├── app.py                            # Main Streamlit application
│   ├── load_and_filter_data()       # Data preprocessing
│   ├── render_sidebar()             # UI configuration controls
│   ├── WeeklySchedule               # Chromosome class
│   ├── run_genetic_algorithm()      # GA engine
│   ├── crossover() / mutate()       # Genetic operators
│   ├── plot_*()                     # Visualization functions
│   ├── export_pdf()                 # Report generation
│   └── main()                       # UI orchestration
│
├── create_db.py                     # Database generation script
│   └── create_professional_database()
│
├── Smart_System_db.xlsx             # Meal database (generated)
│
└── docs/                            # Optional: detailed documentation
    ├── algorithm_details.md
    ├── architecture.md
    └── api_reference.md
```

---

## Visualizations

### Dashboard Screenshots (Placeholder Descriptions)

> **Screenshot 1: Configuration Sidebar**  
> ![Sidebar Configuration](https://via.placeholder.com/400x600?text=Configuration+Sidebar)
> 
> Shows expandable sections for optimization targets, dietary constraints, and algorithm hyperparameters with real-time input validation.

> **Screenshot 2: Results Metrics**  
> ![Metrics Cards](https://via.placeholder.com/600x150?text=Metrics+Cards)
> 
> Displays key performance indicators: total cost vs. target, daily calories, and AI accuracy percentage with delta indicators.

> **Screenshot 3: 7-Day Meal Schedule Table**  
> ![Meal Table](https://via.placeholder.com/800x400?text=Meal+Schedule+Table)
> 
> Interactive table showing daily breakfast, lunch, dinner selections with individual meal costs and calories.

> **Screenshot 4: Analytics Dashboard**  
> ![Analytics Charts](https://via.placeholder.com/800x500?text=Cost+Analysis+%26+Budget+Split)
> 
> Contains:
> - Daily cost consistency bar chart (with target line)
> - Budget allocation pie chart (breakfast/lunch/dinner split)
> - Convergence curve showing fitness improvement over generations

> **Screenshot 5: Optimization Convergence Curve**  
> ![Learning Curve](https://via.placeholder.com/800x300?text=Fitness+Convergence+Over+Generations)
> 
> Line graph showing the genetic algorithm's learning progress, with fitness score on Y-axis and generation count on X-axis.

### Animated GIF Suggestions

| Animation | Description | Suggested Tool |
|-----------|-------------|-----------------|
| **Algorithm Flow Diagram** | Visualize GA loop: initialization → evaluation → selection → crossover → mutation | Manim / Adobe Animate |
| **Meal Selection Heuristic** | Show smart sampling process: dataset filtering → calorie quantile selection → random draw | Streamlit animation |
| **Real-time Convergence** | Live bar chart updating as GA converges | Plotly animated scatter |
| **Budget Allocation Shift** | Pie chart morphing as constraints change | Matplotlib animation |

---

## Configuration Guide

### Algorithm Hyperparameters

| Parameter | Range | Default | Impact |
|-----------|-------|---------|--------|
| **Generations** | 50-400 | 150 | More generations = better convergence but slower computation |
| **Population Size** | 50-300 | 100 | Larger population = more diversity but higher memory usage |
| **Mutation Rate** | (fixed) | 20% | Higher mutation = more exploration, lower convergence |
| **Elite Count** | (fixed) | 10 | Preserves best solutions, prevents loss of good traits |
| **Crossover Type** | (fixed) | Single-point | Preserves meal sequences better than multi-point |

### Budget & Caloric Bounds

**Budget Range:**
- Minimum: 500 EGP/week (~71 EGP/day)
- Maximum: 10,000 EGP/week (~1,429 EGP/day)
- Realistic Range: 2,000-5,000 EGP/week

**Caloric Range:**
- Minimum: 1,200 kcal/day (diet/weight loss)
- Maximum: 5,000 kcal/day (heavy athletes)
- Standard: 2,000-2,500 kcal/day

---

## Contributing

We welcome contributions from researchers, engineers, and nutritionists!

### How to Contribute

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/smart-nutrition-system.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow PEP 8 style guidelines
   - Add docstrings to new functions
   - Include unit tests for algorithmic changes

4. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: description of changes"
   ```

5. **Push to your fork and open a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Contribution Ideas

- **Algorithm Enhancements:**
  - Particle Swarm Optimization (PSO) variant
  - Simulated Annealing integration
  - Multi-objective NSGA-II implementation
  
- **Feature Additions:**
  - Macro/micronutrient tracking (protein, carbs, fats, fiber)
  - Allergen management
  - Seasonal meal preferences
  - Cultural/religious dietary restrictions
  
- **Database Expansion:**
  - International cuisine options
  - Restaurant menu integration
  - Nutritional data API connections
  
- **UI/UX Improvements:**
  - Drag-and-drop meal swapping
  - Real-time recipe suggestions
  - Mobile app adaptation

### Code Review Standards

- All PRs require peer review
- Maintain > 85% code coverage for new features
- Ensure backward compatibility

---

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

**You are free to:**
- Use for commercial or personal projects
- Modify and distribute
- Use privately or publicly

**Under the condition that:**
- Include original license and copyright notice
- Provide a copy of the license

---

## Credits

**Project Developed By:**
- **Isaac** – Data loading & constraint filtering
- **Shaheen** – WeeklySchedule class & fitness function design
- **Adam** – Genetic operators (crossover & mutation)
- **Eyad** – Visualization & analytics module
- **Fady** – Main application orchestration & UI

**Technologies:**
- [Streamlit](https://streamlit.io/) – Interactive web framework
- [Pandas](https://pandas.pydata.org/) – Data manipulation
- [Matplotlib](https://matplotlib.org/) – Scientific visualization
- [FPDF](https://py-pdf.github.io/fpdf2/) – PDF generation

---

## Support & Contact

**For issues, feature requests, or discussions:**
- Open an [Issue](https://github.com/yourusername/smart-nutrition-system/issues)
- Start a [Discussion](https://github.com/yourusername/smart-nutrition-system/discussions)
- Email: contact@smartnutritionsystem.dev

**Documentation:** [Full Docs](./docs/)  
**API Reference:** [docs/api_reference.md](./docs/api_reference.md)

---

## Academic References

This project implements optimization concepts from:

- **Genetic Algorithms:** Holland, J. H. (1975). *Adaptation in Natural and Artificial Systems*
- **Multi-Objective Optimization:** Deb, K. (2001). *Multi-Objective Optimization using Evolutionary Algorithms*
- **Constraint Satisfaction:** Russell & Norvig. *Artificial Intelligence: A Modern Approach*
- **Heuristic Methods:** Michalewicz, Z. *Genetic Algorithms + Data Structures = Evolution Programs*

---

**Last Updated:** January 2026  
**Status:** Active Development  
**Version:** 1.0.0


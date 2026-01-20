import streamlit as st
import pandas as pd
import random
import copy
import io
import matplotlib.pyplot as plt
from fpdf import FPDF


#Isaac
@st.cache_data
def load_and_filter_data(excluded_categories):
    """
    Loads the Excel database and removes excluded food categories.
    """
    try:
        df = pd.read_excel("Smart_System_db.xlsx")
    except FileNotFoundError:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # Apply constraint filtering (Hard Constraints)
    if excluded_categories:
        df = df[~df['Category'].isin(excluded_categories)]

    # Segment data by meal type
    return (
        df[df['Type'] == 'Breakfast'],
        df[df['Type'] == 'Lunch'],
        df[df['Type'] == 'Dinner']
    )

def render_sidebar():
    """
    Renders the sidebar controls and returns user configuration.
    Includes realistic bounds for Budget (500-10000) and Calories (1200-5000).
    """
    st.sidebar.header("System Configuration")
    
    # 1. Optimization Targets
    with st.sidebar.expander("Optimization Targets", expanded=True):
        budget = st.number_input("Weekly Budget (EGP)", 500, 10000, 3000, step=100)
        daily_cal = st.number_input("Target Daily Calories", 1200, 5000, 2500, step=50)

    # 2. Constraints
    with st.sidebar.expander("Dietary Constraints", expanded=True):
        cats = ["Chicken", "Meat", "Seafood", "Eggs", "Dairy", "Vegetarian"]
        excluded = st.multiselect("Exclude Categories:", cats)

    # 3. AI Hyperparameters
    with st.sidebar.expander("Algorithm Settings", expanded=False):
        generations = st.slider("Generations", 50, 400, 150)
        pop_size = st.slider("Population Size", 50, 300, 100)
        
    return budget, daily_cal, excluded, generations, pop_size


# Shaheen 
class WeeklySchedule:
    """
    Represents a single solution (Chromosome) in the population.
    Contains logic for 'Smart Sampling' based on user goals (Heavy vs Light).
    """
    def __init__(self, b_df, l_df, d_df, goal_type='standard', days=None):
        self.b_df = b_df
        self.l_df = l_df
        self.d_df = d_df
        self.goal_type = goal_type  # 'heavy', 'light', or 'standard'
        
        # If days are passed (from crossover), use them. Else, generate new.
        if days:
            self.days = days
        else:
            self.days = [self._generate_day() for _ in range(7)]
        
        # Metrics placeholders
        self.fitness = 0
        self.total_cost = 0
        self.total_cal = 0
        self.accuracy = 0.0

    def _get_smart_sample(self, df):
        """
        Heuristic: Selects meals based on calorie density goals.
        - If Heavy Goal: Picks from top 50% calorie items.
        - If Light Goal: Picks from bottom 50% calorie items.
        """
        if df.empty: return None

        if self.goal_type == 'heavy':
            limit = df['Cal'].quantile(0.5)
            subset = df[df['Cal'] >= limit]
            return subset.sample(1).iloc[0] if not subset.empty else df.sample(1).iloc[0]
            
        elif self.goal_type == 'light':
            limit = df['Cal'].quantile(0.5)
            subset = df[df['Cal'] <= limit]
            return subset.sample(1).iloc[0] if not subset.empty else df.sample(1).iloc[0]
            
        return df.sample(1).iloc[0]

    def _generate_day(self):
        """Creates a full day plan using smart sampling."""
        if self.b_df.empty or self.l_df.empty or self.d_df.empty: return None
        return {
            'Breakfast': self._get_smart_sample(self.b_df),
            'Lunch': self._get_smart_sample(self.l_df),
            'Dinner': self._get_smart_sample(self.d_df)
        }

    def calculate_fitness(self, target_budget, target_cal):
        """
        Objective Function: Calculates how good this schedule is.
        Maximizes accuracy by minimizing the weighted error.
        """
        if not self.days or None in self.days:
            self.fitness = -99999
            return -99999

        # Summation
        self.total_cost = sum(d['Breakfast']['Price'] + d['Lunch']['Price'] + d['Dinner']['Price'] for d in self.days)
        self.total_cal = sum(d['Breakfast']['Cal'] + d['Lunch']['Cal'] + d['Dinner']['Cal'] for d in self.days)
        
        # Normalized Error (Percentage)
        cost_err = abs(target_budget - self.total_cost) / target_budget
        cal_err = abs(target_cal - self.total_cal) / target_cal
        
        # Soft Constraint: Penalize repeated lunches
        variety_penalty = sum(0.05 for i in range(6) if self.days[i]['Lunch']['Name'] == self.days[i+1]['Lunch']['Name'])

        # Final Score (Weighted: 50% Cost, 50% Calories)
        total_error = (cost_err * 0.5) + (cal_err * 0.5) + variety_penalty
        
        self.fitness = -total_error
        self.accuracy = max(0, 100 * (1 - total_error))
        return self.fitness


# Adam
def crossover(p1, p2):
    """Single-point crossover to mix parents."""
    split = random.randint(1, 6)
    new_days = p1.days[:split] + p2.days[split:]
    return WeeklySchedule(p1.b_df, p1.l_df, p1.d_df, goal_type=p1.goal_type, days=copy.deepcopy(new_days))

def mutate(schedule):
    """Randomly regenerates a day to maintain diversity."""
    if random.random() < 0.2: 
        day_idx = random.randint(0, 6)
        schedule.days[day_idx] = schedule._generate_day()

def run_genetic_algorithm(b_df, l_df, d_df, budget, cal_target, pop_size, generations, p_bar, status_txt):
    """
    The Main Optimization Loop.
    1. Heuristic Initialization (Determine Heavy/Light goal).
    2. Evolution over generations.
    """
    # Heuristic: Determine user goal type automatically
    daily_target = cal_target / 7
    goal = 'heavy' if daily_target > 2800 else 'light' if daily_target < 1800 else 'standard'
    
    # Initialize Population
    population = [WeeklySchedule(b_df, l_df, d_df, goal_type=goal) for _ in range(pop_size)]
    history = []
    
    for gen in range(generations):
        # Evaluation
        for ind in population:
            ind.calculate_fitness(budget, cal_target)
        
        # Selection (Sort best first)
        population.sort(key=lambda x: x.fitness, reverse=True)
        history.append(population[0].fitness)
        
        # UI Feedback
        if gen % (generations // 10) == 0:
            p_bar.progress((gen + 1) / generations)
            status_txt.text(f"Gen {gen+1}: Accuracy {population[0].accuracy:.1f}%")

        # Reproduction (Elitism + Breeding)
        next_gen = population[:10] # Keep top 10
        while len(next_gen) < pop_size:
            p1, p2 = random.choice(population[:20]), random.choice(population[:20])
            child = crossover(p1, p2)
            mutate(child)
            next_gen.append(child)
        population = next_gen
        
    return population[0], history


# Eyad
def plot_cost_analysis(schedule, budget):
    """Bar chart for daily cost consistency."""
    days = [f"Day {i+1}" for i in range(7)]
    costs = [d['Breakfast']['Price'] + d['Lunch']['Price'] + d['Dinner']['Price'] for d in schedule.days]
    
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(days, costs, color='#4A90E2', alpha=0.8)
    ax.axhline(y=budget/7, color='red', linestyle='--', label='Target')
    ax.set_title("Daily Spending")
    ax.legend()
    return fig

def plot_budget_split(schedule):
    """Pie chart for meal-type distribution."""
    totals = [
        sum(d['Breakfast']['Price'] for d in schedule.days),
        sum(d['Lunch']['Price'] for d in schedule.days),
        sum(d['Dinner']['Price'] for d in schedule.days)
    ]
    
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.pie(totals, labels=['Breakfast', 'Lunch', 'Dinner'], autopct='%1.1f%%', 
           colors=['#FF9F40', '#36A2EB', '#FF6384'], startangle=90)
    ax.set_title("Budget Allocation")
    return fig

def plot_learning_curve(history):
    """Line chart showing AI improvement over generations."""
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(history, color='green', linewidth=2)
    ax.set_title("Optimization Convergence")
    ax.set_ylabel("Fitness Score")
    ax.set_xlabel("Generation")
    ax.grid(True, alpha=0.3)
    return fig


def export_pdf(df, cost, cal):
    """Generates a PDF report."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Smart Nutrition Plan", ln=True, align='C')
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total Cost: {cost:.1f} EGP | Calories: {int(cal/7)} Kcal/day", ln=True)
    pdf.ln(5)
    
    cols = ["Day", "Breakfast", "Lunch", "Dinner", "Cost", "Cal"]
    widths = [20, 45, 45, 45, 20, 15]
    
    pdf.set_font("Arial", 'B', 8)
    for i, h in enumerate(cols): pdf.cell(widths[i], 10, h, border=1)
    pdf.ln()
    
    pdf.set_font("Arial", size=7)
    for _, row in df.iterrows():
        pdf.cell(widths[0], 10, str(row['Day']), border=1)
        pdf.cell(widths[1], 10, str(row['Breakfast'])[:25], border=1)
        pdf.cell(widths[2], 10, str(row['Lunch'])[:25], border=1)
        pdf.cell(widths[3], 10, str(row['Dinner'])[:25], border=1)
        pdf.cell(widths[4], 10, str(row['Cost']), border=1)
        pdf.cell(widths[5], 10, str(row['Calories']), border=1)
        pdf.ln()
    return pdf.output(dest='S').encode('latin-1')

# Fady
def main():
    st.set_page_config(layout="wide", page_title="Smart Nutrition System App")
    st.title(" Smart Nutrition System")
    
    # 1. Member 1: Inputs
    budget, daily_cal, excluded, generations, pop_size = render_sidebar()

    if st.sidebar.button("Run Optimization", type="primary"):
        # 2. Member 1: Data
        b_df, l_df, d_df = load_and_filter_data(excluded)
        
        if b_df.empty:
            st.error("Error: Constraints too strict.")
        else:
            # 3. Member 3: Engine
            prog_bar = st.progress(0)
            status = st.empty()
            best, history = run_genetic_algorithm(
                b_df, l_df, d_df, budget, daily_cal*7, pop_size, generations, prog_bar, status
            )
            prog_bar.progress(100)
            status.text("Done!")

            # 4. Member 5: Dashboard
            st.divider()
            k1, k2, k3 = st.columns(3)
            diff_c = best.total_cost - budget
            diff_k = (best.total_cal/7) - daily_cal
            
            k1.metric("Total Cost", f"{best.total_cost} EGP", f"{diff_c:+.0f}", delta_color="inverse")
            k2.metric("Daily Calories", f"{int(best.total_cal/7)} Kcal", f"{diff_k:+.0f}")
            k3.metric("AI Accuracy", f"{best.accuracy:.1f}%")

            # Prepare Table
            rows = []
            for i, d in enumerate(best.days):
                rows.append({
                    "Day": f"Day {i+1}",
                    "Breakfast": d['Breakfast']['Name'],
                    "Lunch": d['Lunch']['Name'],
                    "Dinner": d['Dinner']['Name'],
                    "Cost": d['Breakfast']['Price'] + d['Lunch']['Price'] + d['Dinner']['Price'],
                    "Calories": d['Breakfast']['Cal'] + d['Lunch']['Cal'] + d['Dinner']['Cal']
                })
            df_res = pd.DataFrame(rows)

            # Tabs
            t1, t2, t3 = st.tabs([" Schedule", " Analytics", " Export"])
            with t1: st.dataframe(df_res, use_container_width=True, hide_index=True)
            with t2:
                c1, c2 = st.columns(2)
                c1.pyplot(plot_cost_analysis(best, budget))
                c2.pyplot(plot_budget_split(best))
                st.pyplot(plot_learning_curve(history))
            with t3:
                excel_io = io.BytesIO()
                df_res.to_excel(excel_io, index=False); excel_io.seek(0)
                st.download_button("Excel", excel_io, "Plan.xlsx")
                st.download_button("PDF", export_pdf(df_res, best.total_cost, best.total_cal), "Plan.pdf")

if __name__ == "__main__":
    main()
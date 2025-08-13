import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="Financial Independence Calculator",
                   page_subtitle="For Indians",
                   page_icon="💰",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.title("💰 Financial Independence Calculator")
st.markdown(
    "Plan your journey to financial independence with detailed projections and interactive visualizations."
)

# Sidebar for inputs
st.sidebar.header("📊 Financial Parameters")

# Time horizon section
st.sidebar.subheader("🗓️ Time Horizon")
col1, col2 = st.sidebar.columns(2)
with col1:
    start_year = st.number_input("Start Year",
                                 min_value=2020,
                                 max_value=2030,
                                 value=2025,
                                 step=1)
with col2:
    end_year = st.number_input("End Year",
                               min_value=start_year + 1,
                               max_value=2050,
                               value=2037,
                               step=1)

target_corpus = st.sidebar.number_input(
    "Target Corpus (₹)",
    min_value=1000000,
    max_value=500000000,
    value=80000000,
    step=1000000,
    help="Your financial independence target amount")

# Personal details section
st.sidebar.subheader("👫 Personal Details")
col1, col2 = st.sidebar.columns(2)
with col1:
    age_me = st.number_input("Your Current Age",
                             min_value=18,
                             max_value=65,
                             value=33,
                             step=1)
with col2:
    age_wife = st.number_input("Partner's Current Age",
                               min_value=18,
                               max_value=65,
                               value=32,
                               step=1)

# Income section
st.sidebar.subheader("💼 Monthly Income")
salary_me_monthly = st.sidebar.number_input("Your Monthly Salary (₹)",
                                            min_value=10000,
                                            max_value=10000000,
                                            value=195000,
                                            step=5000)
salary_wife_monthly = st.sidebar.number_input("Partner's Monthly Salary (₹)",
                                              min_value=10000,
                                              max_value=10000000,
                                              value=150000,
                                              step=5000)

col1, col2 = st.sidebar.columns(2)
with col1:
    rental_monthly_now = st.number_input("Current Rental Income (₹/month)",
                                         min_value=0,
                                         max_value=1000000,
                                         value=35000,
                                         step=1000)
with col2:
    rental_monthly_future = st.number_input(
        "Future Rental Income (₹/month)",
        min_value=0,
        max_value=1000000,
        value=55000,
        step=1000,
        help="Rental income from 2028 onwards")

income_growth = st.sidebar.slider("Annual Income Growth Rate (%)",
                                  min_value=0.0,
                                  max_value=20.0,
                                  value=5.0,
                                  step=0.5) / 100

# Current assets section
st.sidebar.subheader("💎 Current Assets")
st.sidebar.markdown("**Your Assets:**")
col1, col2 = st.sidebar.columns(2)
with col1:
    stocks_val_me = st.number_input("Your Stocks (₹)",
                                    min_value=0,
                                    max_value=100000000,
                                    value=1500000,
                                    step=50000)
    mf_val_me = st.number_input("Your Mutual Funds (₹)",
                                min_value=0,
                                max_value=100000000,
                                value=1000000,
                                step=50000)
with col2:
    fd_val_me = st.number_input("Your Fixed Deposits (₹)",
                                min_value=0,
                                max_value=100000000,
                                value=500000,
                                step=50000)

st.sidebar.markdown("**Partner's Assets:**")
col1, col2 = st.sidebar.columns(2)
with col1:
    stocks_val_wife = st.number_input("Partner's Stocks (₹)",
                                      min_value=0,
                                      max_value=100000000,
                                      value=1500000,
                                      step=50000)
    mf_val_wife = st.number_input("Partner's Mutual Funds (₹)",
                                  min_value=0,
                                  max_value=100000000,
                                  value=1500000,
                                  step=50000)
with col2:
    fd_val_wife = st.number_input("Partner's Fixed Deposits (₹)",
                                  min_value=0,
                                  max_value=100000000,
                                  value=1500000,
                                  step=50000)

pf_val = st.sidebar.number_input("Combined Provident Fund (₹)",
                                 min_value=0,
                                 max_value=100000000,
                                 value=1500000,
                                 step=50000)

# Calculate total assets
stocks_val = stocks_val_me + stocks_val_wife
mf_val = mf_val_me + mf_val_wife
fd_val = fd_val_me + fd_val_wife

# Growth rates section
st.sidebar.subheader("📈 Expected Returns")
col1, col2 = st.sidebar.columns(2)
with col1:
    stocks_return = st.slider("Stocks Return (%)",
                              min_value=5.0,
                              max_value=25.0,
                              value=12.0,
                              step=0.5) / 100
    mf_return = st.slider("Mutual Funds Return (%)",
                          min_value=5.0,
                          max_value=20.0,
                          value=10.0,
                          step=0.5) / 100
with col2:
    fd_return = st.slider("Fixed Deposits Return (%)",
                          min_value=3.0,
                          max_value=15.0,
                          value=7.0,
                          step=0.5) / 100
    pf_return = st.slider(
        "PF Return (%)", min_value=3.0, max_value=15.0, value=8.0,
        step=0.5) / 100

# Expenses section
st.sidebar.subheader("💸 Monthly Expenses")
col1, col2 = st.sidebar.columns(2)
with col1:
    household_monthly_now = st.number_input(
        "Current Household Expenses (₹/month)",
        min_value=10000,
        max_value=1000000,
        value=50000,
        step=1000)
    household_monthly_future = st.number_input(
        "Future Household Expenses (₹/month)",
        min_value=10000,
        max_value=1000000,
        value=40000,
        step=1000,
        help="From 2028 onwards")
with col2:
    personal_monthly = st.number_input("Personal Expenses (₹/month)",
                                       min_value=5000,
                                       max_value=500000,
                                       value=15000,
                                       step=1000)
    fuel_monthly = st.number_input("Fuel Expenses (₹/month)",
                                   min_value=1000,
                                   max_value=100000,
                                   value=6000,
                                   step=500)

col1, col2 = st.sidebar.columns(2)
with col1:
    inflation_exp = st.slider("General Inflation (%)",
                              min_value=3.0,
                              max_value=15.0,
                              value=7.0,
                              step=0.5) / 100
with col2:
    inflation_fuel = st.slider("Fuel Inflation (%)",
                               min_value=3.0,
                               max_value=15.0,
                               value=5.0,
                               step=0.5) / 100

# Loan EMIs
st.sidebar.subheader("🏠 Loan EMIs")
col1, col2 = st.sidebar.columns(2)
with col1:
    house_loan_emi = st.number_input("House Loan EMI (₹/month)",
                                     min_value=0,
                                     max_value=500000,
                                     value=44000,
                                     step=1000,
                                     key="house_loan_emi")
    house_loan_closure_year = st.number_input("House Loan Closure Year",
                                              min_value=start_year,
                                              max_value=end_year,
                                              value=2028,
                                              step=1,
                                              key="house_loan_closure_year")
with col2:
    car_loan_emi = st.number_input("Car Loan EMI (₹/month)",
                                   min_value=0,
                                   max_value=100000,
                                   value=12500,
                                   step=500,
                                   key="car_loan_emi")
    car_loan_closure_year = st.number_input("Car Loan Closure Year",
                                            min_value=start_year,
                                            max_value=end_year,
                                            value=2027,
                                            step=1,
                                            key="car_loan_closure_year")

# Annual expenses
st.sidebar.subheader("🏖️ Annual Expenses")

# Vacation expenses
col1, col2 = st.sidebar.columns(2)
with col1:
    vacation_annual = st.number_input("Annual Vacation Budget (₹)",
                                      min_value=0,
                                      max_value=10000000,
                                      value=200000,
                                      step=10000,
                                      key="vacation_annual")
with col2:
    vacation_inflation = st.slider("Vacation Inflation (%)",
                                   min_value=3.0,
                                   max_value=15.0,
                                   value=7.0,
                                   step=0.5,
                                   key="vacation_inflation") / 100

# Kids education expenses
col1, col2 = st.sidebar.columns(2)
with col1:
    kids_edu_annual = st.number_input("Annual Kids Education (₹)",
                                      min_value=0,
                                      max_value=10000000,
                                      value=300000,
                                      step=10000,
                                      key="kids_edu_annual")
    kids_edu_start_year = st.number_input("Kids Education Start Year",
                                          min_value=start_year,
                                          max_value=end_year,
                                          value=2028,
                                          step=1,
                                          key="kids_edu_start_year")
with col2:
    kids_edu_end_year = st.number_input("Kids Education End Year",
                                        min_value=kids_edu_start_year,
                                        max_value=end_year,
                                        value=2035,
                                        step=1,
                                        key="kids_edu_end_year")
    kids_edu_inflation = st.slider("Education Inflation (%)",
                                   min_value=3.0,
                                   max_value=20.0,
                                   value=10.0,
                                   step=0.5,
                                   key="kids_edu_inflation") / 100

# Lump sum expenses
st.sidebar.subheader("🎯 Planned Lump Sum Expenses")
col1, col2 = st.sidebar.columns(2)
with col1:
    house_construction_year = st.number_input("House Construction Year",
                                              min_value=start_year,
                                              max_value=end_year,
                                              value=2028,
                                              step=1,
                                              key="house_construction_year")
    house_cost = st.number_input("House Construction Cost (₹)",
                                 min_value=0,
                                 max_value=500000000,
                                 value=10000000,
                                 step=100000,
                                 key="house_cost")
with col2:
    bike_cost = st.number_input("Bike Purchase (₹)",
                                min_value=0,
                                max_value=5000000,
                                value=450000,
                                step=10000,
                                key="bike_cost")
    bike_purchase_year = st.number_input("Bike Purchase Year",
                                         min_value=start_year,
                                         max_value=end_year,
                                         value=2028,
                                         step=1,
                                         key="bike_purchase_year")


# Calculate projections
def calculate_projections():
    rows = []

    # Initialize values for calculations
    curr_stocks_val = stocks_val
    curr_mf_val = mf_val
    curr_fd_val = fd_val
    curr_pf_val = pf_val

    for year in range(start_year, end_year + 1):
        # Age
        curr_age_me = age_me + (year - start_year)
        curr_age_wife = age_wife + (year - start_year)

        # Income
        salary_me = salary_me_monthly * 12 * (
            (1 + income_growth)**(year - start_year))
        salary_wife = salary_wife_monthly * 12 * (
            (1 + income_growth)**(year - start_year))
        rental_income = (rental_monthly_now if year < house_construction_year
                         else rental_monthly_future) * 12
        total_income = salary_me + salary_wife + rental_income

        # Expenses
        household_exp = (
            (household_monthly_now
             if year < house_construction_year else household_monthly_future) *
            ((1 + inflation_exp)**(year - start_year)) * 12)
        personal_exp = personal_monthly * (
            (1 + inflation_exp)**(year - start_year)) * 12
        fuel_exp = fuel_monthly * (
            (1 + inflation_fuel)**(year - start_year)) * 12
        house_loan = house_loan_emi * 12 if year < house_loan_closure_year else 0
        car_loan = car_loan_emi * 12 if year < car_loan_closure_year else 0
        vacation_exp = vacation_annual * (
            (1 + vacation_inflation)**(year - start_year))
        kids_edu = (kids_edu_annual *
                    ((1 + kids_edu_inflation)**(year - start_year))
                    if kids_edu_start_year <= year <= kids_edu_end_year else 0)

        total_exp = household_exp + personal_exp + fuel_exp + house_loan + car_loan + vacation_exp + kids_edu

        # Lump sums
        lump_sum = 0
        if year == house_construction_year:
            lump_sum += house_cost
        if year == bike_purchase_year:
            lump_sum += bike_cost

        # Grow investments first
        curr_stocks_val *= (1 + stocks_return)
        curr_mf_val *= (1 + mf_return)
        curr_fd_val *= (1 + fd_return)
        curr_pf_val *= (1 + pf_return)

        # Annual surplus
        surplus = total_income - total_exp - lump_sum

        # Add surplus to FD
        curr_fd_val += surplus

        total_corpus = curr_stocks_val + curr_mf_val + curr_fd_val + curr_pf_val

        rows.append({
            "Year":
            year,
            "Age Me":
            curr_age_me,
            "Age Wife":
            curr_age_wife,
            "Total Income":
            round(total_income, 0),
            "Total Expenses":
            round(total_exp + lump_sum, 0),
            "Annual Surplus":
            round(surplus, 0),
            "Household Exp":
            round(household_exp, 0),
            "Personal Exp":
            round(personal_exp, 0),
            "Fuel Exp":
            round(fuel_exp, 0),
            "Vacation Exp":
            round(vacation_exp, 0),
            "Kids Education":
            round(kids_edu, 0),
            "House Loan EMI":
            round(house_loan, 0),
            "Car Loan EMI":
            round(car_loan, 0),
            "Lump Sum":
            round(lump_sum, 0),
            "Stocks Value":
            round(curr_stocks_val, 0),
            "MF Value":
            round(curr_mf_val, 0),
            "FD Value":
            round(curr_fd_val, 0),
            "PF Value":
            round(curr_pf_val, 0),
            "Total Corpus":
            round(total_corpus, 0),
            "FI Achieved?":
            "Yes" if total_corpus >= target_corpus else "No"
        })

    return pd.DataFrame(rows)


# Calculate the projections
df = calculate_projections()

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    final_corpus = df.iloc[-1]['Total Corpus']
    st.metric(
        "Final Corpus",
        f"₹{final_corpus:,.0f}",
        delta=f"₹{final_corpus - target_corpus:,.0f}" if final_corpus
        >= target_corpus else f"₹{target_corpus - final_corpus:,.0f} short")

with col2:
    fi_years = df[df['FI Achieved?'] == 'Yes']
    if not fi_years.empty:
        fi_year = fi_years.iloc[0]['Year']
        years_to_fi = fi_year - start_year
        fi_age_me = age_me + years_to_fi
        fi_age_wife = age_wife + years_to_fi
        st.metric("Financial Independence",
                  f"Year {fi_year}",
                  delta=f"Age: You {fi_age_me}, Partner {fi_age_wife}")
    else:
        st.metric("Financial Independence",
                  "Not achieved",
                  delta="Consider adjusting parameters")

with col3:
    progress = min(final_corpus / target_corpus * 100, 100)
    st.metric("Progress to Target", f"{progress:.1f}%")

with col4:
    current_corpus = df.iloc[0]['Total Corpus'] - df.iloc[0]['Annual Surplus']
    st.metric("Current Net Worth", f"₹{current_corpus:,.0f}")

# Financial Independence Achievement Section
fi_years = df[df['FI Achieved?'] == 'Yes']
if not fi_years.empty:
    fi_year = fi_years.iloc[0]['Year']
    years_to_fi = fi_year - start_year
    fi_age_me = age_me + years_to_fi
    fi_age_wife = age_wife + years_to_fi

    st.success(f"🎉 **Financial Independence Achieved in {fi_year}!**")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Years to FI:** {years_to_fi} years")
    with col2:
        st.info(f"**Your age:** {fi_age_me} years")
    with col3:
        st.info(f"**Partner's age:** {fi_age_wife} years")

    # Find the corpus at FI year
    fi_corpus = fi_years.iloc[0]['Total Corpus']
    excess = fi_corpus - target_corpus
    st.success(
        f"💰 **Corpus at FI:** ₹{fi_corpus:,.0f} (₹{excess:,.0f} above target)")

else:
    shortfall = target_corpus - final_corpus
    st.error(f"❌ **Financial Independence not achieved by {end_year}**")
    st.warning(f"⚠️ You are ₹{shortfall:,.0f} short of your target. Consider:")
    st.write("• Increasing your income or income growth rate")
    st.write("• Reducing expenses or lump sum costs")
    st.write("• Extending the time horizon")
    st.write("• Increasing expected returns on investments")

# Inflation Impact Summary
st.markdown("---")
st.subheader("💸 Inflation Impact on Annual Expenses")

final_year_expenses = df.iloc[-1]
col1, col2, col3, col4 = st.columns(4)

with col1:
    current_vacation = vacation_annual
    final_vacation = final_year_expenses['Vacation Exp']
    vacation_growth = (final_vacation / current_vacation -
                       1) * 100 if current_vacation > 0 else 0
    st.metric(
        "Vacation Cost Growth",
        f"₹{current_vacation:,.0f} → ₹{final_vacation:,.0f}",
        delta=f"{vacation_growth:.1f}% over {end_year - start_year} years")

with col2:
    if kids_edu_annual > 0:
        current_education = kids_edu_annual
        final_education = kids_edu_annual * (
            (1 + kids_edu_inflation)**(kids_edu_end_year - start_year))
        education_growth = (final_education / current_education - 1) * 100
        st.metric("Education Cost Growth",
                  f"₹{current_education:,.0f} → ₹{final_education:,.0f}",
                  delta=f"{education_growth:.1f}% over duration")
    else:
        st.metric("Education Cost Growth", "No education expenses", delta="")

with col3:
    current_household = household_monthly_now * 12
    final_household = final_year_expenses['Household Exp']
    household_growth = (final_household / current_household - 1) * 100
    st.metric(
        "Household Cost Growth",
        f"₹{current_household:,.0f} → ₹{final_household:,.0f}",
        delta=f"{household_growth:.1f}% over {end_year - start_year} years")

with col4:
    current_fuel = fuel_monthly * 12
    final_fuel = final_year_expenses['Fuel Exp']
    fuel_growth = (final_fuel / current_fuel - 1) * 100
    st.metric("Fuel Cost Growth",
              f"₹{current_fuel:,.0f} → ₹{final_fuel:,.0f}",
              delta=f"{fuel_growth:.1f}% over {end_year - start_year} years")

# Progress bar
progress_value = min(final_corpus / target_corpus, 1.0)
st.progress(progress_value,
            text=f"Progress to Target: {progress_value*100:.1f}%")

# Tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Projections Table", "📈 Corpus Growth", "🥧 Asset Allocation",
    "📅 Timeline", "📥 Export Data"
])

with tab1:
    st.subheader("Year-by-Year Financial Projections")

    # Format the dataframe for display
    display_df = df.copy()

    # Format currency columns
    currency_cols = [
        'Total Income', 'Total Expenses', 'Annual Surplus', 'Household Exp',
        'Personal Exp', 'Fuel Exp', 'Vacation Exp', 'Kids Education',
        'House Loan EMI', 'Car Loan EMI', 'Lump Sum', 'Stocks Value',
        'MF Value', 'FD Value', 'PF Value', 'Total Corpus'
    ]
    for col in currency_cols:
        display_df[col] = display_df[col].apply(lambda x: f"₹{x:,.0f}")

    # Color code FI achievement
    def highlight_fi(row):
        if row['FI Achieved?'] == 'Yes':
            return ['background-color: #d4edda'] * len(row)
        else:
            return [''] * len(row)

    styled_df = display_df.style.apply(highlight_fi, axis=1)
    st.dataframe(styled_df, use_container_width=True)

with tab2:
    st.subheader("Portfolio Growth Over Time")

    # Create subplot with secondary y-axis
    fig = make_subplots(rows=2,
                        cols=1,
                        subplot_titles=('Total Corpus Growth',
                                        'Asset Breakdown Over Time'),
                        vertical_spacing=0.1,
                        specs=[[{
                            "secondary_y": True
                        }], [{
                            "secondary_y": False
                        }]])

    # Total corpus line chart
    fig.add_trace(go.Scatter(x=df['Year'],
                             y=df['Total Corpus'],
                             mode='lines+markers',
                             name='Total Corpus',
                             line=dict(width=3, color='#1f77b4'),
                             marker=dict(size=8)),
                  row=1,
                  col=1)

    # Target line
    fig.add_hline(y=target_corpus,
                  line_dash="dash",
                  line_color="red",
                  annotation_text=f"Target: ₹{target_corpus:,.0f}",
                  row=1,
                  col=1)

    # Asset breakdown area chart
    fig.add_trace(go.Scatter(x=df['Year'],
                             y=df['Stocks Value'],
                             fill='tonexty',
                             mode='none',
                             name='Stocks',
                             fillcolor='rgba(255, 127, 14, 0.6)'),
                  row=2,
                  col=1)

    fig.add_trace(go.Scatter(x=df['Year'],
                             y=df['Stocks Value'] + df['MF Value'],
                             fill='tonexty',
                             mode='none',
                             name='Mutual Funds',
                             fillcolor='rgba(44, 160, 44, 0.6)'),
                  row=2,
                  col=1)

    fig.add_trace(go.Scatter(x=df['Year'],
                             y=df['Stocks Value'] + df['MF Value'] +
                             df['FD Value'],
                             fill='tonexty',
                             mode='none',
                             name='Fixed Deposits',
                             fillcolor='rgba(214, 39, 40, 0.6)'),
                  row=2,
                  col=1)

    fig.add_trace(go.Scatter(x=df['Year'],
                             y=df['Total Corpus'],
                             fill='tonexty',
                             mode='none',
                             name='Provident Fund',
                             fillcolor='rgba(148, 103, 189, 0.6)'),
                  row=2,
                  col=1)

    fig.update_layout(height=800,
                      showlegend=True,
                      title_text="Financial Portfolio Analysis")

    fig.update_yaxes(title_text="Amount (₹)", row=1, col=1)
    fig.update_yaxes(title_text="Amount (₹)", row=2, col=1)
    fig.update_xaxes(title_text="Year", row=2, col=1)

    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Asset Allocation Analysis")

    # Current vs Final allocation
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Current Allocation**")
        current_data = df.iloc[0]
        current_allocation = [
            current_data['Stocks Value'] - current_data['Annual Surplus'],
            current_data['MF Value'],
            current_data['FD Value'] - current_data['Annual Surplus'],
            current_data['PF Value']
        ]

        fig_current = px.pie(values=[max(0, x) for x in current_allocation],
                             names=[
                                 'Stocks', 'Mutual Funds', 'Fixed Deposits',
                                 'Provident Fund'
                             ],
                             title="Current Asset Allocation")
        st.plotly_chart(fig_current, use_container_width=True)

    with col2:
        st.write("**Final Allocation**")
        final_data = df.iloc[-1]
        final_allocation = [
            final_data['Stocks Value'], final_data['MF Value'],
            final_data['FD Value'], final_data['PF Value']
        ]

        fig_final = px.pie(values=final_allocation,
                           names=[
                               'Stocks', 'Mutual Funds', 'Fixed Deposits',
                               'Provident Fund'
                           ],
                           title=f"Final Asset Allocation ({end_year})")
        st.plotly_chart(fig_final, use_container_width=True)

    # Asset growth comparison
    st.write("**Asset Growth Comparison**")
    asset_growth_df = pd.DataFrame({
        'Asset Type':
        ['Stocks', 'Mutual Funds', 'Fixed Deposits', 'Provident Fund'],
        'Initial Value': [stocks_val, mf_val, fd_val, pf_val],
        'Final Value': [
            final_data['Stocks Value'], final_data['MF Value'],
            final_data['FD Value'], final_data['PF Value']
        ]
    })

    asset_growth_df['Growth'] = asset_growth_df[
        'Final Value'] - asset_growth_df['Initial Value']
    asset_growth_df['Growth %'] = (asset_growth_df['Growth'] /
                                   asset_growth_df['Initial Value'] *
                                   100).round(1)

    fig_growth = px.bar(asset_growth_df,
                        x='Asset Type',
                        y=['Initial Value', 'Final Value'],
                        barmode='group',
                        title="Asset Growth Comparison",
                        labels={
                            'value': 'Amount (₹)',
                            'variable': 'Value Type'
                        })
    st.plotly_chart(fig_growth, use_container_width=True)

    # Display growth table
    st.dataframe(asset_growth_df.style.format({
        'Initial Value': '₹{:,.0f}',
        'Final Value': '₹{:,.0f}',
        'Growth': '₹{:,.0f}',
        'Growth %': '{:.1f}%'
    }),
                 use_container_width=True)

with tab4:
    st.subheader("📅 Financial Timeline & Milestones")

    # Create timeline data
    timeline_events = []

    # Add major expense events
    if house_cost > 0:
        timeline_events.append({
            'Year':
            house_construction_year,
            'Event':
            'House Construction',
            'Amount':
            house_cost,
            'Type':
            'Major Expense',
            'Your Age':
            age_me + (house_construction_year - start_year),
            'Partner Age':
            age_wife + (house_construction_year - start_year)
        })

    if bike_cost > 0:
        timeline_events.append({
            'Year':
            bike_purchase_year,
            'Event':
            'Bike Purchase',
            'Amount':
            bike_cost,
            'Type':
            'Major Expense',
            'Your Age':
            age_me + (bike_purchase_year - start_year),
            'Partner Age':
            age_wife + (bike_purchase_year - start_year)
        })

    # Add kids education start and end
    if kids_edu_annual > 0:
        timeline_events.append({
            'Year':
            kids_edu_start_year,
            'Event':
            'Kids Education Starts',
            'Amount':
            kids_edu_annual,
            'Type':
            'Annual Expense',
            'Your Age':
            age_me + (kids_edu_start_year - start_year),
            'Partner Age':
            age_wife + (kids_edu_start_year - start_year)
        })

        if kids_edu_end_year > kids_edu_start_year:
            timeline_events.append({
                'Year':
                kids_edu_end_year + 1,
                'Event':
                'Kids Education Ends',
                'Amount':
                kids_edu_annual *
                ((1 + kids_edu_inflation)**(kids_edu_end_year - start_year)),
                'Type':
                'Expense End',
                'Your Age':
                age_me + (kids_edu_end_year + 1 - start_year),
                'Partner Age':
                age_wife + (kids_edu_end_year + 1 - start_year)
            })

    # Add loan completion events
    if house_loan_emi > 0:
        timeline_events.append({
            'Year':
            house_loan_closure_year,
            'Event':
            'House Loan Completes',
            'Amount':
            house_loan_emi * 12,
            'Type':
            'Loan End',
            'Your Age':
            age_me + (house_loan_closure_year - start_year),
            'Partner Age':
            age_wife + (house_loan_closure_year - start_year)
        })

    if car_loan_emi > 0:
        timeline_events.append({
            'Year':
            car_loan_closure_year,
            'Event':
            'Car Loan Completes',
            'Amount':
            car_loan_emi * 12,
            'Type':
            'Loan End',
            'Your Age':
            age_me + (car_loan_closure_year - start_year),
            'Partner Age':
            age_wife + (car_loan_closure_year - start_year)
        })

    # Add FI achievement
    fi_years = df[df['FI Achieved?'] == 'Yes']
    if not fi_years.empty:
        fi_year = fi_years.iloc[0]['Year']
        fi_corpus = fi_years.iloc[0]['Total Corpus']
        timeline_events.append({
            'Year': fi_year,
            'Event': '🎉 Financial Independence Achieved!',
            'Amount': fi_corpus,
            'Type': 'Milestone',
            'Your Age': age_me + (fi_year - start_year),
            'Partner Age': age_wife + (fi_year - start_year)
        })

    # Sort by year
    timeline_events = sorted(timeline_events, key=lambda x: x['Year'])

    if timeline_events:
        timeline_df = pd.DataFrame(timeline_events)

        # Create timeline visualization
        fig_timeline = go.Figure()

        # Color mapping for different event types
        color_map = {
            'Major Expense': '#ff6b6b',
            'Annual Expense': '#ffa500',
            'Loan End': '#4ecdc4',
            'Expense End': '#2ecc71',
            'Milestone': '#45b7d1'
        }

        for event_type in timeline_df['Type'].unique():
            type_data = timeline_df[timeline_df['Type'] == event_type]
            fig_timeline.add_trace(
                go.Scatter(
                    x=type_data['Year'],
                    y=[event_type] * len(type_data),
                    mode='markers+text',
                    marker=dict(size=15,
                                color=color_map.get(event_type, '#95a5a6')),
                    text=type_data['Event'],
                    textposition='top center',
                    name=event_type,
                    hovertemplate='<b>%{text}</b><br>' + 'Year: %{x}<br>' +
                    'Amount: ₹%{customdata[0]:,.0f}<br>' +
                    'Your Age: %{customdata[1]}<br>' +
                    'Partner Age: %{customdata[2]}' + '<extra></extra>',
                    customdata=list(
                        zip(type_data['Amount'], type_data['Your Age'],
                            type_data['Partner Age']))))

        fig_timeline.update_layout(title="Financial Timeline & Key Milestones",
                                   xaxis_title="Year",
                                   yaxis_title="Event Type",
                                   height=500,
                                   showlegend=True)

        st.plotly_chart(fig_timeline, use_container_width=True)

        # Display timeline table
        st.subheader("Timeline Details")
        display_timeline = timeline_df.copy()
        display_timeline['Amount'] = display_timeline['Amount'].apply(
            lambda x: f"₹{x:,.0f}")
        st.dataframe(display_timeline, use_container_width=True)
    else:
        st.info(
            "No major timeline events configured. Add house construction, bike purchase, or other expenses to see your financial timeline."
        )

    # Age progression chart
    st.subheader("Age Progression Over Time")
    age_df = df[['Year', 'Age Me', 'Age Wife']].copy()

    fig_age = px.line(age_df.melt(id_vars=['Year'],
                                  value_vars=['Age Me', 'Age Wife'],
                                  var_name='Person',
                                  value_name='Age'),
                      x='Year',
                      y='Age',
                      color='Person',
                      title="Age Progression Timeline",
                      labels={
                          'Age': 'Age (Years)',
                          'Person': 'Family Member'
                      })
    fig_age.update_traces(mode='lines+markers')

    # Mark FI achievement on age chart
    if not fi_years.empty:
        fi_year = fi_years.iloc[0]['Year']
        fi_age_me = age_me + (fi_year - start_year)
        fi_age_wife = age_wife + (fi_year - start_year)

        fig_age.add_vline(
            x=fi_year,
            line_dash="dash",
            line_color="green",
            annotation_text=
            f"FI Achieved<br>You: {fi_age_me}y, Partner: {fi_age_wife}y")

    st.plotly_chart(fig_age, use_container_width=True)

with tab5:
    st.subheader("Export Your Financial Plan")

    st.write("Download your complete financial projections as an Excel file.")

    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Financial Projections', index=False)

        # Add summary sheet
        summary_data = {
            'Parameter': [
                'Target Corpus', 'Final Corpus', 'Years to FI',
                'Current Age (You)', 'Current Age (Partner)',
                'Monthly Salary (You)', 'Monthly Salary (Partner)',
                'Current Rental Income', 'Annual Income Growth',
                'Stocks Return', 'MF Return', 'FD Return', 'PF Return'
            ],
            'Value': [
                f"₹{target_corpus:,.0f}", f"₹{final_corpus:,.0f}",
                f"{fi_years.iloc[0]['Year'] - start_year} years"
                if not fi_years.empty else "Not achieved", age_me, age_wife,
                f"₹{salary_me_monthly:,.0f}", f"₹{salary_wife_monthly:,.0f}",
                f"₹{rental_monthly_now:,.0f}", f"{income_growth*100:.1f}%",
                f"{stocks_return*100:.1f}%", f"{mf_return*100:.1f}%",
                f"{fd_return*100:.1f}%", f"{pf_return*100:.1f}%"
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

    output.seek(0)

    st.download_button(
        label="📥 Download Excel Report",
        data=output.getvalue(),
        file_name=f"financial_plan_{start_year}_{end_year}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Also provide CSV download
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV Data",
        data=csv,
        file_name=f"financial_projections_{start_year}_{end_year}.csv",
        mime="text/csv")

# Footer with key insights
st.markdown("---")
st.subheader("🔍 Key Insights")

col1, col2 = st.columns(2)

with col1:
    total_income_period = df['Total Income'].sum()
    total_expenses_period = df['Total Expenses'].sum()
    savings_rate = (total_income_period -
                    total_expenses_period) / total_income_period * 100

    st.write(f"**Average Savings Rate:** {savings_rate:.1f}%")
    st.write(
        f"**Total Income ({start_year}-{end_year}):** ₹{total_income_period:,.0f}"
    )
    st.write(
        f"**Total Expenses ({start_year}-{end_year}):** ₹{total_expenses_period:,.0f}"
    )

with col2:
    if not fi_years.empty:
        corpus_at_fi = fi_years.iloc[0]['Total Corpus']
        excess_at_end = final_corpus - target_corpus
        st.write(f"**Corpus at FI Achievement:** ₹{corpus_at_fi:,.0f}")
        if excess_at_end > 0:
            st.write(f"**Excess Beyond Target:** ₹{excess_at_end:,.0f}")
    else:
        st.write("**Status:** Target not achieved in the given timeframe")
        st.write(
            "**Recommendation:** Consider increasing income or reducing expenses"
        )

st.markdown("---")
st.markdown("*Built with Streamlit • Financial Independence Calculator*")
import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="SC Architect: Veloce-Tech", layout="wide")

    # --- Header & Context ---
    st.title("🏭 Supply Chain Architect: The Veloce-Tech Challenge")
    st.markdown("""
    **Role:** You are Arjun Nair, COO of Veloce-Tech.
    **Mission:** Design the supply chain for the new **'V-Secure'** home automation line.
    **Challenge:** Your Board demands high profits. You must balance **Cost** (Expenses) against **Responsiveness** (Revenue).
    
    *Hint: Mismatched strategies lead to financial disaster.*
    """)
    
    st.divider()

    # --- sidebar: Dashboard ---
    st.sidebar.header("📋 Strategic Dashboard")
    st.sidebar.info("As you make decisions, costs and potential revenue will fluctuate.")

    # --- PHASE 1: DIAGNOSIS (Understanding Uncertainty) ---
    st.header("Phase 1: Market Diagnosis")
    st.markdown("Analyze the *V-Secure* customer profile to determine the **Implied Demand Uncertainty**.")

    col1, col2 = st.columns(2)
    with col1:
        qty_var = st.slider("Quantity Variance (Demand Swings)", 0, 10, 8, help="How much does order size fluctuate?")
        lead_time = st.slider("Customer Urgency (Lead Time Tolerance)", 0, 10, 9, help="0=Patient, 10=Needs it Yesterday")
    with col2:
        variety = st.slider("Product Variety Required", 0, 10, 8, help="0=Standard Product, 10=Highly Custom")
        innovation = st.slider("Rate of Innovation", 0, 10, 9, help="How fast does the tech become obsolete?")

    # Calculate Uncertainty Score (Average of factors)
    uncertainty_score = (qty_var + lead_time + variety + innovation) / 4
    
    st.caption(f"Calculated Implied Uncertainty Level: **{uncertainty_score}/10**")
    
    if uncertainty_score > 6:
        st.success("Analysis: High Implied Uncertainty detected. Customers demand Responsiveness.")
        target_strategy = "Responsive"
    else:
        st.warning("Analysis: Low Implied Uncertainty. Efficiency might be okay (Are you sure about these inputs?).")
        target_strategy = "Efficient"

    st.divider()

    # --- PHASE 2: SUPPLY CHAIN CONFIGURATION (The Levers) ---
    st.header("Phase 2: Configuration Decisions")
    st.markdown("Choose your strategy for each lever. **Beware:** 'Cheap' decisions save money but may kill sales.")

    # Scoring Variables
    fixed_costs = 0
    revenue_potential = 5000000  # $5M Potential Revenue
    lost_sales_penalty = 0 
    
    # Decisions Dictionary
    decisions = {}

    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("1. Capacity Strategy")
        cap_choice = st.radio(
            "Factory Setup:",
            ["High Utilization (95%)", "Flexible Capacity (70% + Buffer)"],
            key="cap"
        )
        if cap_choice == "High Utilization (95%)":
            decisions['Capacity'] = 'Efficient'
            fixed_costs += 100000       # Low Cost
            lost_sales_penalty += 1500000 # High Lost Sales (Can't meet surges)
        else:
            decisions['Capacity'] = 'Responsive'
            fixed_costs += 500000       # High Cost (Idle machines)
            lost_sales_penalty += 0     # Captures all demand

    with c2:
        st.subheader("2. Inventory Strategy")
        inv_choice = st.radio(
            "Stocking Policy:",
            ["Minimize Inventory (JIT)", "Buffer Inventory (Safety Stock)"],
            key="inv"
        )
        if inv_choice == "Minimize Inventory (JIT)":
            decisions['Inventory'] = 'Efficient'
            fixed_costs += 50000        # Low Holding Cost
            lost_sales_penalty += 1000000 # Stockouts frequent
        else:
            decisions['Inventory'] = 'Responsive'
            fixed_costs += 300000       # High Holding Cost
            lost_sales_penalty += 0     # Product always available

    with c3:
        st.subheader("3. Supplier Selection")
        sup_choice = st.radio(
            "Vendor Criteria:",
            ["Lowest Cost Bidder", "Speed & Flexibility Premium"],
            key="sup"
        )
        if sup_choice == "Lowest Cost Bidder":
            decisions['Supplier'] = 'Efficient'
            fixed_costs += 100000
            lost_sales_penalty += 800000 # Late parts = missed deliveries
        else:
            decisions['Supplier'] = 'Responsive'
            fixed_costs += 400000       # Expensive parts
            lost_sales_penalty += 0

    c4, c5 = st.columns(2)
    with c4:
        st.subheader("4. Transportation")
        trans_choice = st.radio(
            "Logistics Mode:",
            ["Full Truckload (Slow/Cheap)", "Express/Air (Fast/Expensive)"],
            key="trans"
        )
        if trans_choice == "Full Truckload (Slow/Cheap)":
            decisions['Transportation'] = 'Efficient'
            fixed_costs += 50000
            lost_sales_penalty += 500000 # Customer cancels due to wait
        else:
            decisions['Transportation'] = 'Responsive'
            fixed_costs += 250000
            lost_sales_penalty += 0

    with c5:
        st.subheader("5. Pricing Strategy")
        price_choice = st.radio(
            "Price Point:",
            ["Competitive (Low Margin)", "Premium (High Margin)"],
            key="price"
        )
        # Pricing is unique; it changes revenue potential directly
        if price_choice == "Competitive (Low Margin)":
            decisions['Price'] = 'Efficient'
            revenue_potential = 3000000 # Lower potential per unit
        else:
            decisions['Price'] = 'Responsive'
            revenue_potential = 5000000 # High willingness to pay for availability

    st.divider()

    # --- PHASE 3: EVALUATION & SCORING ---
    if st.button("🚀 Run Market Simulation"):
        
        # 1. Calculate Financials
        total_expenses = fixed_costs
        actual_revenue = revenue_potential - lost_sales_penalty
        net_profit = actual_revenue - total_expenses
        
        # 2. Determine "Fit"
        responsive_choices = list(decisions.values()).count('Responsive')
        efficient_choices = list(decisions.values()).count('Efficient')
        
        # Logic: If Uncertainty is HIGH, we need RESPONSIVE choices.
        # If user mixed them, they pay the cost of responsiveness but get the penalty of efficiency (worst case).
        
        st.header("Simulation Results")
        
        # Financial Metrics Display
        m1, m2, m3 = st.columns(3)
        m1.metric("Projected Revenue", f"${revenue_potential:,.0f}")
        m2.metric("Lost Sales (Stockouts)", f"-${lost_sales_penalty:,.0f}", delta_color="inverse")
        m3.metric("Operating Costs", f"-${total_expenses:,.0f}", delta_color="inverse")
        
        st.subheader(f"Net Profit: ${net_profit:,.0f}")
        
        # Strategic Feedback
        if net_profit > 3000000:
            st.balloons()
            st.success(f"**EXCELLENT STRATEGIC FIT!**\nYou recognized that high uncertainty requires a Responsive Supply Chain. You paid extra for flexibility (Buffer, Air Freight), but you captured the high-margin market demand.")
        elif net_profit > 1000000:
            st.warning(f"**MODERATE FIT.**\nYou made some compromises. You likely tried to save cost on a few levers (e.g., using cheap suppliers for a premium product), which caused stockouts and hurt your profit.")
        else:
            st.error(f"**STRATEGIC MISFIT!**\nYou tried to run an 'Efficient' supply chain for a High-Uncertainty product. While your costs were low, your lost sales were massive. The customers went to competitors who could deliver faster.")

        # Show the "Zone of Strategic Fit" Logic
        st.write("---")
        st.markdown(f"**Your Configuration:** {responsive_choices} Responsive Decisions vs {efficient_choices} Efficient Decisions.")
        st.markdown(f"**Market Requirement:** {target_strategy} Supply Chain.")
        
        with st.expander("See Detailed Breakdown"):
            df = pd.DataFrame.from_dict(decisions, orient='index', columns=['Your Strategy'])
            st.table(df)

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import db

# Page Configuration
st.set_page_config(
    page_title="CivicPulse: Local Grievance & Monitoring Portal",
    page_icon="🏛️",
    layout="wide"
)

# Initialize database schema
db.init_db()

# Main Title & Subtitle
st.title("🏛️ CivicPulse: Local Body Grievance & Monitoring Portal")
st.markdown("Streamlining grassroots infrastructure issue reporting and resolution for local administrative bodies.")

# Sidebar Navigation
menu = st.sidebar.radio(
    "Navigation Menu", 
    ["📝 Lodge Complaint", "🔍 Track Status", "📊 Admin & Analytics Dashboard"]
)

# ==========================================
# 1. CITIZEN COMPLAINT LODGING VIEW
# ==========================================
if menu == "📝 Lodge Complaint":
    st.header("Lodge a New Civic Complaint")
    st.markdown("Report local infrastructure bottlenecks such as streetlight failures, water pipeline leaks, or uncollected garbage.")
    
    with st.form("complaint_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            citizen_name = st.text_input("Your Full Name *", placeholder="e.g., Kumar")
            phone_number = st.text_input("Phone Number *", placeholder="10-digit mobile number")
            ward_no = st.selectbox(
                "Ward Number / Area *", 
                ["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5", "Ward 6", "Other / General"]
            )
        
        with col2:
            issue_category = st.selectbox(
                "Issue Category *", 
                ["Water Supply", "Streetlight", "Sanitation & Garbage", "Roads & Potholes", "Drainage / Sewage", "Other"]
            )
            landmark = st.text_input("Location Landmark *", placeholder="e.g., Near Panchayat Office / Bus Stand")
        
        description = st.text_area(
            "Detailed Description of the Issue *", 
            placeholder="Describe the exact problem so maintenance teams can locate and fix it promptly."
        )
        
        submitted = st.form_submit_button("Submit Complaint")
        
        if submitted:
            if not citizen_name or not phone_number or not landmark or not description:
                st.error("Please fill in all mandatory fields marked with an asterisk (*).")
            else:
                ticket_id = db.create_complaint(
                    citizen_name, phone_number, ward_no, issue_category, description, landmark
                )
                st.success(f"Complaint successfully registered! Your Tracking Ticket ID is: **{ticket_id}**")
                st.info("Save this Ticket ID to track the real-time resolution status anytime.")

# ==========================================
# 2. PUBLIC TICKET TRACKING VIEW
# ==========================================
elif menu == "🔍 Track Status":
    st.header("Track Your Complaint Status")
    st.markdown("Enter your unique Ticket ID to inspect live progress and officer remarks.")
    
    col_search1, col_search2 = st.columns([3, 1])
    with col_search1:
        search_id = st.text_input("Enter Tracking Ticket ID", placeholder="e.g., TKT-20261026123045")
    
    with col_search2:
        st.markdown("###") # Vertical alignment spacer
        search_btn = st.button("Search Ticket")
    
    if search_btn or search_id:
        if not search_id:
            st.warning("Please enter a valid Ticket ID.")
        else:
            record = db.get_complaint_by_ticket(search_id)
            if record:
                st.success("Ticket Found!")
                
                # Status visual styling
                status = record['status']
                if status == 'Pending':
                    st.markdown(f"### Current Status: 🔴 **{status}**")
                elif status == 'In Progress':
                    st.markdown(f"### Current Status: 🟠 **{status}**")
                else:
                    st.markdown(f"### Current Status: 🟢 **{status}**")
                
                # Details card layout
                st.markdown("---")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Citizen Name:** {record['citizen_name']}")
                    st.write(f"**Ward / Area:** {record['ward_no']}")
                    st.write(f"**Category:** {record['issue_category']}")
                    st.write(f"**Landmark:** {record['location_landmark']}")
                with col_b:
                    st.write(f"**Logged On:** {record['created_at']}")
                    st.write(f"**Resolved On:** {record['resolved_at'] if record['resolved_at'] else 'Pending Resolution'}")
                
                st.write(f"**Description:** {record['description']}")
                
                if record['admin_notes']:
                    st.info(f"**Officer Action Notes:** {record['admin_notes']}")
            else:
                st.error("No complaint found matching this Ticket ID. Please verify your reference number.")

# ==========================================
# 3. ADMIN & MUNICIPAL DASHBOARD VIEW
# ==========================================
elif menu == "📊 Admin & Analytics Dashboard":
    st.header("Admin & Municipal Officer Dashboard")
    st.markdown("Manage incoming grievances, update resolution statuses, and inspect ward-wise performance metrics.")
    
    # Simple security barrier
    admin_pin = st.text_input("Enter Admin Passkey", type="password", placeholder="Demo Passkey: admin123")
    
    if admin_pin == "admin123" or admin_pin == "admin":
        st.success("Admin Authentication Successful")
        
        df = db.get_all_complaints_df()
        
        if df.empty:
            st.info("No complaints have been registered in the database yet.")
        else:
            # Key Performance Metrics
            total_issues = len(df)
            pending_issues = len(df[df['status'] == 'Pending'])
            in_progress = len(df[df['status'] == 'In Progress'])
            resolved_issues = len(df[df['status'] == 'Resolved'])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Complaints", total_issues)
            col2.metric("Pending Review", pending_issues)
            col3.metric("In Progress", in_progress)
            col4.metric("Resolved", resolved_issues)
            
            st.markdown("---")
            st.subheader("Complaint Queue")
            
            # Filter options
            status_filter = st.selectbox("Filter by Status", ["All", "Pending", "In Progress", "Resolved"])
            filtered_df = df if status_filter == "All" else df[df['status'] == status_filter]
            
            st.dataframe(
                filtered_df[['ticket_id', 'ward_no', 'issue_category', 'citizen_name', 'phone_number', 'status', 'created_at']],
                use_container_width=True
            )
            
            st.markdown("---")
            st.subheader("Update Issue Status & Action Notes")
            
            selected_ticket = st.selectbox("Select Ticket ID", df['ticket_id'].tolist())
            
            if selected_ticket:
                current_record = db.get_complaint_by_ticket(selected_ticket)
                st.write(f"**Selected Ticket:** {selected_ticket} | **Current Status:** {current_record['status']}")
                st.write(f"**Issue Summary:** {current_record['description']}")
                
                with st.form("update_form"):
                    status_options = ["Pending", "In Progress", "Resolved"]
                    default_idx = status_options.index(current_record['status']) if current_record['status'] in status_options else 0
                    
                    new_status = st.selectbox("Update Status", status_options, index=default_idx)
                    admin_notes = st.text_area("Officer Action Notes", value=current_record['admin_notes'] if current_record['admin_notes'] else "")
                    
                    update_submitted = st.form_submit_button("Save Status Update")
                    
                    if update_submitted:
                        db.update_complaint_status(selected_ticket, new_status, admin_notes)
                        st.success(f"Ticket {selected_ticket} successfully updated!")
                        st.rerun()
            
            st.markdown("---")
            st.subheader("Operational Analytics")
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.markdown("##### Issues by Ward")
                ward_counts = df['ward_no'].value_counts()
                st.bar_chart(ward_counts)
                
            with col_chart2:
                st.markdown("##### Issues by Category")
                cat_counts = df['issue_category'].value_counts()
                st.bar_chart(cat_counts)
                
    elif admin_pin:
        st.error("Incorrect Passkey. Use `admin123` for this demo environment.")
    else:
        st.info("Please enter the municipal admin passkey to access management controls. (Demo passkey: `admin123`)")

import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(page_title="Creative Writing AI Agent", layout="wide")

# Title and description
st.title("Creative Writing AI Agent")
st.markdown("Create and manage your content with AI assistance")

# Sidebar for navigation
with st.sidebar:
    page = st.radio("Navigation", ["Create Content", "View Posts", "Analytics"])

# Main content area
if page == "Create Content":
    st.header("Create New Content")
    
    with st.form("content_form"):
        # Content type selection
        content_type = st.selectbox(
            "Content Type",
            ["Blog Post", "Social Media Post", "Article"]
        )
        
        # Content details
        title = st.text_input("Title")
        content = st.text_area("Content", height=300)
        
        # Tags and categories
        tags = st.text_input("Tags (comma-separated)")
        category = st.selectbox(
            "Category",
            ["Technology", "Business", "Lifestyle", "Other"]
        )
        
        # AI assistance options
        st.subheader("AI Assistance")
        use_ai = st.checkbox("Use AI to enhance content")
        if use_ai:
            tone = st.select_slider(
                "Content Tone",
                options=["Professional", "Casual", "Enthusiastic", "Serious"]
            )
            
        # Submit button
        submitted = st.form_submit_button("Create Content")
        
        if submitted:
            st.success("Content created successfully!")
            st.json({
                "type": content_type,
                "title": title,
                "content": content,
                "tags": tags.split(",") if tags else [],
                "category": category,
                "created_at": str(datetime.now()),
                "ai_enhanced": use_ai,
                "tone": tone if use_ai else None
            })

elif page == "View Posts":
    st.header("Your Posts")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_type = st.multiselect(
            "Content Type",
            ["Blog Post", "Social Media Post", "Article"]
        )
    with col2:
        date_range = st.date_input(
            "Date Range",
            [datetime.now()]
        )
    
    # Sample posts (replace with actual data)
    st.write("Sample Post 1")
    st.write("Sample Post 2")

else:  # Analytics
    st.header("Analytics Dashboard")
    
    # Sample metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Posts", "42")
    with col2:
        st.metric("Views", "1,234")
    with col3:
        st.metric("Engagement Rate", "4.7%")
    
    # Sample chart
    st.line_chart({"data": [1, 5, 2, 6, 2, 1]})

# Footer
st.markdown("---")
with st.expander("About"):
    st.write("Creative Writing AI Agent - Helping you create better content")
    st.write("Version 1.0")
import streamlit as st
from datetime import datetime
from content_pipeline.generation.content_generator import ContentGenerator

# Initialize ContentGenerator
content_generator = ContentGenerator()

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
        prompt = st.text_area("Content Brief", 
            "Describe what you want to write about...",
            height=100
        )
        
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
            max_length = st.slider("Maximum Length (words)", 100, 1000, 500)
            
        # Submit button
        submitted = st.form_submit_button("Create Content")
        
        if submitted:
            try:
                if use_ai:
                    with st.spinner("Generating content..."):
                        generated_content = content_generator.generate_content(
                            content_type=content_type.lower(),
                            prompt=prompt,
                            tone=tone.lower(),
                            max_length=max_length
                        )
                        
                        # Store the content
                        content = generated_content
                else:
                    content = prompt

                # Display the content
                st.success("Content created successfully!")
                st.markdown("### Generated Content")
                st.write(content)
                
                # Show metadata
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
                
                # Add download button
                st.download_button(
                    "Download Content",
                    content,
                    file_name=f"{title.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

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
    st.info("This feature will be implemented in the next version")

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
    st.info("Full analytics will be available in the next version")

# Footer
st.markdown("---")
with st.expander("About"):
    st.write("Creative Writing AI Agent - Helping you create better content")
    st.write("Version 1.0")

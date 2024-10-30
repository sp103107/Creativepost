import streamlit as st
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional
import json
import os

# Import your existing classes
from app import (
    PostStatus, PostType, MediaType, Media, PostStorage,
    PostTemplate, TemplateManager, RecurrencePattern,
    ScheduleManager, CreativeWritingAgent
)

# Initialize the CreativeWritingAgent (you'll need to provide credentials)
@st.cache_resource
def init_agent():
    api_key = os.getenv("API_KEY", "your-default-api-key")
    auth_secret = os.getenv("AUTH_SECRET", "your-default-secret")
    social_creds = json.loads(os.getenv("SOCIAL_CREDS", "{}"))
    return CreativeWritingAgent(api_key, auth_secret, social_creds)

agent = init_agent()

# Page config
st.set_page_config(
    page_title="Creative Writing AI Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication
if "user_token" not in st.session_state:
    st.session_state.user_token = None

def login():
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            token = agent.login(email, password)
            if token:
                st.session_state.user_token = token
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# Main navigation
def main():
    if not st.session_state.user_token:
        login()
        return

    # Set current user
    if not agent.set_current_user(st.session_state.user_token):
        st.session_state.user_token = None
        st.error("Session expired. Please login again.")
        st.rerun()
        return

    # Sidebar navigation
    with st.sidebar:
        page = st.radio(
            "Navigation",
            ["Create Content", "Schedule Posts", "Media Library", "Templates", "Analytics"]
        )
        
        if st.button("Logout"):
            st.session_state.user_token = None
            st.rerun()

    # Page content
    if page == "Create Content":
        create_content_page()
    elif page == "Schedule Posts":
        schedule_posts_page()
    elif page == "Media Library":
        media_library_page()
    elif page == "Templates":
        templates_page()
    else:  # Analytics
        analytics_page()

def create_content_page():
    st.header("Create New Content")
    
    with st.form("content_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            post_type = st.selectbox(
                "Post Type",
                [pt.value for pt in PostType]
            )
            
        with col2:
            template = st.selectbox(
                "Use Template",
                ["None"] + [t.name for t in agent.template_manager.list_templates()]
            )
        
        title = st.text_input("Title")
        content = st.text_area("Content", height=200)
        
        col3, col4 = st.columns(2)
        with col3:
            seo_keywords = st.text_input("SEO Keywords (comma-separated)")
        with col4:
            platforms = st.multiselect(
                "Publish to Platforms",
                [p.value for p in Platform]
            )
        
        # AI Assistance
        st.subheader("AI Assistance")
        use_ai = st.checkbox("Use AI to enhance content")
        if use_ai:
            col5, col6 = st.columns(2)
            with col5:
                tone = st.select_slider(
                    "Content Tone",
                    ["Professional", "Casual", "Enthusiastic", "Formal"]
                )
            with col6:
                max_length = st.number_input("Max Length (words)", 100, 5000, 500)
        
        # Media
        st.subheader("Media")
        uploaded_file = st.file_uploader("Add Media", type=['png', 'jpg', 'pdf', 'mp4'])
        
        submitted = st.form_submit_button("Create Post")
        
        if submitted:
            try:
                # Create post
                post = agent.create_post(
                    content=content,
                    post_type=PostType(post_type),
                    industry="general",  # You might want to make this configurable
                    bypass_moderation=False
                )
                
                # Add media if uploaded
                if uploaded_file:
                    # Save uploaded file and add to post
                    file_path = f"uploads/{uploaded_file.name}"
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    agent.add_media_to_post(post, file_path)
                
                # Publish if platforms selected
                if platforms:
                    platform_enums = [Platform(p) for p in platforms]
                    keywords = [k.strip() for k in seo_keywords.split(",")] if seo_keywords else None
                    post = agent.create_and_publish_post(
                        content=content,
                        platforms=platform_enums,
                        seo_keywords=keywords
                    )
                
                st.success("Post created successfully!")
                st.json(post)
                
            except Exception as e:
                st.error(f"Error creating post: {str(e)}")

def schedule_posts_page():
    st.header("Schedule Posts")
    
    # Show upcoming posts
    st.subheader("Upcoming Posts")
    upcoming = agent.schedule_manager.get_upcoming_posts()
    for post in upcoming:
        with st.expander(f"Post {post['post_id']} - {post['schedule_time']}"):
            st.json(post)
    
    # Schedule new post
    st.subheader("Schedule New Post")
    post_id = st.number_input("Post ID", min_value=1)
    schedule_time = st.datetime_input("Schedule Time")
    recurrence = st.selectbox(
        "Recurrence",
        [r.value for r in RecurrencePattern]
    )
    
    if st.button("Schedule"):
        try:
            post = agent.post_storage.load_post(post_id)
            if post:
                success = agent.schedule_post(
                    post,
                    schedule_time,
                    recurrence=RecurrencePattern(recurrence)
                )
                if success:
                    st.success("Post scheduled successfully!")
                else:
                    st.error("Failed to schedule post")
            else:
                st.error("Post not found")
        except Exception as e:
            st.error(f"Error scheduling post: {str(e)}")

def media_library_page():
    st.header("Media Library")
    
    # Display media items
    for media_hash, media in agent.media_library.items():
        with st.expander(f"Media: {media.file_path}"):
            st.write(f"Type: {media.media_type.value}")
            st.write(f"Size: {media.file_size} bytes")
            st.write(f"Hash: {media_hash}")
            
            if media.media_type == MediaType.IMAGE:
                st.image(media.file_path)
            elif media.media_type == MediaType.VIDEO:
                st.video(media.file_path)
            elif media.media_type == MediaType.PDF:
                st.write("PDF preview not available")

def templates_page():
    st.header("Content Templates")
    
    # List existing templates
    st.subheader("Existing Templates")
    for template in agent.template_manager.list_templates():
        with st.expander(template.name):
            st.write("Content:", template.content)
            st.write("Type:", template.post_type.value)
            st.write("Variables:", ", ".join(template.variables))
    
    # Create new template
    st.subheader("Create New Template")
    with st.form("template_form"):
        name = st.text_input("Template Name")
        content = st.text_area("Template Content")
        post_type = st.selectbox(
            "Post Type",
            [pt.value for pt in PostType]
        )
        
        if st.form_submit_button("Create Template"):
            try:
                template = PostTemplate(
                    name=name,
                    content=content,
                    post_type=PostType(post_type),
                    industry="general"  # Make configurable if needed
                )
                agent.template_manager.add_template(template)
                st.success("Template created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating template: {str(e)}")

def analytics_page():
    st.header("Analytics Dashboard")
    
    # Time range selector
    days = st.slider("Time Range (days)", 1, 90, 30)
    
    # Generate report
    report = agent.generate_analytics_report(timedelta(days=days))
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Posts", report.get("total_posts", 0))
    with col2:
        st.metric("Total Views", report.get("total_views", 0))
    with col3:
        st.metric("Engagement Rate", f"{report.get('engagement_rate', 0)}%")
    
    # Display charts
    if "engagement_over_time" in report:
        st.subheader("Engagement Over Time")
        st.line_chart(report["engagement_over_time"])
    
    if "platform_breakdown" in report:
        st.subheader("Platform Breakdown")
        st.bar_chart(report["platform_breakdown"])

if __name__ == "__main__":
    main()

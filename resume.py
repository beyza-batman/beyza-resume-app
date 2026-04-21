import streamlit as st
from PIL import Image, ImageOps, ImageFilter
from fpdf import FPDF
import json
import os

# --- 1. FILE PATHS & STORAGE ---
DB_FILE = "resume_data.json"
SAVE_IMG_PATH = "saved_profile_pic.png"

def load_stored_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_stored_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

saved_info = load_stored_data()

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(page_title="Beyza's Resume", page_icon="💼", layout="wide")

# Recover Photo from Disk if it exists
if "custom_photo" not in st.session_state:
    if os.path.exists(SAVE_IMG_PATH):
        st.session_state.custom_photo = Image.open(SAVE_IMG_PATH)
    else:
        st.session_state.custom_photo = None

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stButton>button {
        width: 100%; border-radius: 5px; height: 3em;
        background-color: #007bff; color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR: EDITABLE INPUTS ---
st.sidebar.title("🛠️ Resume Editor")

with st.sidebar.expander("Personal Info", expanded=True):
    name = st.text_input("Full Name", saved_info.get("name", "ELIF BEYZA SAHIN"))
    email = st.text_input("Email", saved_info.get("email", "elifbeyza2209@gmail.com"))
    location = st.text_input("Location", saved_info.get("location", "Toronto, ON"))
    bio = st.text_area("About Me", saved_info.get("bio", "Motivated and responsible student with strong communication and teamwork skills. Able to manage time well, learn quickly, and take initiative when completing tasks. Looking for an opportunity to gain more work experience while contributing positively to a team and providing excellent service."))

with st.sidebar.expander("Education"):
    edu_info = st.text_area("Education Details", saved_info.get("edu", "Nile Academy | 2023–Present\nHigh School Student"))

with st.sidebar.expander("Skills"):
    skills_text = st.text_area("Skills (comma separated)", saved_info.get("skills", "Leadership, Teamwork, Customer Service, Time Management, Communication, Organization, Problem Solving, Public Interaction"))

with st.sidebar.expander("Relevant Experience"):
    fll_desc = st.text_area("FLL Summer Camp", saved_info.get("fll", "Supervised and led groups of children during daily camp activities. Created a positive and organized environment, encouraged teamwork, and helped campers with tasks and challenges. Demonstrated leadership, responsibility, and strong communication and organizational skills."))
    
    canvassing_desc = st.text_area("Canvassing", saved_info.get("canvassing", "Assisted with community outreach by distributing informational materials to residents on behalf of the office. Helped ensure materials were delivered efficiently while interacting respectfully with members of the public."))
    
    art_desc = st.text_area("Art Vendor Assistant", saved_info.get("art", "Assisted an artist vendor at OCAD Artist Alley with booth setup, organizing and displaying artwork, and labeling products for sale. Interacted with attendees in a friendly and professional manner while helping maintain an organized and visually appealing booth."))
    
    mentor_desc = st.text_area("Mentoring", saved_info.get("mentor", "Mentored younger students by providing academic support, explaining concepts, and encouraging positive study habits. Demonstrated patience, leadership, and strong interpersonal skills."))

with st.sidebar.expander("Extracurricular Activities"):
    extra_curr = st.text_area("Activities", saved_info.get("extra", "- Business/Politics Club (Sept 2025 - Present)\n- Science Academic Club (Sept 2025 - Present)\n- Badminton (Sept 2024 - Present)\n- FIRST Robotics Club (Sept 2024 - Sept 2025)"))

# SAVE BUTTON
if st.sidebar.button("💾 Save All Changes Permanently"):
    current_data = {
        "name": name, "email": email, "location": location, "bio": bio, 
        "skills": skills_text, "fll": fll_desc, "canvassing": canvassing_desc,
        "art": art_desc, "mentor": mentor_desc, "edu": edu_info, 
        "extra": extra_curr
    }
    save_stored_data(current_data)
    st.sidebar.success("Resume saved! Refreshing...")
    st.rerun()

# --- 5. PDF LOGIC (FIXED FOR UNICODE ERRORS) ---
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Helper to fix 'latin-1' encoding errors (replaces fancy dashes/quotes)
    def clean_text(text):
        if text is None: return ""
        # Replaces special characters like \u2013 with a standard hyphen
        return text.encode('latin-1', 'replace').decode('latin-1')

    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 15, clean_text(name), ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, clean_text(f"{email} | {location}"), ln=True, align='C')
    pdf.ln(10)
    
    sections = [
        ("ABOUT ME", bio),
        ("EDUCATION", edu_info),
        ("RELEVANT EXPERIENCE", f"FLL Summer Camp: {fll_desc}\n\nCanvassing: {canvassing_desc}\n\nArt Assistant: {art_desc}\n\nMentoring: {mentor_desc}"),
        ("SKILLS", skills_text),
        ("EXTRACURRICULAR ACTIVITIES", extra_curr)
    ]
    
    for title, content in sections:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, clean_text(title), ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 7, clean_text(content))
        pdf.ln(4)
        
    return pdf.output(dest='S').encode('latin-1')

# --- 6. MAIN NAVIGATION ---
tabs = st.tabs(["📄 My Resume", "🔍 Interactive Photo Editor"])

with tabs[0]:
    col1, col2 = st.columns([1, 2.5], gap="large")
    
    with col1:
        if st.session_state.custom_photo:
            st.image(st.session_state.custom_photo, use_container_width=True)
            if st.button("🗑️ Delete Photo"):
                if os.path.exists(SAVE_IMG_PATH): os.remove(SAVE_IMG_PATH)
                st.session_state.custom_photo = None
                st.rerun()
        else:
            st.image(f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&size=300&background=0D8ABC&color=fff", use_container_width=True)
        
        st.write(f"📫 **Contact:** {email}")
        st.write(f"📍 **Location:** {location}")
        
        # DOWNLOAD BUTTON (Calls the fixed PDF function)
        st.download_button(
            label="📥 Download Resume PDF", 
            data=create_pdf(), 
            file_name=f"{name.replace(' ', '_')}_Resume.pdf", 
            mime="application/pdf"
        )
        
        st.divider()
        st.header("Skills")
        skill_list = [s.strip() for s in skills_text.split(",") if s.strip()]
        for s in skill_list:
            st.markdown(f"✅ **{s}**")

    with col2:
        st.title(name)
        st.subheader("ABOUT ME")
        st.write(bio)
        
        st.divider()
        st.header("EDUCATION")
        st.write(edu_info)
        
        st.divider()
        st.header("RELEVANT EXPERIENCE")
        st.write("**Camp Counselor | First Lego League Summer Camp**")
        st.write(fll_desc)
        st.write("**Canvassing | Anthony Perruza's Office**")
        st.write(canvassing_desc)
        st.write("**Art Vendor Assistant | OCAD Artist Alley**")
        st.write(art_desc)
        st.write("**Mentoring | Nile Academy**")
        st.write(mentor_desc)
        
        st.divider()
        st.header("EXTRACURRICULAR ACTIVITIES")
        st.write(extra_curr)

with tabs[1]:
    st.header("Photo Customization")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=300)
        if st.button("💾 Save Photo Permanently"):
            img.save(SAVE_IMG_PATH)
            st.session_state.custom_photo = img
            st.success("Photo saved!")
            st.rerun()
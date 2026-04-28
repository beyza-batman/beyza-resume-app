import streamlit as st
from PIL import Image, ImageOps, ImageFilter
from fpdf import FPDF
import json
import os

# --- 1. SETUP & STORAGE ---
DB_FILE = "resume_data.json"
SAVE_IMG_PATH = "saved_profile_pic.png"
ADMIN_PASSWORD = "beyza123"  # <--- YOU CAN CHANGE YOUR PASSWORD HERE

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

saved_info = load_data()

# --- 2. PHOTO HANDLER ---
if "custom_photo" not in st.session_state:
    if os.path.exists(SAVE_IMG_PATH):
        st.session_state.custom_photo = Image.open(SAVE_IMG_PATH)
    else:
        st.session_state.custom_photo = None

# --- 3. PAGE SETTINGS ---
st.set_page_config(page_title="Beyza's Resume", layout="wide")

# --- 4. ADMIN LOGIN LOGIC ---
st.sidebar.title("🔐 Admin Access")
pwd_input = st.sidebar.text_input("Enter password to edit", type="password")

if pwd_input == ADMIN_PASSWORD:
    is_admin = True
    st.sidebar.success("Logged in as Admin")
else:
    is_admin = False
    if pwd_input != "":
        st.sidebar.error("Incorrect password")

# --- 5. EDITABLE SIDEBAR (ONLY IF ADMIN) ---
if is_admin:
    st.sidebar.divider()
    st.sidebar.subheader("🛠️ Edit Sections")
    
    with st.sidebar.expander("Personal & Education"):
        name = st.text_input("Name", saved_info.get("name", "ELIF BEYZA SAHIN"))
        email = st.text_input("Email", saved_info.get("email", "elifbeyza2209@gmail.com"))
        location = st.text_input("Location", saved_info.get("location", "Toronto, ON"))
        bio = st.text_area("About Me", saved_info.get("bio", "Motivated student..."))
        edu = st.text_area("Education", saved_info.get("edu", "Nile Academy | 2023–Present"))

    with st.sidebar.expander("Work Experience"):
        fll = st.text_area("FLL Camp", saved_info.get("fll", "Supervised children..."))
        canv = st.text_area("Canvassing", saved_info.get("canvassing", "Outreach work..."))
        art = st.text_area("Art Assistant", saved_info.get("art", "Booth setup..."))
        ment = st.text_area("Mentoring", saved_info.get("mentor", "Academic support..."))

    with st.sidebar.expander("Skills & Extra"):
        skills = st.text_area("Skills", saved_info.get("skills", "Leadership, Teamwork"))
        extra = st.text_area("Activities", saved_info.get("extra", "- Robotics Club"))

    if st.sidebar.button("💾 Save All Changes"):
        data_to_save = {
            "name": name, "email": email, "location": location, "bio": bio,
            "edu": edu, "fll": fll, "canvassing": canv, "art": art,
            "mentor": ment, "skills": skills, "extra": extra
        }
        save_data(data_to_save)
        st.rerun()
else:
    # If not admin, use the saved info or defaults automatically
    name = saved_info.get("name", "ELIF BEYZA SAHIN")
    email = saved_info.get("email", "elifbeyza2209@gmail.com")
    location = saved_info.get("location", "Toronto, ON")
    bio = saved_info.get("bio", "Motivated student...")
    edu = saved_info.get("edu", "Nile Academy | 2023–Present")
    fll = saved_info.get("fll", "Supervised children...")
    canv = saved_info.get("canvassing", "Outreach work...")
    art = saved_info.get("art", "Booth setup...")
    ment = saved_info.get("mentor", "Academic support...")
    skills = saved_info.get("skills", "Leadership, Teamwork")
    extra = saved_info.get("extra", "- Robotics Club")

# --- 6. PDF GENERATOR ---
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    def clean(t): return str(t).encode('latin-1', 'replace').decode('latin-1')
    
    pdf.set_fill_color(13, 138, 188)
    pdf.rect(0, 0, 65, 300, 'F')
    
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_xy(5, 50)
    pdf.cell(55, 10, "CONTACT", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.set_x(5)
    pdf.multi_cell(55, 6, clean(email))
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(75, 20)
    pdf.set_font("Arial", 'B', 25)
    pdf.cell(120, 15, clean(name), ln=True)
    
    sections = [("ABOUT ME", bio), ("EDUCATION", edu), ("SKILLS", skills), ("EXTRACURRICULAR", extra)]
    for title, content in sections:
        pdf.set_x(75)
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 10, title, ln=True)
        pdf.line(75, pdf.get_y(), 200, pdf.get_y())
        pdf.set_x(75)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(120, 6, clean(content))
        pdf.ln(5)
    return pdf.output(dest='S').encode('latin-1')

# --- 7. MAIN INTERFACE ---
# If admin, show both tabs. If guest, show only the Resume tab.
if is_admin:
    tab1, tab2 = st.tabs(["📄 Resume View", "🔍 Admin: Photo Editor"])
else:
    tab1 = st.container() # Just a container, no tabs for guests

with tab1:
    col1, col2 = st.columns([1, 2.5])
    with col1:
        if st.session_state.custom_photo:
            st.image(st.session_state.custom_photo, use_container_width=True)
        else:
            st.image(f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&size=300&background=0D8ABC&color=fff")
        
        st.write(f"📫 {email}")
        st.write(f"📍 {location}")
        st.download_button("📥 Download PDF", data=create_pdf(), file_name="Resume.pdf")

    with col2:
        st.title(name)
        st.subheader("ABOUT ME")
        st.write(bio)
        st.divider()
        st.subheader("EDUCATION")
        st.write(edu)
        st.divider()
        st.subheader("EXPERIENCE")
        st.write(f"**FLL Camp:** {fll}")
        st.write(f"**Canvassing:** {canv}")
        st.write(f"**Art Assistant:** {art}")
        st.write(f"**Mentoring:** {ment}")
        st.divider()
        st.subheader("SKILLS")
        st.write(skills)

if is_admin:
    with tab2:
        st.header("Admin: Photo Editor")
        file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
        if file:
            img = Image.open(file)
            st.image(img, width=300)
            if st.button("💾 Save Photo"):
                img.save(SAVE_IMG_PATH)
                st.session_state.custom_photo = img
                st.rerun()
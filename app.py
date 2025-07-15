import streamlit as st
from utils.whisper_utils import transcribe_audio
from utils.llm_utils import generate_summary, generate_notes, generate_flashcards
from utils.file_export_utils import generate_pdf, generate_docx

import os

# Page config
st.set_page_config(
    page_title="LLM Smart Notes Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- Initialize Session State -------------------
if 'content_generated' not in st.session_state:
    st.session_state.content_generated = False
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'notes' not in st.session_state:
    st.session_state.notes = ""
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = ""
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'file_processed' not in st.session_state:
    st.session_state.file_processed = False
if 'current_file_name' not in st.session_state:
    st.session_state.current_file_name = ""

# ------------------- Sidebar -------------------
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    st.markdown("---")
    
    # Settings
    st.markdown("### 📊 Output Options")
    show_word_count = st.checkbox("Show word count", value=True)
    enable_auto_scroll = st.checkbox("Auto-scroll to results", value=True)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This app uses:
    - **Whisper** for audio transcription
    - **GPT** for content generation
    - **Streamlit** for the interface
    """)

# ------------------- Dark Theme Colors (Fixed) -------------------
theme_config = {
    'page_bg': '#0e1117',
    'secondary_bg': '#1e1e2e',
    'card_bg': '#262638',
    'text_primary': '#ffffff',
    'text_secondary': '#a6adc8',
    'accent_color': '#89b4fa',
    'success_color': '#a6e3a1',
    'warning_color': '#f9e2af',
    'error_color': '#f38ba8',
    'border_color': '#45475a',
    'sidebar_bg': '#181825',
    'input_bg': '#313244',
    'hover_bg': '#383848'
}

# ------------------- Enhanced CSS Styling -------------------
st.markdown(f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    html, body, .stApp {{
        background-color: {theme_config['page_bg']};
        color: {theme_config['text_primary']};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {theme_config['sidebar_bg']};
        border-right: 1px solid {theme_config['border_color']};
    }}
    
    section[data-testid="stSidebar"] > div {{
        padding-top: 2rem;
    }}
    
    /* Sidebar text and labels */
    .stSidebar [data-testid="stMarkdownContainer"] p,
    .stSidebar label,
    .stSidebar .stSelectbox label,
    .stSidebar .stCheckbox label {{
        color: {theme_config['text_primary']} !important;
        font-weight: 500;
    }}
    
    /* Main content area */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: {theme_config['text_primary']} !important;
        font-weight: 600;
    }}
    
    h1 {{
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
        color: white !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {theme_config['accent_color']}, {theme_config['success_color']});
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }}
    
    /* File uploader */
    .stFileUploader {{
        background-color: {theme_config['card_bg']};
        border: 2px dashed {theme_config['border_color']};
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }}
    
    .stFileUploader:hover {{
        border-color: {theme_config['accent_color']};
        background-color: {theme_config['hover_bg']};
    }}
    
    .stFileUploader label {{
        color: {theme_config['text_primary']} !important;
        font-size: 1.1rem;
        font-weight: 500;
    }}
    
    /* Text areas */
    .stTextArea > div > div > textarea {{
        background-color: {theme_config['input_bg']};
        color: {theme_config['text_primary']};
        border: 1px solid {theme_config['border_color']};
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        line-height: 1.6;
    }}
    
    /* Select boxes */
    .stSelectbox > div > div {{
        background-color: {theme_config['input_bg']};
        border: 1px solid {theme_config['border_color']};
        border-radius: 8px;
    }}
    
    /* Checkboxes */
    .stCheckbox > label > div {{
        background-color: {theme_config['input_bg']};
        border: 1px solid {theme_config['border_color']};
    }}
    
    /* Enhanced output boxes */
    .content-card {{
        background: {theme_config['card_bg']};
        border: 1px solid {theme_config['border_color']};
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .content-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, {theme_config['accent_color']}, {theme_config['success_color']});
    }}
    
    .content-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    }}
    
    .content-card h3 {{
        margin-top: 0;
        color: {theme_config['accent_color']} !important;
        font-size: 1.4rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .content-card .content {{
        color: {theme_config['text_primary']};
        line-height: 1.8;
        font-size: 1rem;
    }}
    
    /* Word count badge */
    .word-count {{
        display: inline-block;
        background: {theme_config['accent_color']};
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-left: 1rem;
    }}
    
    /* Status messages */
    .stSuccess > div {{
        background-color: {theme_config['success_color']}20;
        border: 1px solid {theme_config['success_color']};
        color: {theme_config['success_color']};
        border-radius: 8px;
    }}
    
    .stInfo > div {{
        background-color: {theme_config['accent_color']}20;
        border: 1px solid {theme_config['accent_color']};
        color: {theme_config['accent_color']};
        border-radius: 8px;
    }}
    
    .stWarning > div {{
        background-color: {theme_config['warning_color']}20;
        border: 1px solid {theme_config['warning_color']};
        color: {theme_config['warning_color']};
        border-radius: 8px;
    }}
    
    /* Expander */
    .stExpander > div > div {{
        background-color: {theme_config['card_bg']};
        border: 1px solid {theme_config['border_color']};
        border-radius: 12px;
    }}
    
    /* Spinner */
    .stSpinner > div {{
        border-top-color: {theme_config['accent_color']} !important;
    }}
    
    /* Progress bar */
    .stProgress > div > div > div {{
        background: linear-gradient(135deg, {theme_config['accent_color']}, {theme_config['success_color']});
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 1rem;
        }}
        
        h1 {{
            font-size: 2rem !important;
        }}
        
        .content-card {{
            padding: 1.5rem;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# ------------------- Helper Functions -------------------
def count_words(text):
    return len(text.split()) if text else 0

def create_content_card(title, content, icon="", word_count=None):
    word_badge = f"<span class='word-count'>{word_count} words</span>" if word_count and show_word_count else ""
    
    return f"""
    <div class="content-card">
        <h3>{icon} {title}{word_badge}</h3>
        <div class="content">{content}</div>
    </div>
    """

# ------------------- Main App -------------------
# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🧠 Smart Notes Generator")
    st.markdown("Transform your lectures into **summaries**, **organized notes**, and **flashcards** using AI")

with col2:
    # Dark mode indicator
    st.markdown(f"<div style='text-align: right; font-size: 2rem; margin-top: 1rem;'>🌙</div>", unsafe_allow_html=True)

st.markdown("---")

# ------------------- File Upload Section -------------------
st.markdown('<div class="upload-section-title">📤 Upload Your Content</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Choose your lecture file",
        type=["mp3", "wav", "txt", "m4a", "ogg"],
        help="Supported formats: MP3, WAV, M4A, OGG, TXT"
    )

with col2:
    if uploaded_file:
        file_info = f"""
        **📄 File Info:**
        - **Name:** {uploaded_file.name}
        - **Size:** {uploaded_file.size / 1024:.1f} KB
        - **Type:** {uploaded_file.type}
        """
        st.markdown(file_info)

# ------------------- Processing Section -------------------
if uploaded_file:
    # Check if this is a new file or if we need to process it
    file_changed = st.session_state.current_file_name != uploaded_file.name
    
    if file_changed or not st.session_state.file_processed:
        # Reset states when new file is uploaded
        if file_changed:
            st.session_state.content_generated = False
            st.session_state.summary = ""
            st.session_state.notes = ""
            st.session_state.flashcards = ""
            st.session_state.transcript = ""
            st.session_state.file_processed = False
            st.session_state.current_file_name = uploaded_file.name
        
        # Create upload directory
        os.makedirs("audio_uploads", exist_ok=True)
        file_path = os.path.join("audio_uploads", uploaded_file.name)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        
        # Progress bar for transcription
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Transcribe or read content
        status_text.text("🔄 Processing your file...")
        progress_bar.progress(25)
        
        try:
            if uploaded_file.name.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    transcript = f.read()
                status_text.text("📖 Text file loaded successfully!")
            else:
                status_text.text("🎤 Transcribing audio... This may take a moment.")
                transcript = transcribe_audio(file_path)
                status_text.text("🎤 Audio transcribed successfully!")
            
            # Store transcript in session state
            st.session_state.transcript = transcript
            st.session_state.file_processed = True
            
            progress_bar.progress(50)
            
            # Clean up the file
            os.remove(file_path)
            
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()
            
            st.success("✅ Content processed successfully!")
            
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.stop()
    
    # Use transcript from session state
    transcript = st.session_state.transcript
    
    # Show transcript stats
    word_count = count_words(transcript)
    char_count = len(transcript)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Words", f"{word_count:,}")
    with col2:
        st.metric("🔤 Characters", f"{char_count:,}")
    with col3:
        estimated_time = max(1, word_count // 200)  # Assuming 200 words per minute reading
        st.metric("⏱️ Est. Reading Time", f"{estimated_time} min")
    
    # ------------------- Transcript Viewer -------------------
    with st.expander("📜 View Transcript", expanded=False):
        st.text_area(
            "Transcript Content",
            st.session_state.transcript,
            height=300,
            help="Review the transcribed content before generating notes"
        )
    
    # ------------------- Generation Section -------------------
    st.markdown("---")
    st.markdown("### 🚀 Generate AI Content")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        generate_btn = st.button(
            "🧠 Generate Summary, Notes & Flashcards",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        if st.button("🔄 Clear Results", use_container_width=True):
            st.session_state.content_generated = False
            st.session_state.summary = ""
            st.session_state.notes = ""
            st.session_state.flashcards = ""
            st.session_state.transcript = ""
            st.session_state.file_processed = False
            st.session_state.current_file_name = ""
            st.experimental_rerun()
    
    if generate_btn:
        try:
            # Progress tracking
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Generate summary
                status_text.text("📄 Generating summary...")
                progress_bar.progress(20)
                summary = generate_summary(st.session_state.transcript)
                st.session_state.summary = summary
                
                # Generate notes
                status_text.text("📝 Creating organized notes...")
                progress_bar.progress(60)
                notes = generate_notes(st.session_state.transcript)
                st.session_state.notes = notes
                
                # Generate flashcards
                status_text.text("🎴 Building flashcards...")
                progress_bar.progress(90)
                flashcards = generate_flashcards(st.session_state.transcript)
                st.session_state.flashcards = flashcards
                
                progress_bar.progress(100)
                status_text.text("✅ All content generated!")
                
                # Set content generated flag
                st.session_state.content_generated = True
                
                # Clean up progress indicators
                progress_bar.empty()
                status_text.empty()
            
            st.success("🎉 All content generated successfully! You can now review and use your AI-generated notes.")
            
        except Exception as e:
            st.error(f"❌ Error generating content: {str(e)}")
            st.info("💡 Try uploading a different file or check your API configuration.")
    
    # ------------------- Results Display -------------------
    if st.session_state.content_generated:
        st.markdown("---")
        st.markdown("## 📋 Generated Content")
        
        # Summary
        summary_html = create_content_card(
            "Summary", 
            st.session_state.summary.replace('\n', '<br>'), 
            "📄", 
            count_words(st.session_state.summary) if show_word_count else None
        )
        st.markdown(summary_html, unsafe_allow_html=True)
        
        # Notes
        notes_html = create_content_card(
            "Topic-wise Notes", 
            st.session_state.notes.replace('\n', '<br>'), 
            "📝", 
            count_words(st.session_state.notes) if show_word_count else None
        )
        st.markdown(notes_html, unsafe_allow_html=True)
        
        # Flashcards
        flashcards_html = create_content_card(
            "Study Flashcards", 
            st.session_state.flashcards.replace('\n', '<br>'), 
            "🎴", 
            count_words(st.session_state.flashcards) if show_word_count else None
        )
        st.markdown(flashcards_html, unsafe_allow_html=True)
        
        # Auto-scroll to results
        if enable_auto_scroll:
            st.markdown("""
            <script>
            window.scrollTo(0, document.body.scrollHeight);
            </script>
            """, unsafe_allow_html=True)
        
        # ------------------- Download Section (Only shown after content is generated) -------------------
        st.markdown("---")
        st.markdown("### 📥 Download Your Notes")
        
        # Generate files
        pdf_path = generate_pdf("Smart Notes", st.session_state.summary, st.session_state.notes, st.session_state.flashcards)
        docx_path = generate_docx("Smart Notes", st.session_state.summary, st.session_state.notes, st.session_state.flashcards)
        
        col1, col2 = st.columns(2)
        
        with col1:
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download as PDF",
                    data=f,
                    file_name="smart_notes.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        
        with col2:
            with open(docx_path, "rb") as f:
                st.download_button(
                    label="📝 Download as Word (.docx)",
                    data=f,
                    file_name="smart_notes.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

else:
    # ------------------- Welcome Section -------------------
    st.markdown("""
    <div class="content-card">
        <h3>🚀 Get Started</h3>
        <div class="content">
            <p><strong>Upload your lecture content to begin:</strong></p>
            <ul>
                <li>🎵 <strong>Audio files:</strong> MP3, WAV, M4A, OGG</li>
                <li>📄 <strong>Text files:</strong> TXT format</li>
            </ul>
            <p>The AI will automatically:</p>
            <ul>
                <li>📄 Create a concise summary</li>
                <li>📝 Organize content into topic-wise notes</li>
                <li>🎴 Generate study flashcards</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------- Footer -------------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: {}; font-size: 0.9rem; margin-top: 2rem;'>
        <p>Built with 💙 using <strong>Streamlit</strong> • Powered by <strong>OpenAI</strong> & <strong>Whisper</strong></p>
        <p style='font-size: 0.8rem; opacity: 0.7;'>© 2025 Smart Notes Generator • Made by Gautham</p>
    </div>
    """.format(theme_config['text_secondary']),
    unsafe_allow_html=True
)
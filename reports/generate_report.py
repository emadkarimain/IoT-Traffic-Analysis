import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

# ================= CONFIGURATION =================
CSV_FILE = "mqtt_captured_data.csv"
OUTPUT_PDF = "Professional_Report.pdf"

# ================= TEXT CONTENT =================
TEXT_SECTIONS = {
    "header": "TECHNICAL REPORT: Large-Scale Public IoT Traffic Analysis",
    "author": "Author: Emad Karimian Shamsabadi | Date: December 2025",
    "sec1_title": "1. Executive Summary",
    "sec1_body": """This report details a large-scale analysis of the public IoT ecosystem. Leveraging a custom multi-threaded Python ingestion engine, we monitored global traffic across Europe and Asia.
Key Achievement: Successfully captured and analyzed 286,253 real-time messages in a 30-minute window. The study uncovers a distinct preference for speed over reliability (100% QoS 0 usage) and identifies significant infrastructure variances between major brokers like HiveMQ and Mosquitto.""",
    
    "sec2_title": "2. Data Acquisition Architecture",
    "sec2_body": """To ensure data integrity, we developed a Python logger using 'paho-mqtt'. The system handled concurrent connections to 6 global brokers (HiveMQ, EMQX, Mosquitto, etc.) simultaneously.
Strategy: We utilized the 'root/#' wildcard to capture the entire topic tree.
Concurrency: Implemented threading to prevent blocking during high-throughput bursts.""",
    
    "sec3_title": "3. Infrastructure Performance Analysis",
    "sec3_body": """Benchmarking revealed massive disparities. HiveMQ emerged as the top performer (~104k messages).
Critical Finding: Mosquitto showed significantly lower traffic (~26k) due to strict ACLs blocking anonymous wildcard subscribers. EmqxCN proved to be a high-traffic source.""",
    
    "sec4_title": "4. Payload & Protocol Insights",
    "sec4_body": """Format Standardization: JSON dominates (67% of traffic), confirming it as the standard for interoperability. HiveMQ shows high 'Numeric' traffic due to educational usage.
Reliability vs. Speed: 100% of traffic used QoS 0. Only 5.8% of messages were 'Retained', proving public IoT data is ephemeral.""",
    
    "sec5_title": "5. Temporal Traffic Behavior",
    "sec5_body": """A 24-hour analysis revealed a massive synchronization spike at 23:00 (~95k messages), driven by a fleet of trackers performing batch updates (device/status).""",
    
    "sec6_title": "6. Conclusion",
    "sec6_body": """The project bridged theoretical networking with real-world engineering. Results prove the public IoT ecosystem is a high-velocity, JSON-dominated environment prioritizing speed ('Fire and Forget') over security."""
}

# ================= IMAGE GENERATION FUNCTIONS =================

def generate_charts(df):
    # Set style suitable for print
    sns.set_style("whitegrid")
    
    # 1. Code Snippet Simulation
    plt.figure(figsize=(10, 4))
    plt.text(0.01, 0.9, 
             "def start_logging():\n    clients = []\n    for broker in BROKERS:\n        client = mqtt.Client(userdata={'name': broker['name']})\n        client.connect(broker['address'], broker['port'])\n        client.subscribe('#')\n        client.loop_start()\n        clients.append(client)", 
             fontsize=11, family='monospace', verticalalignment='top')
    plt.axis('off')
    plt.title("Figure 1: Core Python Multi-threading Implementation", loc='left', fontsize=10, fontweight='bold')
    plt.savefig("fig1_code.png", bbox_inches='tight', dpi=150)
    plt.close()

    # 2. Broker Traffic (Slide 6)
    plt.figure(figsize=(10, 5))
    order = df['broker'].value_counts().index
    sns.countplot(y='broker', data=df, order=order, palette='viridis')
    plt.title("Figure 2: Messages Received per Broker (Traffic Volume)", fontsize=12, fontweight='bold')
    plt.xlabel("Message Count")
    plt.tight_layout()
    plt.savefig("fig2_broker.png", dpi=150)
    plt.close()

    # 3. Payload Type (Slide 7)
    plt.figure(figsize=(10, 5))
    sns.countplot(x='broker', hue='payload_type', data=df, palette='viridis')
    plt.title("Figure 3: Payload Type Distribution per Broker", fontsize=12, fontweight='bold')
    plt.ylabel("Message Count")
    plt.legend(title='Payload Type')
    plt.tight_layout()
    plt.savefig("fig3_payload.png", dpi=150)
    plt.close()

    # 4. QoS & Retention (Slide 8)
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    sns.countplot(x='qos', data=df, ax=axes[0], palette='magma')
    axes[0].set_title("Figure 4a: QoS Usage (100% QoS 0)")
    
    retain_counts = df['retain'].value_counts()
    axes[1].pie(retain_counts, labels=['Not Retained', 'Retained'], autopct='%1.1f%%', colors=['#c2c2f0', '#ffb3e6'])
    axes[1].set_title("Figure 4b: Retained Messages")
    plt.tight_layout()
    plt.savefig("fig4_qos.png", dpi=150)
    plt.close()

    # 5. Temporal Spike (Slide 11)
    try:
        # Try converting timestamp, handle errors if format is unexpected
        df['hour'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S', errors='coerce').dt.hour
        # Drop NaNs if any conversion failed
        df_time = df.dropna(subset=['hour'])
        
        if not df_time.empty:
            plt.figure(figsize=(10, 5))
            sns.histplot(data=df_time, x='hour', bins=24, color='purple', kde=False)
            plt.title("Figure 5: Hourly Traffic Distribution (Spike at 23:00)", fontsize=12, fontweight='bold')
            plt.xlabel("Hour of Day")
            plt.tight_layout()
            plt.savefig("fig5_time.png", dpi=150)
            plt.close()
        else:
            print("Warning: Could not extract hours from timestamp. Skipping Figure 5.")
    except Exception as e:
        print(f"Warning: Could not generate time chart. {e}")

# ================= PDF GENERATION =================
class ReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, TEXT_SECTIONS["header"], 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, TEXT_SECTIONS["author"], 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln()

    def add_image_safe(self, image_path):
        if os.path.exists(image_path):
            try:
                self.image(image_path, w=170)
                self.ln(10)
            except Exception as e:
                print(f"Error adding image {image_path}: {e}")
        else:
            print(f"Image not found: {image_path}")

def create_pdf():
    pdf = ReportPDF()
    pdf.add_page()
    
    # Sec 1
    pdf.chapter_title(TEXT_SECTIONS["sec1_title"])
    pdf.chapter_body(TEXT_SECTIONS["sec1_body"])
    
    # Sec 2
    pdf.chapter_title(TEXT_SECTIONS["sec2_title"])
    pdf.chapter_body(TEXT_SECTIONS["sec2_body"])
    pdf.add_image_safe("fig1_code.png")
    
    # Sec 3
    pdf.chapter_title(TEXT_SECTIONS["sec3_title"])
    pdf.chapter_body(TEXT_SECTIONS["sec3_body"])
    pdf.add_image_safe("fig2_broker.png")
    
    # Sec 4
    pdf.add_page()
    pdf.chapter_title(TEXT_SECTIONS["sec4_title"])
    pdf.chapter_body(TEXT_SECTIONS["sec4_body"])
    pdf.add_image_safe("fig3_payload.png")
    pdf.add_image_safe("fig4_qos.png")
    
    # Sec 5
    pdf.chapter_title(TEXT_SECTIONS["sec5_title"])
    pdf.chapter_body(TEXT_SECTIONS["sec5_body"])
    pdf.add_image_safe("fig5_time.png")
        
    # Sec 6
    pdf.chapter_title(TEXT_SECTIONS["sec6_title"])
    pdf.chapter_body(TEXT_SECTIONS["sec6_body"])

    try:
        pdf.output(OUTPUT_PDF, 'F')
        print(f"\n✅ SUCCESS! Report generated: {OUTPUT_PDF}")
        print("Now you can upload this PDF to LinkedIn!")
    except Exception as e:
        print(f"\n❌ Error saving PDF: {e}")

# ================= MAIN EXECUTION =================
if __name__ == "__main__":
    if os.path.exists(CSV_FILE):
        print("Loading Data...")
        try:
            df = pd.read_csv(CSV_FILE)
            print("Generating Charts...")
            generate_charts(df)
            print("Building PDF...")
            create_pdf()
        except Exception as e:
            print(f"❌ Error processing data: {e}")
    else:
        print(f"❌ Error: Could not find '{CSV_FILE}'. Please make sure it is in the same folder.")

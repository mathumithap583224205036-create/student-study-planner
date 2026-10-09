"""
Modern styling and custom CSS for Student Study Planner Agent.
Provides an elegant, responsive, and visually appealing user experience.
"""

def get_custom_css() -> str:
    return """
    <style>
    /* Global Font and Container Styling */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 95rem;
    }

    /* Header Banner */
    .agent-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 100%);
        border-radius: 16px;
        padding: 24px 32px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(67, 56, 202, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    
    .agent-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .agent-subtitle {
        font-size: 0.95rem;
        color: #c7d2fe;
        margin-top: 6px;
        margin-bottom: 0;
        font-weight: 500;
    }

    .status-badge {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.3);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .badge-dot {
        width: 8px;
        height: 8px;
        background-color: #34d399;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #34d399;
    }

    /* Metric Card Styling */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02), 0 1px 2px rgba(0,0,0,0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px -4px rgba(0,0,0,0.06);
    }

    .metric-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
    }

    .metric-subtext {
        font-size: 0.8rem;
        color: #6366f1;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Priority Badges */
    .pill-high {
        background-color: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin: 2px 4px 2px 0;
    }

    .pill-med {
        background-color: #fffbeb;
        color: #d97706;
        border: 1px solid #fde68a;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin: 2px 4px 2px 0;
    }

    .pill-low {
        background-color: #f0fdf4;
        color: #16a34a;
        border: 1px solid #bbf7d0;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin: 2px 4px 2px 0;
    }

    /* Today's Schedule Card */
    .today-card {
        background: #ffffff;
        border: 1px solid #e0e7ff;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.05);
    }

    .session-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 14px;
        margin-bottom: 8px;
        border-radius: 10px;
        background: #f8fafc;
        border-left: 4px solid #6366f1;
    }

    .session-item.break {
        border-left-color: #10b981;
        background: #f0fdf4;
    }

    .session-item.revision {
        border-left-color: #f59e0b;
        background: #fffbeb;
    }

    /* Trace / Audit Container */
    .agent-trace-box {
        background: #0f172a;
        color: #e2e8f0;
        border-radius: 10px;
        padding: 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        line-height: 1.5;
        border-left: 4px solid #6366f1;
        margin-top: 10px;
    }

    /* Custom Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        padding: 6px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
        padding: 8px 16px;
        color: #475569;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #4f46e5 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """

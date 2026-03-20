from __future__ import annotations

custom_css = """
:root {
    --bg-1: #030712;
    --bg-2: #071224;
    --bg-3: #0b1730;
    --bg-4: #0f1d3b;
    --panel: rgba(7, 18, 36, 0.92);
    --panel-soft: rgba(10, 20, 40, 0.95);
    --border: rgba(148, 163, 184, 0.16);
    --text: #f8fafc;
    --muted: #cbd5e1;
    --accent: #38bdf8;
    --green: #22c55e;
    --violet: #8b5cf6;
    --gold: #f59e0b;
    --danger: #ef4444;
}

.gradio-container {
    background:
        radial-gradient(circle at top left, rgba(56, 189, 248, 0.08), transparent 22%),
        radial-gradient(circle at top right, rgba(139, 92, 246, 0.08), transparent 18%),
        linear-gradient(135deg, var(--bg-1) 0%, var(--bg-2) 42%, #0b1020 100%) !important;
    color: var(--text) !important;
    min-height: 100vh;
}

#dashboard-root,
#dashboard-root * {
    box-sizing: border-box;
}

#dashboard-root .gr-block,
#dashboard-root .block,
#dashboard-root .gr-panel {
    border-radius: 22px !important;
    border: 1px solid var(--border) !important;
    background: var(--panel) !important;
    box-shadow: 0 18px 44px rgba(0, 0, 0, 0.28) !important;
}

#dashboard-root .gr-row,
#dashboard-root .gr-column,
#dashboard-root .gr-group,
#dashboard-root .gr-box {
    overflow: visible !important;
}

#dashboard-root h1,
#dashboard-root h2,
#dashboard-root h3,
#dashboard-root h4,
#dashboard-root p,
#dashboard-root label,
#dashboard-root span,
#dashboard-root div {
    color: var(--text);
}

.main-title {
    padding: 10px 6px 18px 6px;
}

.main-title h1 {
    margin: 0 0 8px 0;
    font-size: 38px;
    font-weight: 900;
    letter-spacing: -0.02em;
}

.main-title p {
    margin: 0;
    color: var(--muted);
    font-size: 15px;
    line-height: 1.5;
}

.section-title {
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 6px;
}

.subtle-text {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 12px;
}

.legend-box,
.info-box {
    padding: 14px 16px;
    border-radius: 16px;
    border: 1px solid var(--border);
    background: rgba(255, 255, 255, 0.04);
    color: #e2e8f0;
    line-height: 1.5;
}

.kpi-card {
    display: flex;
    align-items: center;
    gap: 14px;
    min-height: 96px;
    padding: 18px;
    border-radius: 20px;
    border: 1px solid var(--border);
    background: linear-gradient(145deg, rgba(10,18,35,0.98), rgba(16,29,58,0.94));
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.26);
}

.kpi-card.blue { border-color: rgba(56, 189, 248, 0.20); }
.kpi-card.green { border-color: rgba(34, 197, 94, 0.20); }
.kpi-card.violet { border-color: rgba(139, 92, 246, 0.20); }
.kpi-card.gold { border-color: rgba(245, 158, 11, 0.20); }

.kpi-icon {
    min-width: 52px;
    height: 52px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.07);
    font-size: 24px;
}

.kpi-body {
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.kpi-title {
    color: var(--muted);
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 6px;
}

.kpi-value {
    color: var(--text);
    font-size: 18px;
    font-weight: 900;
    line-height: 1.25;
    word-break: break-word;
}

#dashboard-root input,
#dashboard-root textarea {
    background: rgba(15, 23, 42, 0.94) !important;
    color: #ffffff !important;
    border: 1px solid rgba(148, 163, 184, 0.22) !important;
    border-radius: 15px !important;
}

#dashboard-root input:focus,
#dashboard-root textarea:focus {
    border-color: rgba(56, 189, 248, 0.65) !important;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.14) !important;
}

#dashboard-root button {
    border-radius: 14px !important;
    font-weight: 800 !important;
    transition: transform 0.16s ease, box-shadow 0.16s ease !important;
}

#dashboard-root button:hover {
    transform: translateY(-1px);
}

#dashboard-root .primary-btn button {
    background: linear-gradient(135deg, #0284c7, #2563eb) !important;
    border: none !important;
    color: white !important;
}

#dashboard-root .secondary-btn button {
    background: rgba(255, 255, 255, 0.06) !important;
    color: white !important;
    border: 1px solid rgba(148, 163, 184, 0.18) !important;
}

#dashboard-root .danger-btn button {
    background: linear-gradient(135deg, #dc2626, #ef4444) !important;
    border: none !important;
    color: white !important;
}

#dashboard-root [role="listbox"],
#dashboard-root .options,
#dashboard-root .wrap,
#dashboard-root .dropdown,
#dashboard-root .menu {
    z-index: 9999 !important;
}

#dashboard-root .gr-dataframe {
    border-radius: 18px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
    background: rgba(7, 18, 36, 0.96) !important;
}

#dashboard-root table {
    border-radius: 18px !important;
    overflow: hidden !important;
}

#dashboard-root thead tr th {
    background: rgba(15, 29, 59, 0.98) !important;
    color: #f8fafc !important;
    font-weight: 800 !important;
    border-bottom: 1px solid rgba(148,163,184,0.14) !important;
}

#dashboard-root tbody tr {
    background: rgba(7, 18, 36, 0.90) !important;
}

#dashboard-root tbody tr:nth-child(even) {
    background: rgba(10, 20, 40, 0.98) !important;
}

#dashboard-root tbody td {
    color: #e2e8f0 !important;
    border-bottom: 1px solid rgba(148,163,184,0.08) !important;
}

.report-box textarea {
    font-family: Consolas, "Courier New", monospace !important;
    line-height: 1.5 !important;
}

footer {
    display: none !important;
}
"""
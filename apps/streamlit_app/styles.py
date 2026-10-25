"""Global CSS for the app (visual identity: teal -> red gradient)."""

GLOBAL_CSS = """
    <style>
    .main-title {text-align: center;}
    .subtitle {text-align: center; color: #94A3B8; font-size: 18px; margin: 10px 0 30px 0;}
    /* Subtle frame + vignette on every detection image (Sample Images,
       Upload, Search by Region) so satellite tiles read as part of the
       same designed piece instead of looking like raw, unstyled crops. */
    [data-testid="stImage"] img {
        border-radius: 10px;
        border: 1px solid rgba(20,184,166,0.28);
        box-shadow:
            inset 0 0 34px rgba(0,0,0,0.30),
            0 4px 18px rgba(0,0,0,0.35);
    }
    /* Same rounded, teal-bordered "netron box" outline applied to native
       Streamlit inputs that otherwise blend flat into the dark background:
       dropdowns (Metric / Experiment pickers), number inputs (Min/Max
       Longitude/Latitude), and the file-uploader's drop zone. */
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stNumberInput"] > div,
    [data-testid="stFileUploaderDropzone"] {
        border: 1px solid rgba(20,184,166,0.35) !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25);
    }
    /* Same teal outline extended to every st.dataframe table in the app
       (Top 10 cities, Coordinate data, Field Detections, Experiment
       Metrics, etc.) and every st.expander panel — Streamlit's own default
       border on these is barely visible against the dark background, which
       read as an unstyled white/near-transparent edge next to everything
       else above that already gets this treatment. overflow:hidden clips
       the inner grid's own square corners to the rounded border instead of
       poking past it. */
    [data-testid="stDataFrame"],
    [data-testid="stExpander"] {
        border: 1px solid rgba(20,184,166,0.35) !important;
        border-radius: 10px !important;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25);
    }
    /* Same teal outline on every button and download button (Downloads tab's
       "quadradinhos" — Annotated Dataset, Experiment Metrics, Detection
       Summary, Field Triage Log, etc., plus Play/Pause Music and the
       Search-by-Region buttons) — same reasoning as the tables/expanders
       above: these had no border at all against the dark background, which
       stood out as unstyled next to everything else. `> button` targets the
       actual clickable element inside Streamlit's wrapper div, which is
       where the visible edges are. */
    [data-testid="stDownloadButton"] > button,
    [data-testid="stButton"] > button {
        border: 1px solid rgba(20,184,166,0.35) !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25);
    }
    .result-card {background-color: #f8fafc; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0;}
    .metric-card {
        background-color: #f8fafc;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.08);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(15, 23, 42, 0.16);
    }
    .flow-step {
        border-radius: 16px;
        padding: 22px 20px 20px 20px;
        text-align: left;
        position: relative;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.12);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        margin-bottom: 18px;
    }
    .flow-step:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.28);
    }
    .flow-step .flow-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 999px;
        font-size: 12.5px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .flow-step .flow-icon {
        font-size: 26px;
        margin-bottom: 8px;
        display: block;
    }
    .flow-step .flow-title {
        font-weight: 700; font-size: 15px; margin: 0 0 6px 0; line-height: 1.3;
    }
    .flow-step .flow-desc {
        font-size: 12.5px; margin: 0; line-height: 1.5; flex-grow: 1;
    }
    .flow-arrow {
        text-align: center; color: #cbd5e1; font-size: 16px; padding-top: 40px;
    }
    .dark-card {
        background: linear-gradient(135deg, #0B1F1D 0%, #0E3B36 55%, #3A1A17 100%);
        padding: 28px 26px;
        border-radius: 14px;
        border: 1px solid rgba(20, 184, 166, 0.30);
        box-shadow: 0 6px 22px rgba(15, 23, 42, 0.35), inset 0 1px 0 rgba(255,255,255,0.06);
        text-align: center;
    }
    .dark-card .repo-icon {
        font-size: 44px;
        display: block;
        text-align: center;
        margin: 0 auto 10px auto;
        line-height: 1;
    }
    .dark-card h4 {
        text-align: center;
        margin: 0 0 8px 0;
        color: #FFFFFF;
    }
    .sample-btn > button {
        background: linear-gradient(135deg, #0E756D 0%, #924227 55%, #C20000 100%);
        color: white;
        font-weight: 600;
        border: none !important;
        padding: 0.75em 1.4em;
        border-radius: 10px;
        box-shadow: 0 4px 14px rgba(194, 0, 0, 0.30);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .sample-btn > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(194, 0, 0, 0.45);
    }
    /* ===== Visual identity: teal -> red gradient (same as README/SVGs) ===== */
    :root {
        --hd-grad: linear-gradient(90deg,#005C48 0%,#425943 30%,#6E513B 40%,#924227 50%,#B02813 60%,#C20000 70%,#D80000 80%,#DD0000 100%);
        --hd-teal: #14b8a6;
        --hd-red: #DD0000;
    }
    /* thin gradient line fixed at the very top of the page */
    [data-testid="stApp"]::before {
        content: ""; position: fixed; top: 0; left: 0; right: 0; height: 3px;
        background: var(--hd-grad); z-index: 999999; pointer-events: none;
    }
    /* gradient divider for st.markdown("---") */
    [data-testid="stMarkdownContainer"] hr {
        border: 0 !important; height: 2px !important;
        background: var(--hd-grad) !important; opacity: .55; border-radius: 2px;
    }
    /* active tab: gradient underline instead of default red */
    [data-baseweb="tab-highlight"],
    [data-testid="stTabs"] .react-aria-SelectionIndicator { background: var(--hd-grad) !important; height: 3px !important; }
    [data-baseweb="tab"][aria-selected="true"],
    [data-testid="stTab"][aria-selected="true"],
    [data-testid="stTab"][aria-selected="true"] p { color: #FFFFFF !important; }
    [data-baseweb="tab-border"] { background: rgba(20,184,166,0.18) !important; }
    /* buttons: teal border turns into the red end on hover */
    [data-testid="stDownloadButton"] > button:hover,
    [data-testid="stButton"] > button:hover,
    [data-testid="stLinkButton"] > a:hover {
        border-color: rgba(221,0,0,0.75) !important; color: #FFFFFF !important;
        box-shadow: 0 4px 16px rgba(194,0,0,0.28);
    }
    [data-testid="stLinkButton"] > a {
        border: 1px solid rgba(20,184,166,0.35) !important; border-radius: 10px !important;
    }
    [data-testid="stExpander"]:hover { border-color: rgba(221,0,0,0.45) !important; }
    /* cards, inputs and focus rings */
    .metric-card:hover, .flow-step:hover { border-color: rgba(221,0,0,0.35); }
    [data-testid="stSelectbox"] > div > div:focus-within,
    [data-testid="stNumberInput"] > div:focus-within { border-color: rgba(221,0,0,0.7) !important; }
    /* progress / slider accents */
    [data-testid="stProgress"] > div > div > div > div { background: var(--hd-grad) !important; }
    /* keyboard focus: visible and on-brand (accessibility) */
    button:focus-visible, a:focus-visible, [role="tab"]:focus-visible {
        outline: 2px solid var(--hd-teal) !important; outline-offset: 2px !important;
    }
    /* text selection */
    ::selection { background: rgba(221,0,0,0.45); color: #fff; }
    /* main title: same look as assets/title.svg (card, serif, per-letter reds, sheen, underline) */
    .hd-title-card {
        max-width: 760px; margin: 6px auto 4px auto; padding: 22px 16px 16px 16px; text-align: center;
        border-radius: 14px; background: radial-gradient(ellipse at 50% 40%, #0b1216 0%, #05080b 100%);
    }
    .main-title { font-family: Georgia, 'Times New Roman', serif !important; font-size: 64px !important;
        font-weight: 700 !important; letter-spacing: 1px; line-height: 1.1 !important; margin: 0 !important;
        padding: 0 !important; white-space: nowrap; color: #FFFFFF; }
    .main-title .hd-emoji { font-size: 0.84em; }
    .main-title .hd-white { color: #FFFFFF; }
    .main-title .hd-text { position: relative; display: inline-block; }
    .main-title .hd-text::after {
        content: attr(data-text); position: absolute; left: 0; top: 0; white-space: nowrap;
        color: transparent; -webkit-text-fill-color: transparent; pointer-events: none;
        background: linear-gradient(100deg, transparent 40%, rgba(255,255,255,.22) 50%, transparent 60%) no-repeat;
        background-size: 250% 100%; background-position: 160% 0;
        -webkit-background-clip: text; background-clip: text;
        animation: hd-sheen 7s ease-in-out infinite;
    }
    @keyframes hd-sheen { 0%, 12% { background-position: 160% 0; } 40%, 100% { background-position: -60% 0; } }
    .hd-title-line { width: min(420px, 70%); height: 2px; margin: 12px auto 0 auto; border-radius: 1px; background: var(--hd-grad); }
    @media (max-width: 640px) { .main-title { font-size: 34px !important; } }
    @media (prefers-reduced-motion: reduce) { .main-title .hd-text::after { animation: none; } }
    /* embedded HTML snippets (music button, brand footer, helper scripts): no border,
       no opaque canvas — the thin white lines / white boxes came from these frames */
    iframe.stIFrame, [data-testid="stIFrame"] { border: 0 !important; background: transparent !important; color-scheme: normal !important; }
    /* mandatory detection disclaimer (responsible-AI notice) */
    .hd-disclaimer {
        margin: 10px 0 4px 0; padding: 10px 14px; font-size: 13px; line-height: 1.5;
        color: #FDE2E2; background: rgba(221,0,0,0.08);
        border: 1px solid rgba(221,0,0,0.25); border-left: 4px solid #DD0000; border-radius: 8px;
    }
    /* Teal info callout — replaces Streamlit's default blue st.info band so
       every notice uses the identity palette (teal, not blue). */
    .hd-info {
        display: flex; gap: 12px; align-items: flex-start;
        margin: 6px 0 14px 0; padding: 14px 18px; font-size: 15px; line-height: 1.55;
        color: #CFFAF3; background: rgba(20,184,166,0.10);
        border: 1px solid rgba(20,184,166,0.40); border-left: 4px solid #14B8A6; border-radius: 10px;
    }
    .hd-info .hd-info-icon { font-size: 1.15em; line-height: 1.4; }
    .hd-info strong { color: #FFFFFF; }
    .hd-info code { color: #5EEAD4; background: rgba(0,0,0,0.25); padding: 1px 5px; border-radius: 4px; }

    /* Global-context table (About): stronger frame, visible row and column
       rules, header band, zebra rows, hover, São Paulo (study focus) row marked. */
    .hd-ctx-wrap {
        overflow-x: auto; border: 1.5px solid rgba(20,184,166,0.65); border-radius: 10px;
        box-shadow: 0 0 0 1px rgba(20,184,166,0.10), 0 4px 16px rgba(0,0,0,0.35);
    }
    .hd-ctx { width: 100%; border-collapse: collapse; }
    .hd-ctx th {
        text-align: left; padding: 11px 14px; color: #5EEAD4; font-size: 12px;
        text-transform: uppercase; letter-spacing: .05em;
        background: rgba(20,184,166,0.14); border-bottom: 3px solid #14B8A6;
        border-right: 1px solid rgba(94,234,212,0.28);
    }
    .hd-ctx td {
        padding: 10px 14px; color: #E8EEF5; font-size: 13.5px; vertical-align: top;
        border-bottom: 1px solid rgba(94,234,212,0.38);
        border-right: 1px solid rgba(94,234,212,0.20);
    }
    .hd-ctx th:last-child, .hd-ctx td:last-child { border-right: none; }
    .hd-ctx tbody tr:last-child td { border-bottom: none; }
    .hd-ctx tbody tr:nth-child(even) td { background: rgba(255,255,255,0.025); }
    .hd-ctx tbody tr:hover td { background: rgba(20,184,166,0.10); }
    .hd-ctx tbody tr:first-child td {
        background: rgba(20,184,166,0.12); border-bottom: 2px solid rgba(94,234,212,0.55);
    }
    .hd-ctx tbody tr:first-child td:first-child { box-shadow: inset 4px 0 0 #14B8A6; }
    .hd-ctx a { color: #5EEAD4; }

    /* Pre-project box (Downloads) */
    .hd-preproj {
        margin: 8px 0 10px 0; padding: 14px 18px; border-radius: 10px;
        border: 1px solid rgba(20,184,166,0.45); border-left: 4px solid #14B8A6;
        background: rgba(20,184,166,0.07);
    }
    .hd-preproj h4 { margin: 0 0 6px 0; color: #5EEAD4; font-size: 1.05rem; }
    .hd-preproj p { margin: 0; color: #CBD5E1; font-size: 13.5px; line-height: 1.6; }
    /* respect users who prefer reduced motion (page UI only) */
    @media (prefers-reduced-motion: reduce) {
        .metric-card, .flow-step, .sample-btn > button { transition: none !important; }
    }
    </style>
"""

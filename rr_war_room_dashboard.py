import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Rajasthan Royals | 2027 Auction War Room",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">

<style>
    :root { color-scheme: dark !important; }
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(145deg, #060B14 0%, #0A1324 45%, #0F1A30 100%) !important;
        color: #F8FAFC !important;
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    .stApp p, .stApp label, .stApp li,
    [data-testid="stMarkdownContainer"] p, [data-testid="stWidgetLabel"] p {
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded' !important;
    }
    }
    h1, h2, h3, h4, .rr-title, .section-title, .scout-name, .quota-title {
        font-family: 'Space Grotesk', -apple-system, sans-serif !important;
        letter-spacing: -0.02em;
    }
    .mono-font, .card-value, .rr-pill, .scout-metric-val, .quota-chip {
        font-family: 'JetBrains Mono', monospace !important;
        font-variant-numeric: tabular-nums;
    }
    .block-container {
        padding-top: 3.2rem !important;
        padding-bottom: 2.6rem !important;
        padding-left: 2.2rem !important;
        padding-right: 2.2rem !important;
        max-width: 1420px !important;
    }
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #070D18; }
    ::-webkit-scrollbar-thumb { background: #1C2D4A; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #2A436D; }

    .rr-header {
        background: linear-gradient(135deg, rgba(14, 25, 48, 0.96) 0%, rgba(20, 36, 68, 0.92) 60%, rgba(55, 14, 46, 0.78) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-left: 4px solid #E8127D !important;
        border-radius: 12px !important;
        padding: 22px 26px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
    }
    .rr-header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        flex-wrap: wrap;
        gap: 8px;
    }
    .rr-crest {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1.6px;
        color: #E8127D !important;
    }
    .rr-status-beacon {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 11px;
        border-radius: 20px;
        background: rgba(232, 18, 125, 0.14) !important;
        border: 1px solid rgba(232, 18, 125, 0.35) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 10.5px !important;
        font-weight: 600 !important;
        letter-spacing: 0.8px;
        color: #FF5EA6 !important;
    }
    .rr-status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #E8127D;
        box-shadow: 0 0 8px #E8127D;
        display: inline-block;
    }
    .rr-title {
        font-size: 27px !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        margin: 0 !important;
        line-height: 1.15 !important;
    }
    .rr-subtitle {
        font-size: 13.5px !important;
        color: #94A3B8 !important;
        margin-top: 6px;
        line-height: 1.45;
    }
    .rr-strip {
        display: flex;
        gap: 8px;
        margin-top: 14px;
        flex-wrap: wrap;
    }
    .rr-pill {
        font-size: 11px !important;
        background: rgba(14, 25, 48, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 4px 10px;
        border-radius: 6px;
        color: #CBD5E1 !important;
    }
    .rr-pill strong { color: #FFFFFF !important; }
    .rr-pill-accent {
        border-color: rgba(232, 18, 125, 0.45) !important;
        color: #FF4D9E !important;
        background: rgba(232, 18, 125, 0.12) !important;
    }
    .rr-pill-gold {
        border-color: rgba(212, 175, 55, 0.45) !important;
        color: #F1D278 !important;
        background: rgba(212, 175, 55, 0.12) !important;
    }
    .analyst-card {
        background: linear-gradient(180deg, rgba(17, 30, 56, 0.92) 0%, rgba(10, 19, 38, 0.98) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 16px 18px !important;
        height: 100%;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        transition: all 0.25s ease;
    }
    .analyst-card:hover {
        border-color: rgba(232, 18, 125, 0.4) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }
    .card-eyebrow {
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94A3B8 !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .card-value {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        margin: 8px 0 4px 0;
        letter-spacing: -0.02em;
    }
    .card-sub {
        font-size: 12px !important;
        color: #94A3B8 !important;
        line-height: 1.4;
    }
    .pill-tag-pink {
        background: linear-gradient(90deg, rgba(232, 18, 125, 0.22) 0%, rgba(232, 18, 125, 0.08) 100%) !important;
        border: 1px solid rgba(232, 18, 125, 0.4) !important;
        color: #FF5EA6 !important;
        padding: 2px 7px;
        border-radius: 4px;
        font-weight: 600 !important;
        font-size: 11px !important;
    }
    .pill-tag-gold {
        background: linear-gradient(90deg, rgba(212, 175, 55, 0.22) 0%, rgba(212, 175, 55, 0.08) 100%) !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        color: #E5C368 !important;
        padding: 2px 7px;
        border-radius: 4px;
        font-weight: 600 !important;
        font-size: 11px !important;
    }
    .pill-tag-blue {
        background: linear-gradient(90deg, rgba(37, 99, 235, 0.22) 0%, rgba(37, 99, 235, 0.08) 100%) !important;
        border: 1px solid rgba(37, 99, 235, 0.4) !important;
        color: #93C5FD !important;
        padding: 2px 7px;
        border-radius: 4px;
        font-weight: 600 !important;
        font-size: 11px !important;
    }
    .section-title {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        margin-top: 6px;
        margin-bottom: 10px;
    }
    div[role="radiogroup"] {
        gap: 10px !important;
        margin-bottom: 12px !important;
    }
    div[role="radiogroup"] label {
        background: rgba(17, 30, 56, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 6px !important;
        padding: 5px 12px !important;
    }
    div[role="radiogroup"] label p {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 12.5px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(10, 19, 38, 0.9) !important;
        padding: 5px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 38px;
        border-radius: 7px;
        padding: 0 18px;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        border: none !important;
        transition: all 0.15s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #F8FAFC !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #E8127D 0%, #B80F63 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(232, 18, 125, 0.35) !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab-border"], .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 10px !important;
        background: rgba(11, 20, 38, 0.95) !important;
        overflow: hidden;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070D18 0%, #0A1426 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] label p {
        color: #F8FAFC !important;
    }
    .scout-card {
        background: linear-gradient(180deg, rgba(17, 30, 56, 0.88) 0%, rgba(10, 19, 38, 0.96) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
        margin-top: 8px;
        margin-bottom: 6px;
    }
    .scout-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .scout-name {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
    }
    .scout-meta {
        font-size: 11.5px !important;
        color: #94A3B8 !important;
    }
    .scout-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin-top: 8px;
    }
    .scout-metric {
        background: rgba(6, 12, 24, 0.78) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 6px;
        padding: 6px 10px;
    }
    .scout-metric-label {
        font-size: 9.5px !important;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #94A3B8 !important;
    }
    .scout-metric-val {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
    }
    .quota-box {
        background: linear-gradient(180deg, rgba(16, 28, 52, 0.9) 0%, rgba(10, 19, 38, 0.98) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
    }
    .quota-title {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .quota-chips {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .quota-chip {
        font-size: 11px !important;
        padding: 4px 10px;
        border-radius: 6px;
        background: rgba(14, 25, 48, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #CBD5E1 !important;
    }
    .quota-chip-locked {
        border-color: rgba(232, 18, 125, 0.45) !important;
        color: #FF5EA6 !important;
        background: rgba(232, 18, 125, 0.12) !important;
    }
    .quota-chip-target {
        border-color: rgba(212, 175, 55, 0.45) !important;
        color: #F1D278 !important;
        background: rgba(212, 175, 55, 0.12) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. ONE-TIME INGESTION & VECTORIZED PRE-COMPUTATION
# ---------------------------------------------------------
@st.cache_resource(show_spinner="Initializing scouting engine...")
def load_base_engine():
    cache_bbb = ".cache_bbb_m.parquet"
    cache_meta = ".cache_player_meta.parquet"

    if os.path.exists(cache_bbb) and os.path.exists(cache_meta):
        return pd.read_parquet(cache_bbb), pd.read_parquet(cache_meta)

    comps = pd.read_csv('competitions.csv', usecols=['comp_id', 'comp_name', 'match_format', 'season'])
    teams = pd.read_csv('teams.csv', usecols=['comp_id', 'team_id', 'team_name'])
    matches = pd.read_csv('matches.csv', usecols=[
        'match_id', 'comp_id', 'stage', 'knock_out',
        'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target'
    ])
    p11 = pd.read_csv('playing_eleven.csv', usecols=['match_id', 'team_id', 'player_id', 'batting_order', 'is_wk'])
    mapping = pd.read_csv('competition_team_player_mapping.csv', usecols=['comp_id', 'player_id', 'player_name', 'team_name'])

    bbb_cols = [
        'match_id', 'innings', 'overid', 'over_ball_num', 'innings_ball_num',
        'batting_team_id', 'bowling_team_id',
        'striker_id', 'striker_name', 'bowler_id', 'bowler_name',
        'runs', 'extras1_runs', 'extras_2_runs', 'extras_type',
        'is_four', 'is_six', 'is_wicket', 'dismissal_type',
        'batting_type', 'bowling_type'
    ]
    bbb = pd.read_csv('ball_by_ball.csv', usecols=bbb_cols)

    bbb_m = bbb.merge(matches, on='match_id', how='left').merge(comps, on='comp_id', how='left')
    bbb_m = bbb_m.sort_values(['match_id', 'innings', 'overid', 'over_ball_num', 'innings_ball_num']).reset_index(drop=True)

    bbb_m['total_runs'] = (bbb_m['runs'] + bbb_m['extras1_runs'] + bbb_m['extras_2_runs']).astype('int16')
    bbb_m['is_legal_ball'] = ~bbb_m['extras_type'].isin(['wide', 'Overstep'])
    bbb_m['is_batter_ball'] = bbb_m['extras_type'] != 'wide'
    bbb_m['is_boundary'] = bbb_m['is_four'] | bbb_m['is_six']
    bbb_m['is_bowler_wicket'] = bbb_m['is_wicket'] & (
        ~bbb_m['dismissal_type'].isin(['RunOut', 'Retire Out', 'Obstracting the field', 'Obstructing the field'])
    )

    bbb_m['phase'] = np.where(
        bbb_m['overid'] <= 6, 'Powerplay (1-6)',
        np.where(bbb_m['overid'] <= 15, 'Middle (7-15)', 'Death (16-20)')
    )

    bbb_m['cum_runs_before'] = bbb_m.groupby(['match_id', 'innings'])['total_runs'].cumsum() - bbb_m['total_runs']
    bbb_m['cum_wkts_before'] = bbb_m.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - bbb_m['is_wicket'].astype(int)
    bbb_m['legal_balls_before'] = bbb_m.groupby(['match_id', 'innings'])['is_legal_ball'].cumsum() - bbb_m['is_legal_ball'].astype(int)

    inn1_totals = bbb_m[bbb_m['innings'] == 1].groupby('match_id')['total_runs'].sum().rename('inn1_total')
    bbb_m = bbb_m.merge(inn1_totals, on='match_id', how='left')

    bbb_m['target'] = np.where(
        bbb_m['innings'] == 2,
        np.where(bbb_m['revised_target'].notna() & (bbb_m['revised_target'] > 0), bbb_m['revised_target'], bbb_m['inn1_total'] + 1),
        np.nan
    )
    bbb_m['max_overs'] = np.where(
        bbb_m['innings'] == 1,
        np.where(bbb_m['first_inn_revised_overs'].notna() & (bbb_m['first_inn_revised_overs'] > 0), bbb_m['first_inn_revised_overs'], 20.0),
        np.where(bbb_m['second_inn_revised_overs'].notna() & (bbb_m['second_inn_revised_overs'] > 0), bbb_m['second_inn_revised_overs'], 20.0)
    )
    bbb_m['balls_rem'] = ((bbb_m['max_overs'] * 6).astype(int) - bbb_m['legal_balls_before']).clip(lower=1)
    bbb_m['runs_needed'] = (bbb_m['target'] - bbb_m['cum_runs_before']).clip(lower=0)
    bbb_m['rrr'] = np.where(bbb_m['innings'] == 2, (bbb_m['runs_needed'] / bbb_m['balls_rem']) * 6, np.nan)

    pp_scores = bbb_m[bbb_m['overid'] <= 6].groupby(['match_id', 'innings'])['total_runs'].sum().rename('pp_runs')
    bbb_m = bbb_m.merge(pp_scores, on=['match_id', 'innings'], how='left')

    is_high_stakes = (bbb_m['knock_out'] == 1) | (bbb_m['stage'].isin(['Final', 'Qualifier', 'Eliminator', 'Semi Final', 'Super 4']))
    is_death = bbb_m['overid'] >= 16
    is_collapse = (
        ((bbb_m['overid'] <= 6) & (bbb_m['cum_wkts_before'] >= 2)) |
        ((bbb_m['overid'] <= 10) & (bbb_m['cum_wkts_before'] >= 3)) |
        (bbb_m['cum_wkts_before'] >= 5)
    )
    is_chase_pressure = (bbb_m['innings'] == 2) & (
        (bbb_m['rrr'] >= 10.5) | ((bbb_m['overid'] >= 15) & (bbb_m['rrr'] >= 8.5) & (bbb_m['rrr'] <= 18.0))
    )
    is_bowling_siege = (bbb_m['overid'] > 6) & (bbb_m['pp_runs'] >= 60)

    bbb_m['is_collapse'] = is_collapse
    bbb_m['dpi'] = (
        is_high_stakes.astype(int) * 20 +
        is_death.astype(int) * 30 +
        is_collapse.astype(int) * 25 +
        is_chase_pressure.astype(int) * 30 +
        is_bowling_siege.astype(int) * 15
    ).clip(upper=100).astype('int16')

    bbb_m['season_year'] = bbb_m['season'].astype(str).str[:4].astype('int16')
    recency_wt = np.where(bbb_m['season_year'] >= 2025, 1.25, np.where(bbb_m['season_year'] == 2024, 1.10, 0.85)).astype('float32')

    # Pre-compute vectorized weighted columns & boolean flags (eliminates slow .apply(lambda) later)
    bbb_m['is_dot_bat'] = (bbb_m['total_runs'] == 0) & bbb_m['is_batter_ball']
    bbb_m['bowler_runs'] = np.where(bbb_m['extras_type'].isin(['byes', 'legbyes', 'Penalty']), 0, bbb_m['total_runs']).astype('int16')
    bbb_m['is_dot_bowl'] = (bbb_m['bowler_runs'] == 0) & bbb_m['is_legal_ball']
    bbb_m['is_dot_any'] = (bbb_m['total_runs'] == 0) & bbb_m['is_legal_ball']

    bbb_m['rec_bat_runs'] = (bbb_m['runs'] * recency_wt).astype('float32')
    bbb_m['rec_bat_balls'] = (bbb_m['is_batter_ball'] * recency_wt).astype('float32')
    bbb_m['rec_bowl_runs'] = (bbb_m['bowler_runs'] * recency_wt).astype('float32')
    bbb_m['rec_bowl_balls'] = (bbb_m['is_legal_ball'] * recency_wt).astype('float32')
    bbb_m['rec_bowl_wkts'] = (bbb_m['is_bowler_wicket'] * recency_wt).astype('float32')

    # Drop intermediate columns not needed in UI to minimize RAM footprint
    keep_cols = [
        'match_id', 'comp_id', 'innings', 'overid', 'phase', 'season_year',
        'batting_team_id', 'bowling_team_id', 'striker_id', 'striker_name',
        'bowler_id', 'bowler_name', 'runs', 'total_runs', 'bowler_runs',
        'is_legal_ball', 'is_batter_ball', 'is_boundary', 'is_four', 'is_six',
        'is_wicket', 'is_bowler_wicket', 'is_dot_bat', 'is_dot_bowl', 'is_dot_any',
        'is_collapse', 'rrr', 'dpi',
        'rec_bat_runs', 'rec_bat_balls', 'rec_bowl_runs', 'rec_bowl_balls', 'rec_bowl_wkts'
    ]
    bbb_m = bbb_m[keep_cols]

    # Player Metadata
    latest_comp = mapping.merge(comps[['comp_id', 'season']], on='comp_id').sort_values(['season', 'comp_id'], ascending=False)
    latest_team = latest_comp.drop_duplicates('player_id')[['player_id', 'team_name']].rename(columns={'team_name': 'latest_team'})
    ipl26_roster = mapping[mapping['comp_id'] == 3298][['player_id', 'team_name']].rename(columns={'team_name': 'ipl_2026_team'})
    p11_teams = p11.merge(matches[['match_id', 'comp_id']], on='match_id').merge(teams, on=['comp_id', 'team_id'], how='left')
    ipl26_p11 = p11_teams[p11_teams['comp_id'] == 3298][['player_id', 'team_name']].drop_duplicates('player_id').rename(columns={'team_name': 'ipl_2026_team_p11'})

    player_meta = mapping[['player_id', 'player_name']].drop_duplicates('player_id')
    player_meta = player_meta.merge(ipl26_roster, on='player_id', how='left').merge(ipl26_p11, on='player_id', how='left').merge(latest_team, on='player_id', how='left')
    player_meta['ipl_2026_team'] = player_meta['ipl_2026_team'].fillna(player_meta['ipl_2026_team_p11']).fillna('Free Agent / Non-IPL')
    player_meta.drop(columns=['ipl_2026_team_p11'], inplace=True)

    role_info = p11.groupby('player_id').agg(
        matches_p11=('match_id', 'nunique'),
        avg_bat_order=('batting_order', 'mean')
    ).reset_index()

    bowl_style = bbb.groupby('bowler_id')['bowling_type'].agg(
        lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'None'
    ).reset_index().rename(columns={'bowler_id': 'player_id'})

    player_teams = mapping.groupby('player_id')['team_name'].apply(list).reset_index().rename(columns={'team_name': 'all_teams'})
    ipl_team_names = set(teams[teams['comp_id'].isin([1358, 1715, 2193, 2725, 3298])]['team_name'].unique())

    def classify_origin(t_list):
        non_ipl = [t for t in t_list if t not in ipl_team_names]
        if 'Pakistan' in non_ipl:
            return 'Pakistan (Ineligible)'
        if 'India' in non_ipl or (len(non_ipl) == 0 and any(t in ipl_team_names for t in t_list)):
            return 'India'
        return 'Overseas (IPL-Eligible)'

    player_teams['category'] = player_teams['all_teams'].apply(classify_origin)
    player_meta = player_meta.merge(role_info, on='player_id', how='left').merge(bowl_style, on='player_id', how='left').merge(player_teams[['player_id', 'category']], on='player_id', how='left')

    bbb_m.to_parquet(cache_bbb, index=False)
    player_meta.to_parquet(cache_meta, index=False)
    return bbb_m, player_meta

@st.cache_data
def get_ipl26_audit(_bbb_m):
    ipl26 = _bbb_m[_bbb_m['comp_id'] == 3298]

    rr_bat26 = ipl26[ipl26['batting_team_id'] == 3].groupby('striker_name', as_index=False).agg(
        Inn=('match_id', 'nunique'),
        Runs=('runs', 'sum'),
        Balls=('is_batter_ball', 'sum'),
        _4s=('is_four', 'sum'),
        _6s=('is_six', 'sum')
    ).rename(columns={'striker_name': 'Batter', '_4s': '4s', '_6s': '6s'})
    rr_bat26['SR'] = (rr_bat26['Runs'] / rr_bat26['Balls'] * 100).round(1)
    rr_bat26 = rr_bat26.sort_values('Runs', ascending=False)

    rr_bowl26 = ipl26[ipl26['bowling_team_id'] == 3].groupby('bowler_name', as_index=False).agg(
        Mat=('match_id', 'nunique'),
        Balls=('is_legal_ball', 'sum'),
        Runs=('total_runs', 'sum'),
        Wkts=('is_bowler_wicket', 'sum')
    ).rename(columns={'bowler_name': 'Bowler'})
    rr_bowl26['Econ'] = (rr_bowl26['Runs'] / (rr_bowl26['Balls'] / 6)).round(2)
    rr_bowl26 = rr_bowl26.sort_values('Wkts', ascending=False)

    bat_p = ipl26.assign(Team=np.where(ipl26['batting_team_id'] == 3, 'Rajasthan Royals', 'IPL 2026 League Avg')) \
                 .groupby(['Team', 'phase'], as_index=False).agg(runs=('total_runs', 'sum'), balls=('is_legal_ball', 'sum'))
    bat_p['Run Rate'] = (bat_p['runs'] / bat_p['balls'] * 6).round(2)

    bowl_p = ipl26.assign(Bowl_Team=np.where(ipl26['bowling_team_id'] == 3, 'Rajasthan Royals', 'IPL 2026 League Avg')) \
                  .groupby(['Bowl_Team', 'phase'], as_index=False).agg(balls=('is_legal_ball', 'sum'), dots=('is_dot_any', 'sum'))
    bowl_p['Dot %'] = (bowl_p['dots'] / bowl_p['balls'] * 100).round(1)

    return rr_bat26, rr_bowl26, bat_p, bowl_p

def minmax(s):
    if len(s) == 0 or s.max() == s.min():
        return pd.Series(0.5, index=s.index)
    return (s - s.min()) / (s.max() - s.min())

@st.cache_data
def compute_leaderboards(_bbb_m, _player_meta, dpi_threshold, min_balls, origin_tuple, season_tuple):
    mask_season = _bbb_m['season_year'].isin(season_tuple)
    df_s = _bbb_m[mask_season]
    is_hp = df_s['dpi'] >= dpi_threshold

    hp_count = int(is_hp.sum())
    tot_count = len(df_s)
    hp_pct = (hp_count / tot_count * 100) if tot_count > 0 else 0.0

    # Fast vectorized batting aggregations
    overall_bat = df_s.groupby('striker_id').agg(tot_balls=('is_batter_ball', 'sum'), tot_runs=('runs', 'sum'))
    overall_bat['overall_sr'] = overall_bat['tot_runs'] / overall_bat['tot_balls'].replace(0, np.nan) * 100

    hp_bat = df_s[is_hp].groupby('striker_id').agg(
        hp_balls=('is_batter_ball', 'sum'),
        hp_runs=('runs', 'sum'),
        hp_outs=('is_wicket', 'sum'),
        hp_bnds=('is_boundary', 'sum'),
        hp_dots=('is_dot_bat', 'sum'),
        rec_runs=('rec_bat_runs', 'sum'),
        rec_balls=('rec_bat_balls', 'sum')
    )
    hp_bat['hp_sr'] = hp_bat['hp_runs'] / hp_bat['hp_balls'].replace(0, np.nan) * 100
    hp_bat['hp_rec_sr'] = hp_bat['rec_runs'] / hp_bat['rec_balls'].replace(0, np.nan) * 100
    hp_bat['hp_bpd'] = hp_bat['hp_balls'] / hp_bat['hp_outs'].replace(0, np.nan)
    hp_bat['hp_bnd_pct'] = hp_bat['hp_bnds'] / hp_bat['hp_balls'].replace(0, np.nan) * 100
    hp_bat['hp_dot_pct'] = hp_bat['hp_dots'] / hp_bat['hp_balls'].replace(0, np.nan) * 100

    death_bat = df_s[df_s['overid'] >= 16].groupby('striker_id').agg(d_runs=('runs', 'sum'), d_balls=('is_batter_ball', 'sum'))
    death_bat['death_sr'] = death_bat['d_runs'] / death_bat['d_balls'].replace(0, np.nan) * 100

    chase_bat = df_s[(df_s['innings'] == 2) & (df_s['rrr'] >= 10.5)].groupby('striker_id').agg(c_runs=('runs', 'sum'), c_balls=('is_batter_ball', 'sum'))
    chase_bat['chase_sr'] = chase_bat['c_runs'] / chase_bat['c_balls'].replace(0, np.nan) * 100

    coll_bat = df_s[df_s['is_collapse']].groupby('striker_id').agg(co_runs=('runs', 'sum'), co_balls=('is_batter_ball', 'sum'))
    coll_bat['coll_sr'] = coll_bat['co_runs'] / coll_bat['co_balls'].replace(0, np.nan) * 100

    bat_table = overall_bat.join(hp_bat).join(death_bat[['death_sr']]).join(chase_bat[['chase_sr']]).join(coll_bat[['coll_sr']]).reset_index().rename(columns={'striker_id': 'player_id'})
    bat_table = bat_table.merge(_player_meta, on='player_id', how='left')
    bat_qual = bat_table[(bat_table['hp_balls'] >= min_balls) & (bat_table['category'].isin(origin_tuple))].copy()
    bat_qual['sr_retention'] = (bat_qual['hp_sr'] / bat_qual['overall_sr']) * 100
    bat_qual['BPRS'] = (
        0.30 * minmax(bat_qual['hp_rec_sr'].clip(110, 200)) +
        0.25 * minmax(bat_qual['hp_bpd'].clip(10, 35)) +
        0.20 * minmax(bat_qual['hp_bnd_pct'].clip(12, 35)) +
        0.15 * minmax(100 - bat_qual['hp_dot_pct'].clip(20, 50)) +
        0.10 * minmax(bat_qual['sr_retention'].clip(80, 120))
    ) * 100

    # Fast vectorized bowling aggregations
    overall_bowl = df_s.groupby('bowler_id').agg(tot_balls=('is_legal_ball', 'sum'), tot_runs=('bowler_runs', 'sum'))
    overall_bowl['overall_econ'] = overall_bowl['tot_runs'] / (overall_bowl['tot_balls'] / 6).replace(0, np.nan)

    hp_bowl = df_s[is_hp].groupby('bowler_id').agg(
        hp_balls=('is_legal_ball', 'sum'),
        hp_runs=('bowler_runs', 'sum'),
        hp_wkts=('is_bowler_wicket', 'sum'),
        hp_dots=('is_dot_bowl', 'sum'),
        hp_bnds=('is_boundary', 'sum'),
        rec_runs=('rec_bowl_runs', 'sum'),
        rec_balls=('rec_bowl_balls', 'sum'),
        rec_wkts=('rec_bowl_wkts', 'sum')
    )
    hp_bowl['hp_econ'] = hp_bowl['hp_runs'] / (hp_bowl['hp_balls'] / 6).replace(0, np.nan)
    hp_bowl['hp_rec_econ'] = hp_bowl['rec_runs'] / (hp_bowl['rec_balls'] / 6).replace(0, np.nan)
    hp_bowl['hp_sr'] = hp_bowl['hp_balls'] / hp_bowl['hp_wkts'].replace(0, np.nan)
    hp_bowl['hp_rec_sr'] = hp_bowl['rec_balls'] / hp_bowl['rec_wkts'].replace(0, np.nan)
    hp_bowl['hp_dot_pct'] = hp_bowl['hp_dots'] / hp_bowl['hp_balls'].replace(0, np.nan) * 100
    hp_bowl['hp_bnd_pct'] = hp_bowl['hp_bnds'] / hp_bowl['hp_balls'].replace(0, np.nan) * 100

    death_bowl = df_s[df_s['overid'] >= 16].groupby('bowler_id').agg(
        d_balls=('is_legal_ball', 'sum'), d_runs=('bowler_runs', 'sum'), d_wkts=('is_bowler_wicket', 'sum')
    )
    death_bowl['death_econ'] = death_bowl['d_runs'] / (death_bowl['d_balls'] / 6).replace(0, np.nan)
    death_bowl['death_sr'] = death_bowl['d_balls'] / death_bowl['d_wkts'].replace(0, np.nan)

    bowl_table = overall_bowl.join(hp_bowl).join(death_bowl[['death_econ', 'death_sr']]).reset_index().rename(columns={'bowler_id': 'player_id'})
    bowl_table = bowl_table.merge(_player_meta, on='player_id', how='left')
    bowl_qual = bowl_table[(bowl_table['hp_balls'] >= min_balls) & (bowl_table['category'].isin(origin_tuple))].copy()
    bowl_qual['econ_resilience'] = (bowl_qual['overall_econ'] / bowl_qual['hp_econ']) * 100
    bowl_qual['BWPRS'] = (
        0.30 * minmax(12.0 - bowl_qual['hp_rec_econ'].clip(6.5, 11.5)) +
        0.25 * minmax(30.0 - bowl_qual['hp_rec_sr'].clip(10.0, 28.0)) +
        0.20 * minmax(bowl_qual['hp_dot_pct'].clip(22.0, 48.0)) +
        0.15 * minmax(22.0 - bowl_qual['hp_bnd_pct'].clip(8.0, 22.0)) +
        0.10 * minmax(bowl_qual['econ_resilience'].clip(75.0, 110.0))
    ) * 100

    dpi_dist = df_s.groupby('dpi', as_index=False).size().rename(columns={'size': 'Deliveries'})
    dpi_dist['Regime'] = np.where(dpi_dist['dpi'] >= dpi_threshold, f'High Pressure (DPI ≥ {dpi_threshold})', 'Standard Leverage')

    return bat_qual, bowl_qual, dpi_dist, hp_count, tot_count, hp_pct

bbb_m, player_meta = load_base_engine()
rr_bat26, rr_bowl26, bat_p, bowl_p = get_ipl26_audit(bbb_m)

with st.sidebar:
    st.subheader("Scouting Controls")
    dpi_threshold = st.slider("Min Pressure Index (DPI)", min_value=20, max_value=70, value=30, step=5)
    min_balls = st.slider("Min High-Pressure Balls", min_value=60, max_value=300, value=120, step=20)
    origin_filter = st.multiselect(
        "IPL Eligibility Pool",
        options=['India', 'Overseas (IPL-Eligible)', 'Pakistan (Ineligible)'],
        default=['India', 'Overseas (IPL-Eligible)']
    )
    all_seasons = sorted(bbb_m['season_year'].unique().tolist())
    season_range = st.multiselect(
        "Seasons Scope",
        options=all_seasons,
        default=all_seasons
    )

bat_qual, bowl_qual, dpi_dist, hp_balls, tot_balls, hp_pct = compute_leaderboards(
    bbb_m, player_meta, dpi_threshold, min_balls, tuple(origin_filter), tuple(season_range)
)

def style_chart(fig, height=410):
    fig.update_layout(
        height=height,
        font=dict(family="DM Sans, sans-serif", size=12, color="#94A3B8"),
        title_font=dict(family="Space Grotesk, sans-serif", size=14, color="#F8FAFC"),
        plot_bgcolor="#0A1324",
        paper_bgcolor="#0A1324",
        margin=dict(l=26, r=22, t=50, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=None,
            font=dict(size=11, color="#94A3B8")
        ),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.1)",
            tickfont=dict(size=11, color="#94A3B8"),
            title_font=dict(size=12, color="#CBD5E1")
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.1)",
            tickfont=dict(size=11, color="#94A3B8"),
            title_font=dict(size=12, color="#CBD5E1")
        ),
        hoverlabel=dict(
            bgcolor="#0E192E",
            bordercolor="rgba(232, 18, 125, 0.4)",
            font=dict(family="DM Sans, sans-serif", size=12, color="#F8FAFC")
        )
    )
    return fig

st.markdown("""
<div class="rr-header">
<div class="rr-header-top">
<div class="rr-crest">
<span>RAJASTHAN ROYALS</span>
</div>
<div class="rr-status-beacon">
<span class="rr-status-dot"></span>
ACTIVE SCOUTING ENGINE · 200,999 DELIVERIES
</div>
</div>
<h1 class="rr-title">IPL 2027 Mega-Auction War Room</h1>
<div class="rr-subtitle">
Delivery-level leverage modeling isolating death-over execution, collapse mitigation, and steep run-chase resilience across 867 T20 matches (2022–2026).
</div>
<div class="rr-strip">
<span class="rr-pill rr-pill-accent">PURSE: <strong>₹120.0 CR</strong></span>
<span class="rr-pill">RETENTIONS: <strong>6 PLAYERS</strong></span>
<span class="rr-pill">OVERSEAS SLOTS: <strong>2 VACANT (4 MAX)</strong></span>
<span class="rr-pill rr-pill-gold">PRIMARY NEED: <strong>DEATH FINISHER & SEAM ENFORCER</strong></span>
</div>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
<div class="analyst-card">
<div class="card-eyebrow">
<span>Leverage Sample</span>
<span class="pill-tag-pink">DPI ≥ {dpi_threshold}</span>
</div>
<div class="card-value">{hp_balls:,} <span style="font-size:13px;color:#94A3B8;">balls</span></div>
<div class="card-sub"><span style="color:#FF4D9E;font-weight:600;">{hp_pct:.1f}%</span> of {tot_balls:,} deliveries indexed</div>
</div>
""", unsafe_allow_html=True)

with k2:
    st.markdown("""
<div class="analyst-card">
<div class="card-eyebrow">
<span>RR 2026 Death Batting</span>
<span class="pill-tag-gold">Overs 16–20</span>
</div>
<div class="card-value">10.31 <span style="font-size:13px;color:#94A3B8;">RPO</span></div>
<div class="card-sub"><span style="color:#E5C368;font-weight:600;">-0.49 RPO</span> vs league avg (10.80 benchmark)</div>
</div>
""", unsafe_allow_html=True)

with k3:
    st.markdown("""
<div class="analyst-card">
<div class="card-eyebrow">
<span>RR Middle Dot-Ball Deficit</span>
<span class="pill-tag-blue">Overs 7–15</span>
</div>
<div class="card-value">25.6% <span style="font-size:13px;color:#94A3B8;">dots</span></div>
<div class="card-sub"><span style="color:#93C5FD;font-weight:600;">-3.2%</span> below 28.8% league middle containment</div>
</div>
""", unsafe_allow_html=True)

with k4:
    st.markdown("""
<div class="analyst-card">
<div class="card-eyebrow">
<span>#1 Target Score</span>
<span class="pill-tag-pink">Priority Target</span>
</div>
<div class="card-value">78.3 <span style="font-size:13px;color:#94A3B8;">BPRS</span></div>
<div class="card-sub">Shashank Singh · 182.8 HP SR · 195.4 Death SR</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "01 · RR 2026 Diagnostic",
    "02 · Batting Leverage (BPRS)",
    "03 · Bowling Leverage (BWPRS)",
    "04 · 2027 Blueprint & XII",
    "05 · Model Architecture"
])

with tab1:
    st.markdown('<div class="section-title">Rajasthan Royals · IPL 2026 Season Audit (9W – 7L)</div>', unsafe_allow_html=True)

    c_bat, c_bowl = st.columns(2)
    with c_bat:
        st.markdown("**RR IPL 2026 Batting Output**")
        st.dataframe(
            rr_bat26,
            use_container_width=True,
            hide_index=True,
            column_config={
                "SR": st.column_config.NumberColumn("Strike Rate", format="%.1f"),
                "Runs": st.column_config.ProgressColumn("Total Runs", min_value=0, max_value=int(rr_bat26['Runs'].max()), format="%d"),
                "Balls": st.column_config.NumberColumn("Balls", format="%d")
            }
        )

    with c_bowl:
        st.markdown("**RR IPL 2026 Bowling Output**")
        st.dataframe(
            rr_bowl26,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Econ": st.column_config.NumberColumn("Economy", format="%.2f"),
                "Wkts": st.column_config.ProgressColumn("Wickets", min_value=0, max_value=int(rr_bowl26['Wkts'].max()), format="%d"),
                "Balls": st.column_config.NumberColumn("Balls", format="%d")
            }
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        fig_bat_p = px.bar(
            bat_p, x='phase', y='Run Rate', color='Team', barmode='group', text='Run Rate',
            color_discrete_map={'Rajasthan Royals': '#E8127D', 'IPL 2026 League Avg': '#253E68'},
            title="Batting Run Rate by Phase: RR vs. IPL 2026 League Benchmark",
            category_orders={'phase': ['Powerplay (1-6)', 'Middle (7-15)', 'Death (16-20)']}
        )
        fig_bat_p.update_traces(textposition='outside', marker_line_width=0, textfont=dict(color='#F8FAFC'))
        st.plotly_chart(style_chart(fig_bat_p, 380), use_container_width=True)

    with g2:
        fig_bowl_p = px.bar(
            bowl_p, x='phase', y='Dot %', color='Bowl_Team', barmode='group', text='Dot %',
            color_discrete_map={'Rajasthan Royals': '#E8127D', 'IPL 2026 League Avg': '#253E68'},
            title="Bowling Dot-Ball % by Phase: RR vs. IPL 2026 League Benchmark",
            category_orders={'phase': ['Powerplay (1-6)', 'Middle (7-15)', 'Death (16-20)']}
        )
        fig_bowl_p.update_traces(textposition='outside', marker_line_width=0, textfont=dict(color='#F8FAFC'))
        st.plotly_chart(style_chart(fig_bowl_p, 380), use_container_width=True)

with tab2:
    st.markdown('<div class="section-title">Batting Pressure Reliability Score (BPRS Leaderboard)</div>', unsafe_allow_html=True)

    role_choice = st.radio(
        "Role Filter:",
        ["All Qualified Batters", "Middle & Lower-Order Finishers (Pos ≥ 4.5)", "Top-Order (Pos < 4.5)"],
        horizontal=True
    )

    bat_view = bat_qual
    if "Finishers" in role_choice:
        bat_view = bat_view[bat_view['avg_bat_order'] >= 4.5]
    elif "Top-Order" in role_choice:
        bat_view = bat_view[bat_view['avg_bat_order'] < 4.5]

    bat_sorted = bat_view.sort_values('BPRS', ascending=False)

    disp_bat = bat_sorted[[
        'player_name', 'category', 'ipl_2026_team', 'avg_bat_order', 'hp_balls', 'hp_runs',
        'hp_sr', 'hp_rec_sr', 'hp_bpd', 'hp_bnd_pct', 'death_sr', 'chase_sr', 'coll_sr', 'BPRS'
    ]].rename(columns={
        'player_name': 'Player', 'category': 'Pool', 'ipl_2026_team': '2026 Team',
        'avg_bat_order': 'Pos', 'hp_balls': 'HP Balls', 'hp_runs': 'HP Runs',
        'hp_sr': 'HP SR', 'hp_rec_sr': 'Rec SR', 'hp_bpd': 'Balls/Out',
        'hp_bnd_pct': 'Bnd %', 'death_sr': 'Death SR', 'chase_sr': 'Chase SR', 'coll_sr': 'Collapse SR'
    }).round(1)

    st.dataframe(
        disp_bat,
        use_container_width=True,
        hide_index=True,
        height=390,
        column_config={
            "BPRS": st.column_config.ProgressColumn("BPRS Score", min_value=0, max_value=100, format="%.1f"),
            "HP SR": st.column_config.NumberColumn("HP SR", format="%.1f"),
            "Death SR": st.column_config.NumberColumn("Death SR", format="%.1f"),
            "Balls/Out": st.column_config.NumberColumn("Balls/Out", format="%.1f"),
            "Bnd %": st.column_config.NumberColumn("Bnd %", format="%.1f%%")
        }
    )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    fig_bat = px.scatter(
        bat_sorted.head(30),
        x='hp_bpd', y='hp_sr', size='hp_balls', color='category',
        hover_name='player_name',
        hover_data={'ipl_2026_team': True, 'BPRS': ':.1f', 'death_sr': ':.1f'},
        text='player_name',
        color_discrete_map={
            'India': '#E8127D',
            'Overseas (IPL-Eligible)': '#D4AF37',
            'Pakistan (Ineligible)': '#475569'
        },
        labels={'hp_bpd': 'Wicket Preservation (Balls per Dismissal under Pressure)', 'hp_sr': 'High-Pressure Strike Rate'},
        title="Top 30 Clutch Batters: Strike Rate vs. Wicket Preservation (Top-Right = Elite Outliers)"
    )
    fig_bat.update_traces(textposition='top center', textfont=dict(size=10, color='#CBD5E1'), marker=dict(opacity=0.9, line=dict(width=1, color='#070D18')))
    st.plotly_chart(style_chart(fig_bat, 480), use_container_width=True)

    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("""
<div class="scout-card">
<div class="scout-header">
<div>
<div class="scout-name">Shashank Singh</div>
<div class="scout-meta">PBKS (2026) · Right-Hand Middle/Death Finisher (#5–6)</div>
</div>
<span class="pill-tag-pink">78.3 BPRS (#1 IND)</span>
</div>
<div class="scout-grid">
<div class="scout-metric">
<div class="scout-metric-label">High-Pressure SR</div>
<div class="scout-metric-val" style="color:#FF4D9E;">182.8</div>
</div>
<div class="scout-metric">
<div class="scout-metric-label">Death Overs SR</div>
<div class="scout-metric-val" style="color:#FF4D9E;">195.4</div>
</div>
<div class="scout-metric">
<div class="scout-metric-label">Balls / Dismissal</div>
<div class="scout-metric-val">26.2</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    with sc2:
        st.markdown("""
<div class="scout-card">
<div class="scout-header">
<div>
<div class="scout-name">Naman Dhir</div>
<div class="scout-meta">MI (2026) · RHB / Auxiliary Off-Spin (#5)</div>
</div>
<span class="pill-tag-pink">73.7 BPRS (#2 IND)</span>
</div>
<div class="scout-grid">
<div class="scout-metric">
<div class="scout-metric-label">High-Pressure SR</div>
<div class="scout-metric-val" style="color:#FF4D9E;">201.1</div>
</div>
<div class="scout-metric">
<div class="scout-metric-label">Boundary %</div>
<div class="scout-metric-val" style="color:#FF4D9E;">30.8%</div>
</div>
<div class="scout-metric">
<div class="scout-metric-label">Collapse Rescue SR</div>
<div class="scout-metric-val">174.5</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-title">Bowling Pressure Reliability Score (BWPRS Leaderboard)</div>', unsafe_allow_html=True)

    bowl_type_filter = st.radio("Discipline Filter:", ["All Bowlers", "Pace / Seam", "Spin"], horizontal=True)

    bowl_view = bowl_qual
    if bowl_type_filter == "Pace / Seam":
        bowl_view = bowl_view[bowl_view['bowling_type'].str.contains('fast|medium', case=False, na=False)]
    elif bowl_type_filter == "Spin":
        bowl_view = bowl_view[~bowl_view['bowling_type'].str.contains('fast|medium', case=False, na=False)]

    bowl_sorted = bowl_view.sort_values('BWPRS', ascending=False)

    disp_bowl = bowl_sorted[[
        'player_name', 'category', 'ipl_2026_team', 'bowling_type', 'hp_balls', 'hp_wkts',
        'hp_econ', 'hp_rec_econ', 'hp_sr', 'hp_dot_pct', 'death_econ', 'death_sr', 'BWPRS'
    ]].rename(columns={
        'player_name': 'Player', 'category': 'Pool', 'ipl_2026_team': '2026 Team',
        'bowling_type': 'Style', 'hp_balls': 'HP Balls', 'hp_wkts': 'HP Wkts',
        'hp_econ': 'HP Econ', 'hp_rec_econ': 'Rec Econ', 'hp_sr': 'HP SR',
        'hp_dot_pct': 'Dot %', 'death_econ': 'Death Econ', 'death_sr': 'Death SR'
    }).round(2)

    st.dataframe(
        disp_bowl,
        use_container_width=True,
        hide_index=True,
        height=390,
        column_config={
            "BWPRS": st.column_config.ProgressColumn("BWPRS Score", min_value=0, max_value=100, format="%.1f"),
            "HP Econ": st.column_config.NumberColumn("HP Econ", format="%.2f"),
            "Death Econ": st.column_config.NumberColumn("Death Econ", format="%.2f"),
            "Dot %": st.column_config.NumberColumn("Dot %", format="%.1f%%")
        }
    )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    fig_bowl = px.scatter(
        bowl_sorted.head(30),
        x='hp_econ', y='hp_sr', size='hp_balls', color='category',
        hover_name='player_name',
        hover_data={'ipl_2026_team': True, 'BWPRS': ':.1f', 'death_econ': ':.2f'},
        text='player_name',
        color_discrete_map={
            'India': '#E8127D',
            'Overseas (IPL-Eligible)': '#D4AF37',
            'Pakistan (Ineligible)': '#475569'
        },
        labels={'hp_econ': 'High-Pressure Economy (Inverted: Right = Lower Economy)', 'hp_sr': 'High-Pressure Bowling SR (Inverted: Top = Faster Wickets)'},
        title="Top 30 Bowlers: Economy Rate vs. Strike Rate (Top-Right = Elite Enforcers)"
    )
    fig_bowl.update_traces(textposition='top center', textfont=dict(size=10, color='#CBD5E1'), marker=dict(opacity=0.9, line=dict(width=1, color='#070D18')))
    fig_bowl.update_yaxes(autorange="reversed")
    fig_bowl.update_xaxes(autorange="reversed")
    st.plotly_chart(style_chart(fig_bowl, 480), use_container_width=True)

    bd1, bd2 = st.columns(2)
    with bd1:
        st.markdown("""
<div class="scout-card">
<div class="scout-header">
<div>
<div class="scout-name">Corbin Bosch</div>
<div class="scout-meta">MI (2026) · Right-Arm Fast-Medium All-Rounder (SA)</div>
</div>
<span class="pill-tag-gold">73.0 BWPRS (#2 Pace)</span>
</div>
<div class="scout-grid">
<div class="scout-metric">
<div class="scout-metric-label">High-Pressure Econ</div>
<div class="scout-metric-val" style="color:#F1D278;">8.37</div>
</div>
<div class="scout-metric">
<div class="scout-metric-label">Dot Ball %</div>
<div class="scout-metric-val" style="color:#F1D278;">49.7%</div>
</div>
<div class="scout-metric">
<div class="scout-metric-label">Death Overs Econ</div>
<div class="scout-metric-val">9.12</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    with bd2:
        st.markdown("""
<div class="scout-card">
<div class="scout-header">
<div>
<div class="scout-name">Mujeeb Ur Rahman</div>
<div class="scout-meta">Free Agent (2026) · Mystery Off-Spin / Carrom (AFG)</div>
</div>
<span class="pill-tag-gold">69.8 BWPRS (#1 Spin Target)</span>
</div>
<div class="scout-grid">
<div class="scout-metric">
<div class="scout-metric-label">High-Pressure Econ</div>
<div class="scout-metric-val" style="color:#F1D278;">7.76</div>
</div>
<div class="scout-metric">
<div class="scout-metric-label">Bowling SR</div>
<div class="scout-metric-val" style="color:#F1D278;">16.8</div>
</div>
<div class="scout-metric">
<div class="scout-metric-label">Dot Ball %</div>
<div class="scout-metric-val">42.4%</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-title">IPL 2027 Auction Target Matrix & Projected Playing XII</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="quota-box">
<div class="quota-title">
<span>🛡️ OVERSEAS REGISTRATION ALLOCATION</span>
<span class="pill-tag-pink">4 / 4 SLOTS ACCOUNTED</span>
</div>
<div class="quota-chips">
<span class="quota-chip quota-chip-locked">OS #1: Donovan Ferreira (Retained Finisher)</span>
<span class="quota-chip quota-chip-target">OS #2: Corbin Bosch / Jamie Overton (Target Seamer)</span>
<span class="quota-chip quota-chip-locked">OS #3: Jofra Archer (Retained Spearhead)</span>
<span class="quota-chip quota-chip-target">OS #4: Mujeeb Ur Rahman / Impact Sub (Target Spinner)</span>
</div>
</div>
""", unsafe_allow_html=True)

    c_left, c_right = st.columns([1.1, 1])
    with c_left:
        st.markdown("**Auction Target Shortlist**")
        targets_df = pd.DataFrame([
            {"Tier": "Tier 1", "Target": "Shashank Singh", "Pool": "IND", "Team": "PBKS", "Role": "Finisher (#5–6)", "Profile": "78.3 BPRS · 182.8 HP SR · 26.2 BPD"},
            {"Tier": "Tier 1", "Target": "Naman Dhir", "Pool": "IND", "Team": "MI", "Role": "Finisher / Off-Spin", "Profile": "73.7 BPRS · 201.1 HP SR · 30.8% Bnd%"},
            {"Tier": "Tier 1", "Target": "Corbin Bosch", "Pool": "OS (SA)", "Team": "MI", "Role": "Death Pace All-Rounder", "Profile": "73.0 BWPRS · 8.37 Econ · 49.7% Dots"},
            {"Tier": "Tier 1", "Target": "Jamie Overton", "Pool": "OS (ENG)", "Team": "CSK", "Role": "Death Seamer / Hitter", "Profile": "67.3 BWPRS · 7.48 HP SR · 6.85 Death SR"},
            {"Tier": "Tier 1", "Target": "Mujeeb Ur Rahman", "Pool": "OS (AFG)", "Team": "Free Agent", "Role": "PP & Middle Spin", "Profile": "69.8 BWPRS · 7.76 Econ · 42.4% Dots"},
            {"Tier": "Tier 2", "Target": "Gurjapneet Singh", "Pool": "IND", "Team": "CSK", "Role": "Left-Arm Pace", "Profile": "64.6 BWPRS · 8.48 Econ · 8.88 Death Econ"},
            {"Tier": "Tier 2", "Target": "Cooper Connolly", "Pool": "OS (AUS)", "Team": "PBKS", "Role": "LHB Middle / SLA Spin", "Profile": "67.2 BPRS · 176.9 HP SR · 237.8 Death SR"}
        ])
        st.dataframe(targets_df, use_container_width=True, hide_index=True)

    with c_right:
        st.markdown("**Projected IPL 2027 Playing XII (With Impact Sub)**")
        xii_df = pd.DataFrame([
            {"#": 1, "Player": "Yashasvi Jaiswal", "Status": "RETAINED (IND)", "Role": "LHB Opener (152.5 SR)"},
            {"#": 2, "Player": "Vaibhav Sooryavanshi", "Status": "RETAINED (IND)", "Role": "LHB Opener (776 runs @ 237.3 SR)"},
            {"#": 3, "Player": "Riyan Parag", "Status": "RETAINED (IND)", "Role": "RHB Anchor / Spin (157.7 SR)"},
            {"#": 4, "Player": "Dhruv Jurel (WK)", "Status": "RETAINED (IND)", "Role": "RHB / Wicketkeeper (515 runs @ 154.7 SR)"},
            {"#": 5, "Player": "Naman Dhir", "Status": "BUY TARGET (IND)", "Role": "RHB / Off-Spin (201.1 HP SR)"},
            {"#": 6, "Player": "Shashank Singh", "Status": "BUY TARGET (IND)", "Role": "RHB Finisher (195.4 Death SR)"},
            {"#": 7, "Player": "Donovan Ferreira", "Status": "RETAINED (OS #1)", "Role": "RHB Death Hitter (179.1 SR)"},
            {"#": 8, "Player": "Ravindra Jadeja", "Status": "RETAINED (IND)", "Role": "LHB / SLA Spin (8.58 Econ)"},
            {"#": 9, "Player": "Corbin Bosch / Overton", "Status": "BUY TARGET (OS #2)", "Role": "Death Pace All-Rounder (8.37 Econ)"},
            {"#": 10, "Player": "Jofra Archer", "Status": "RETAINED (OS #3)", "Role": "Pace Spearhead (25 Wkts @ 9.43)"},
            {"#": 11, "Player": "Ravi Bishnoi", "Status": "RETAINED (IND)", "Role": "Leg-Break Strike Spinner"},
            {"#": 12, "Player": "Gurjapneet / Mujeeb (OS #4)", "Status": "IMPACT SUB", "Role": "Left-Arm Pace or Mystery Spin Matchup"}
        ])
        st.dataframe(xii_df, use_container_width=True, hide_index=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    upgrade_df = pd.DataFrame([
        {"Slot": "Finishing Battery (#5–6)", "Player": "Shimron Hetmyer (RR 2026)", "Value": 113.0, "Type": "2026 Outgoing"},
        {"Slot": "Finishing Battery (#5–6)", "Player": "Shashank Singh", "Value": 182.8, "Type": "2027 Target"},
        {"Slot": "Finishing Battery (#5–6)", "Player": "Naman Dhir", "Value": 201.1, "Type": "2027 Target"},
        {"Slot": "Support Seam Attack", "Player": "Tushar Deshpande (RR 2026)", "Value": 12.26, "Type": "2026 Outgoing"},
        {"Slot": "Support Seam Attack", "Player": "Corbin Bosch", "Value": 8.37, "Type": "2027 Target"},
        {"Slot": "Support Seam Attack", "Player": "Gurjapneet Singh", "Value": 8.48, "Type": "2027 Target"}
    ])

    u1, u2 = st.columns(2)
    with u1:
        fig_u1 = px.bar(
            upgrade_df[upgrade_df['Slot'] == "Finishing Battery (#5–6)"],
            x='Player', y='Value', color='Type', text='Value',
            color_discrete_map={'2026 Outgoing': '#253E68', '2027 Target': '#E8127D'},
            title="Finishing Upgrade: High-Pressure Strike Rate (2026 vs 2027 Targets)",
            labels={'Value': 'Strike Rate'}
        )
        fig_u1.update_traces(textposition='outside', marker_line_width=0, textfont=dict(color='#F8FAFC'))
        st.plotly_chart(style_chart(fig_u1, 350), use_container_width=True)

    with u2:
        fig_u2 = px.bar(
            upgrade_df[upgrade_df['Slot'] == "Support Seam Attack"],
            x='Player', y='Value', color='Type', text='Value',
            labels={'Value': 'Economy Rate'},
            color_discrete_map={'2026 Outgoing': '#253E68', '2027 Target': '#D4AF37'},
            title="Bowling Upgrade: High-Pressure Economy Rate (Lower = Better)",
        )
        fig_u2.update_traces(textposition='outside', marker_line_width=0, textfont=dict(color='#F8FAFC'))
        st.plotly_chart(style_chart(fig_u2, 350), use_container_width=True)

with tab5:
    st.markdown('<div class="section-title">Underlying Datasets & Delivery Pressure Index (DPI) Formulation</div>', unsafe_allow_html=True)

    ref_df = pd.DataFrame([
        {"Data Source": "ball_by_ball.csv", "Deliveries / Rows": "200,999", "Dimensions": 33, "Join Keys": "match_id, striker_id, bowler_id", "Analytical Role": "Delivery runs, extras, dismissals, phase, bowling style"},
        {"Data Source": "matches.csv", "Deliveries / Rows": "883", "Dimensions": 22, "Join Keys": "match_id, comp_id, win_team_id", "Analytical Role": "Dates, match stages, knockout flags, DLS target revisions"},
        {"Data Source": "competitions.csv", "Deliveries / Rows": "141", "Dimensions": 4, "Join Keys": "comp_id", "Analytical Role": "Seasons (2022–2026) and tournament format segregation"},
        {"Data Source": "playing_eleven.csv", "Deliveries / Rows": "28,381", "Dimensions": 9, "Join Keys": "match_id, team_id, player_id", "Analytical Role": "Batting position tracking and Impact Sub tracking"},
        {"Data Source": "competition_team_player_mapping.csv", "Deliveries / Rows": "6,413", "Dimensions": 6, "Join Keys": "comp_id, team_id, player_id", "Analytical Role": "Master player names and franchise rosters"},
        {"Data Source": "teams.csv", "Deliveries / Rows": "353", "Dimensions": 3, "Join Keys": "comp_id, team_id", "Analytical Role": "Franchise and international team identifiers"}
    ])
    st.dataframe(ref_df, use_container_width=True, hide_index=True)

    st.markdown("**DPI 5-Factor Leverage Additive Points**")
    dpi_rules = pd.DataFrame([
        {"Condition": "Death Overs", "Points": "+30 PTS", "Analytical Trigger": "Overs 16.1 through 20.0 in either innings"},
        {"Condition": "High-RRR Chase", "Points": "+30 PTS", "Analytical Trigger": "Innings 2 with RRR ≥ 10.5 or (Overs ≥ 15 with 8.5 ≤ RRR ≤ 18.0)"},
        {"Condition": "Collapse Mitigation", "Points": "+25 PTS", "Analytical Trigger": "≥ 2 wickets in Powerplay, ≥ 3 wickets by Over 10, or ≥ 5 wickets down"},
        {"Condition": "Knockout Stakes", "Points": "+20 PTS", "Analytical Trigger": "Finals, Qualifiers, Eliminators, Semi-Finals, Super 4s"},
        {"Condition": "Bowling Siege", "Points": "+15 PTS", "Analytical Trigger": "Bowling in Overs 7–20 after conceding ≥ 60 runs in the Powerplay"}
    ])
    st.dataframe(dpi_rules, use_container_width=True, hide_index=True)

    fig_dpi = px.bar(
        dpi_dist, x='dpi', y='Deliveries', color='Regime',
        color_discrete_map={f'High Pressure (DPI ≥ {dpi_threshold})': '#E8127D', 'Standard Leverage': '#182642'},
        labels={'dpi': 'DPI Score', 'Deliveries': 'Number of Deliveries'},
        title="DPI Leverage Distribution Across 200,999 Deliveries"
    )
    fig_dpi.update_traces(marker_line_width=0)
    st.plotly_chart(style_chart(fig_dpi, 320), use_container_width=True)
import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Rajasthan Royals | IPL 2027 Auction Scouting",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">

<style>
    :root { color-scheme: light !important; }

    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F4F6FA !important;
        color: #111827 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp p, .stApp label, .stApp li,
    [data-testid="stMarkdownContainer"] p, [data-testid="stWidgetLabel"] p {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded' !important;
    }

    h1, h2, h3, h4, .page-title, .card-name, .table-head-title {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        letter-spacing: -0.02em;
        color: #17316B !important;
    }

    .mono, .kpi-number, .stat-val {
        font-family: 'JetBrains Mono', monospace !important;
        font-variant-numeric: tabular-nums;
    }

    .block-container {
        padding-top: 2.2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2.1rem !important;
        padding-right: 2.1rem !important;
        max-width: 1400px !important;
    }

    /* Polished Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }
    .sb-title {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #17316B !important;
        padding-bottom: 10px;
        margin-bottom: 14px;
        border-bottom: 1px solid #E2E8F0;
    }

    /* Royals Masthead */
    .rr-banner {
        background: linear-gradient(180deg, #FFFFFF 0%, #FAFBFD 100%);
        border: 1px solid #E2E8F0;
        border-top: 4px solid #17316B;
        border-radius: 10px;
        padding: 22px 26px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(15, 23, 42, 0.02);
    }
    .rr-banner-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 6px;
    }
    .rr-team-line {
        font-size: 11.5px;
        font-weight: 700;
        color: #E51A7A;
        letter-spacing: 0.06em;
    }
    .sample-pill {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px;
        color: #17316B;
        background: #EEF2FF;
        border: 1px solid #DBEAFE;
        padding: 3px 10px;
        border-radius: 999px;
        font-weight: 600;
    }
    .page-title {
        font-size: 25px !important;
        font-weight: 800 !important;
        color: #17316B !important;
        margin: 0 0 6px 0 !important;
        line-height: 1.2 !important;
    }
    .page-lead {
        font-size: 14px;
        color: #475569;
        line-height: 1.5;
        margin: 0;
        max-width: 920px;
    }
    .squad-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 18px;
        margin-top: 15px;
        padding-top: 13px;
        border-top: 1px solid #E2E8F0;
        font-size: 12.5px;
        color: #475569;
    }
    .squad-strip strong {
        color: #17316B;
        font-weight: 700;
    }

    /* Restored 4 Hero Stat Cards with Subtle Elevation */
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 17px 19px;
        height: 100%;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(15, 23, 42, 0.02);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stat-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(23, 49, 107, 0.07);
    }
    .stat-card-pink { border-top: 3px solid #E51A7A; }
    .stat-card-blue { border-top: 3px solid #17316B; }
    .stat-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 6px;
        margin-bottom: 8px;
    }
    .stat-label {
        font-size: 11.5px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .kpi-number {
        font-size: 25px;
        font-weight: 700;
        color: #111827;
        line-height: 1.15;
        margin-bottom: 6px;
    }
    .stat-note {
        font-size: 12.5px;
        color: #475569;
        line-height: 1.35;
    }

    /* Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #E2E8F0;
        padding: 4px;
        border-radius: 9px;
        margin-top: 18px;
        margin-bottom: 1.2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 38px;
        border-radius: 7px;
        padding: 0 18px;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #475569 !important;
        background: transparent !important;
        border: none !important;
        transition: all 0.15s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #17316B !important;
        background: rgba(255, 255, 255, 0.55) !important;
    }
    .stTabs [aria-selected="true"] {
        background: #17316B !important;
        color: #FFFFFF !important;
        box-shadow: 0 1px 3px rgba(23, 49, 107, 0.25) !important;
    }
    .stTabs [data-baseweb="tab-border"], .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* Section Header Bar Above Tables */
    .table-head-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .table-head-title {
        font-size: 14.5px;
        font-weight: 700;
        color: #17316B !important;
    }

    /* Player Spotlight Cards */
    .panel-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 12px;
    }
    .card-name {
        font-size: 16px;
        font-weight: 700;
        color: #17316B !important;
    }
    .card-role {
        font-size: 12px;
        color: #64748B;
        margin-top: 2px;
    }
    .tag-pink {
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 5px;
        background: #FDF2F8;
        color: #BE185D;
        border: 1px solid #FBCFE8;
    }
    .tag-navy {
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 5px;
        background: #EFF6FF;
        color: #17316B;
        border: 1px solid #BFDBFE;
    }
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
    }
    .stat-cell {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 7px;
        padding: 9px 11px;
    }
    .stat-lbl {
        font-size: 10.5px;
        font-weight: 600;
        color: #64748B;
    }
    .stat-val {
        font-size: 15px;
        font-weight: 700;
        color: #111827;
        margin-top: 3px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        background: #FFFFFF !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. FAST PARQUET-BACKED ENGINE
# ---------------------------------------------------------
@st.cache_resource(show_spinner="Loading ball-by-ball dataset...")
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

    bbb_m['is_dot_bat'] = (bbb_m['total_runs'] == 0) & bbb_m['is_batter_ball']
    bbb_m['bowler_runs'] = np.where(bbb_m['extras_type'].isin(['byes', 'legbyes', 'Penalty']), 0, bbb_m['total_runs']).astype('int16')
    bbb_m['is_dot_bowl'] = (bbb_m['bowler_runs'] == 0) & bbb_m['is_legal_ball']
    bbb_m['is_dot_any'] = (bbb_m['total_runs'] == 0) & bbb_m['is_legal_ball']

    bbb_m['rec_bat_runs'] = (bbb_m['runs'] * recency_wt).astype('float32')
    bbb_m['rec_bat_balls'] = (bbb_m['is_batter_ball'] * recency_wt).astype('float32')
    bbb_m['rec_bowl_runs'] = (bbb_m['bowler_runs'] * recency_wt).astype('float32')
    bbb_m['rec_bowl_balls'] = (bbb_m['is_legal_ball'] * recency_wt).astype('float32')
    bbb_m['rec_bowl_wkts'] = (bbb_m['is_bowler_wicket'] * recency_wt).astype('float32')

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

# ---------------------------------------------------------
# 2. OPEN SIDEBAR (NO DROPDOWNS — DIRECT CONTROLS)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sb-title">Scouting Controls</div>', unsafe_allow_html=True)

    player_search = st.text_input("Search Player", placeholder="e.g. Shashank, Bosch, Archer")

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

def style_chart(fig, height=370):
    fig.update_layout(
        height=height,
        font=dict(family="Inter, sans-serif", size=12, color="#475569"),
        title_font=dict(family="Plus Jakarta Sans, sans-serif", size=14.5, color="#17316B"),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=24, r=20, t=50, b=28),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=None,
            font=dict(size=11.5, color="#334155")
        ),
        xaxis=dict(
            gridcolor="#F1F5F9",
            zerolinecolor="#CBD5E1",
            tickfont=dict(size=11, color="#475569"),
            title_font=dict(size=12, color="#334155")
        ),
        yaxis=dict(
            gridcolor="#F1F5F9",
            zerolinecolor="#CBD5E1",
            tickfont=dict(size=11, color="#475569"),
            title_font=dict(size=12, color="#334155")
        ),
        hoverlabel=dict(
            bgcolor="#17316B",
            bordercolor="#17316B",
            font=dict(family="Inter, sans-serif", size=12, color="#FFFFFF")
        )
    )
    return fig

# ---------------------------------------------------------
# 3. CLEAN ROYALS HEADER & RESTORED 4 HERO STAT CARDS
# ---------------------------------------------------------
st.markdown(f"""
<div class="rr-banner">
<div class="rr-banner-top">
<span class="rr-team-line">RAJASTHAN ROYALS · PERFORMANCE ANALYSIS</span>
<span class="sample-pill">Sample: {hp_balls:,} / {tot_balls:,} balls ({hp_pct:.1f}% DPI ≥ {dpi_threshold})</span>
</div>
<h1 class="page-title">IPL 2027 Mega-Auction Scouting & Squad Plan</h1>
<div class="squad-strip">
<span>Purse: <strong>₹120.0 Cr</strong></span>
<span>Retentions: <strong>6 Players</strong></span>
<span>Overseas Slots: <strong>2 Retained, 2 Open</strong></span>
<span>Target Roles: <strong>Indian Finisher (#5–6) & Seam All-Rounder</strong></span>
</div>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown("""
<div class="stat-card stat-card-pink">
<div class="stat-top">
<span class="stat-label">RR 2026 Death Batting</span>
<span class="tag-pink">Overs 16–20</span>
</div>
<div class="kpi-number">10.31 <span style="font-size:13px;font-weight:500;color:#64748B;">RPO</span></div>
<div class="stat-note">-0.49 RPO behind league average (10.80)</div>
</div>
""", unsafe_allow_html=True)

with k2:
    st.markdown("""
<div class="stat-card stat-card-blue">
<div class="stat-top">
<span class="stat-label">RR Middle Dot-Ball Rate</span>
<span class="tag-navy">Overs 7–15</span>
</div>
<div class="kpi-number">25.6% <span style="font-size:13px;font-weight:500;color:#64748B;">dots</span></div>
<div class="stat-note">-3.2% behind league average (28.8%)</div>
</div>
""", unsafe_allow_html=True)

with k3:
    st.markdown("""
<div class="stat-card stat-card-pink">
<div class="stat-top">
<span class="stat-label">#1 Finisher Target (IND)</span>
<span class="tag-pink">78.3 BPRS</span>
</div>
<div class="kpi-number">Shashank <span style="font-size:13px;font-weight:500;color:#64748B;">#5–6</span></div>
<div class="stat-note">182.8 Pressure SR · 195.4 Death SR</div>
</div>
""", unsafe_allow_html=True)

with k4:
    st.markdown("""
<div class="stat-card stat-card-blue">
<div class="stat-top">
<span class="stat-label">#1 Seam Target (OS)</span>
<span class="tag-navy">73.0 BWPRS</span>
</div>
<div class="kpi-number">C. Bosch <span style="font-size:13px;font-weight:500;color:#64748B;">SA</span></div>
<div class="stat-note">8.37 Pressure Econ · 49.7% Dot Balls</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. STRUCTURED 5-TAB WORKSPACE
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. 2027 Auction Blueprint & XII",
    "2. RR 2026 Season Audit",
    "3. Batting Leaderboard (BPRS)",
    "4. Bowling Leaderboard (BWPRS)",
    "5. Model & Data Notes"
])

with tab1:
    c_left, c_right = st.columns([1.05, 1])
    with c_left:
        st.markdown('<div class="table-head-bar"><span class="table-head-title">Priority Auction Target Matrix</span><span class="tag-pink">7 Shortlisted Targets</span></div>', unsafe_allow_html=True)
        targets_df = pd.DataFrame([
            {"Tier": "Tier 1", "Player": "Shashank Singh", "Pool": "IND", "2026 Team": "PBKS", "Role": "Finisher (#5–6)", "Pressure Profile": "78.3 BPRS · 195.4 Death SR"},
            {"Tier": "Tier 1", "Player": "Naman Dhir", "Pool": "IND", "2026 Team": "MI", "Role": "Finisher / Off-Spin", "Pressure Profile": "73.7 BPRS · 201.1 Pressure SR"},
            {"Tier": "Tier 1", "Player": "Corbin Bosch", "Pool": "OS (SA)", "2026 Team": "MI", "Role": "Death Seam All-Rounder", "Pressure Profile": "73.0 BWPRS · 8.37 Econ · 49.7% Dots"},
            {"Tier": "Tier 1", "Player": "Mujeeb Ur Rahman", "Pool": "OS (AFG)", "2026 Team": "Free Agent", "Role": "PP & Middle Spin", "Pressure Profile": "69.8 BWPRS · 7.76 Pressure Econ"},
            {"Tier": "Backup", "Player": "Jamie Overton", "Pool": "OS (ENG)", "2026 Team": "CSK", "Role": "Death Pace / Hitter", "Pressure Profile": "67.3 BWPRS · 6.85 Death SR"},
            {"Tier": "Backup", "Player": "Gurjapneet Singh", "Pool": "IND", "2026 Team": "CSK", "Role": "Left-Arm Seam", "Pressure Profile": "64.6 BWPRS · 8.88 Death Econ"},
            {"Tier": "Backup", "Player": "Cooper Connolly", "Pool": "OS (AUS)", "2026 Team": "PBKS", "Role": "LHB Middle / SLA Spin", "Pressure Profile": "67.2 BPRS · 237.8 Death SR"}
        ])
        st.dataframe(targets_df, use_container_width=True, hide_index=True, height=295)

    with c_right:
        st.markdown('<div class="table-head-bar"><span class="table-head-title">Projected IPL 2027 Playing XII</span><span class="tag-navy">4 / 4 Overseas Slots</span></div>', unsafe_allow_html=True)
        xii_df = pd.DataFrame([
            {"#": 1, "Player": "Yashasvi Jaiswal", "Status": "Retained (IND)", "Role & 2026 Output": "LHB Opener · 427 runs @ 152.5 SR"},
            {"#": 2, "Player": "Vaibhav Sooryavanshi", "Status": "Retained (IND)", "Role & 2026 Output": "LHB Opener · 776 runs @ 237.3 SR"},
            {"#": 3, "Player": "Riyan Parag", "Status": "Retained (IND)", "Role & 2026 Output": "RHB Middle / Spin · 309 runs @ 157.7 SR"},
            {"#": 4, "Player": "Dhruv Jurel (WK)", "Status": "Retained (IND)", "Role & 2026 Output": "RHB Keeper · 515 runs @ 154.7 SR"},
            {"#": 5, "Player": "Naman Dhir", "Status": "Target (IND)", "Role & 2026 Output": "RHB Enforcer / Off-Spin · 201.1 Pressure SR"},
            {"#": 6, "Player": "Shashank Singh", "Status": "Target (IND)", "Role & 2026 Output": "RHB Death Finisher · 195.4 Death SR"},
            {"#": 7, "Player": "Donovan Ferreira", "Status": "Retained (OS #1)", "Role & 2026 Output": "RHB Power Hitter · 317 runs @ 179.1 SR"},
            {"#": 8, "Player": "Ravindra Jadeja", "Status": "Retained (IND)", "Role & 2026 Output": "LHB / SLA Spin · 266 runs & 8.58 Econ"},
            {"#": 9, "Player": "Corbin Bosch", "Status": "Target (OS #2)", "Role & 2026 Output": "Death Seam All-Rounder · 8.37 Pressure Econ"},
            {"#": 10, "Player": "Jofra Archer", "Status": "Retained (OS #3)", "Role & 2026 Output": "Pace Spearhead · 25 Wkts @ 9.43 Econ"},
            {"#": 11, "Player": "Ravi Bishnoi", "Status": "Retained (IND)", "Role & 2026 Output": "Leg-Break Spinner · 11 Wkts @ 9.96 Econ"},
            {"#": 12, "Player": "Gurjapneet / Mujeeb", "Status": "Impact Sub (OS #4)", "Role & 2026 Output": "Left-Arm Seam or Mystery Spin Matchup"}
        ])
        st.dataframe(xii_df, use_container_width=True, hide_index=True, height=295)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    upgrade_df = pd.DataFrame([
        {"Slot": "Finishing Battery", "Player": "Shimron Hetmyer (RR 2026)", "Value": 113.0, "Status": "2026 Outgoing"},
        {"Slot": "Finishing Battery", "Player": "Shashank Singh", "Value": 182.8, "Status": "2027 Target"},
        {"Slot": "Finishing Battery", "Player": "Naman Dhir", "Value": 201.1, "Status": "2027 Target"},
        {"Slot": "Support Seam", "Player": "Tushar Deshpande (RR 2026)", "Value": 12.26, "Status": "2026 Outgoing"},
        {"Slot": "Support Seam", "Player": "Corbin Bosch", "Value": 8.37, "Status": "2027 Target"},
        {"Slot": "Support Seam", "Player": "Gurjapneet Singh", "Value": 8.48, "Status": "2027 Target"}
    ])

    u1, u2 = st.columns(2)
    with u1:
        fig_u1 = px.bar(
            upgrade_df[upgrade_df['Slot'] == "Finishing Battery"],
            x='Player', y='Value', color='Status', text='Value',
            color_discrete_map={'2026 Outgoing': '#94A3B8', '2027 Target': '#E51A7A'},
            title="Finishing Upgrade: High-Pressure Strike Rate (Higher is Better)",
            labels={'Value': 'Strike Rate'}
        )
        fig_u1.update_traces(textposition='outside', marker_line_width=0)
        st.plotly_chart(style_chart(fig_u1, 330), use_container_width=True)

    with u2:
        fig_u2 = px.bar(
            upgrade_df[upgrade_df['Slot'] == "Support Seam"],
            x='Player', y='Value', color='Status', text='Value',
            color_discrete_map={'2026 Outgoing': '#94A3B8', '2027 Target': '#17316B'},
            title="Support Seam Upgrade: High-Pressure Economy (Lower is Better)",
            labels={'Value': 'Economy Rate'}
        )
        fig_u2.update_traces(textposition='outside', marker_line_width=0)
        st.plotly_chart(style_chart(fig_u2, 330), use_container_width=True)

with tab2:
    g1, g2 = st.columns(2)
    with g1:
        fig_bat_p = px.bar(
            bat_p, x='phase', y='Run Rate', color='Team', barmode='group', text='Run Rate',
            color_discrete_map={'Rajasthan Royals': '#E51A7A', 'IPL 2026 League Avg': '#94A3B8'},
            title="IPL 2026 Batting Run Rate by Phase vs. League Avg",
            category_orders={'phase': ['Powerplay (1-6)', 'Middle (7-15)', 'Death (16-20)']}
        )
        fig_bat_p.update_traces(textposition='outside', marker_line_width=0)
        st.plotly_chart(style_chart(fig_bat_p, 340), use_container_width=True)

    with g2:
        fig_bowl_p = px.bar(
            bowl_p, x='phase', y='Dot %', color='Bowl_Team', barmode='group', text='Dot %',
            color_discrete_map={'Rajasthan Royals': '#17316B', 'IPL 2026 League Avg': '#94A3B8'},
            title="IPL 2026 Bowling Dot-Ball % by Phase vs. League Avg",
            category_orders={'phase': ['Powerplay (1-6)', 'Middle (7-15)', 'Death (16-20)']}
        )
        fig_bowl_p.update_traces(textposition='outside', marker_line_width=0)
        st.plotly_chart(style_chart(fig_bowl_p, 340), use_container_width=True)

    c_bat, c_bowl = st.columns(2)
    with c_bat:
        st.markdown('<div class="table-head-bar"><span class="table-head-title">RR IPL 2026 Batting Output</span><span class="tag-pink">9W – 7L</span></div>', unsafe_allow_html=True)
        st.dataframe(
            rr_bat26,
            use_container_width=True,
            hide_index=True,
            height=340,
            column_config={
                "SR": st.column_config.NumberColumn("Strike Rate", format="%.1f"),
                "Runs": st.column_config.ProgressColumn("Runs", min_value=0, max_value=int(rr_bat26['Runs'].max()), format="%d"),
                "Balls": st.column_config.NumberColumn("Balls", format="%d")
            }
        )

    with c_bowl:
        st.markdown('<div class="table-head-bar"><span class="table-head-title">RR IPL 2026 Bowling Output</span><span class="tag-navy">9W – 7L</span></div>', unsafe_allow_html=True)
        st.dataframe(
            rr_bowl26,
            use_container_width=True,
            hide_index=True,
            height=340,
            column_config={
                "Econ": st.column_config.NumberColumn("Economy", format="%.2f"),
                "Wkts": st.column_config.ProgressColumn("Wickets", min_value=0, max_value=int(rr_bowl26['Wkts'].max()), format="%d"),
                "Balls": st.column_config.NumberColumn("Balls", format="%d")
            }
        )

with tab3:
    role_choice = st.radio(
        "Filter Batting Position:",
        ["All Qualified Batters", "Finishers & Lower-Middle Order (Avg Pos ≥ 4.5)", "Top-Order Batters (Avg Pos < 4.5)"],
        horizontal=True
    )

    bat_view = bat_qual
    if "Finishers" in role_choice:
        bat_view = bat_view[bat_view['avg_bat_order'] >= 4.5]
    elif "Top-Order" in role_choice:
        bat_view = bat_view[bat_view['avg_bat_order'] < 4.5]

    if player_search.strip():
        bat_view = bat_view[bat_view['player_name'].str.contains(player_search.strip(), case=False, na=False)]

    bat_sorted = bat_view.sort_values('BPRS', ascending=False)

    disp_bat = bat_sorted[[
        'player_name', 'category', 'ipl_2026_team', 'avg_bat_order', 'hp_balls', 'hp_runs',
        'hp_sr', 'hp_rec_sr', 'hp_bpd', 'hp_bnd_pct', 'death_sr', 'chase_sr', 'coll_sr', 'BPRS'
    ]].rename(columns={
        'player_name': 'Player', 'category': 'Pool', 'ipl_2026_team': '2026 Team',
        'avg_bat_order': 'Avg Pos', 'hp_balls': 'Pressure Balls', 'hp_runs': 'Pressure Runs',
        'hp_sr': 'Pressure SR', 'hp_rec_sr': 'Recency SR', 'hp_bpd': 'Balls/Out',
        'hp_bnd_pct': 'Boundary %', 'death_sr': 'Death SR', 'chase_sr': 'Chase SR', 'coll_sr': 'Collapse SR'
    }).round(1)

    st.dataframe(
        disp_bat,
        use_container_width=True,
        hide_index=True,
        height=360,
        column_config={
            "BPRS": st.column_config.ProgressColumn("BPRS (0–100)", min_value=0, max_value=100, format="%.1f"),
            "Pressure SR": st.column_config.NumberColumn("Pressure SR", format="%.1f"),
            "Death SR": st.column_config.NumberColumn("Death SR", format="%.1f"),
            "Balls/Out": st.column_config.NumberColumn("Balls/Out", format="%.1f"),
            "Boundary %": st.column_config.NumberColumn("Boundary %", format="%.1f%%")
        }
    )

    if len(bat_sorted) > 0:
        fig_bat = px.scatter(
            bat_sorted.head(30),
            x='hp_bpd', y='hp_sr', size='hp_balls', color='category',
            hover_name='player_name',
            hover_data={'ipl_2026_team': True, 'BPRS': ':.1f', 'death_sr': ':.1f'},
            text='player_name',
            color_discrete_map={
                'India': '#E51A7A',
                'Overseas (IPL-Eligible)': '#17316B',
                'Pakistan (Ineligible)': '#94A3B8'
            },
            labels={'hp_bpd': 'Wicket Preservation (Balls per Dismissal under Pressure)', 'hp_sr': 'High-Pressure Strike Rate'},
            title="Top 30 Batters: Strike Rate vs. Wicket Preservation (Top-Right = Ideal Finishers)"
        )
        fig_bat.update_traces(textposition='top center', textfont=dict(size=10, color='#334155'), marker=dict(opacity=0.88))
        st.plotly_chart(style_chart(fig_bat, 420), use_container_width=True)

    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("""
<div class="panel-card">
<div class="card-top">
<div><div class="card-name">Shashank Singh</div><div class="card-role">PBKS (2026) · Right-Hand Finisher (#5–6) · India</div></div>
<span class="tag-pink">78.3 BPRS (#1 IND)</span>
</div>
<div class="stat-grid">
<div class="stat-cell"><div class="stat-lbl">Pressure SR</div><div class="stat-val">182.8</div></div>
<div class="stat-cell"><div class="stat-lbl">Death SR</div><div class="stat-val">195.4</div></div>
<div class="stat-cell"><div class="stat-lbl">Balls / Out</div><div class="stat-val">26.2</div></div>
</div>
</div>
""", unsafe_allow_html=True)

    with sc2:
        st.markdown("""
<div class="panel-card">
<div class="card-top">
<div><div class="card-name">Naman Dhir</div><div class="card-role">MI (2026) · RHB / Part-Time Off-Spin (#5) · India</div></div>
<span class="tag-pink">73.7 BPRS (#2 IND)</span>
</div>
<div class="stat-grid">
<div class="stat-cell"><div class="stat-lbl">Pressure SR</div><div class="stat-val">201.1</div></div>
<div class="stat-cell"><div class="stat-lbl">Boundary %</div><div class="stat-val">30.8%</div></div>
<div class="stat-cell"><div class="stat-lbl">Collapse SR</div><div class="stat-val">174.5</div></div>
</div>
</div>
""", unsafe_allow_html=True)

with tab4:
    bowl_type_filter = st.radio("Filter Bowling Discipline:", ["All Bowlers", "Pace / Seam", "Spin"], horizontal=True)

    bowl_view = bowl_qual
    if bowl_type_filter == "Pace / Seam":
        bowl_view = bowl_view[bowl_view['bowling_type'].str.contains('fast|medium', case=False, na=False)]
    elif bowl_type_filter == "Spin":
        bowl_view = bowl_view[~bowl_view['bowling_type'].str.contains('fast|medium', case=False, na=False)]

    if player_search.strip():
        bowl_view = bowl_view[bowl_view['player_name'].str.contains(player_search.strip(), case=False, na=False)]

    bowl_sorted = bowl_view.sort_values('BWPRS', ascending=False)

    disp_bowl = bowl_sorted[[
        'player_name', 'category', 'ipl_2026_team', 'bowling_type', 'hp_balls', 'hp_wkts',
        'hp_econ', 'hp_rec_econ', 'hp_sr', 'hp_dot_pct', 'death_econ', 'death_sr', 'BWPRS'
    ]].rename(columns={
        'player_name': 'Player', 'category': 'Pool', 'ipl_2026_team': '2026 Team',
        'bowling_type': 'Style', 'hp_balls': 'Pressure Balls', 'hp_wkts': 'Pressure Wkts',
        'hp_econ': 'Pressure Econ', 'hp_rec_econ': 'Recency Econ', 'hp_sr': 'Pressure SR',
        'hp_dot_pct': 'Dot %', 'death_econ': 'Death Econ', 'death_sr': 'Death SR'
    }).round(2)

    st.dataframe(
        disp_bowl,
        use_container_width=True,
        hide_index=True,
        height=360,
        column_config={
            "BWPRS": st.column_config.ProgressColumn("BWPRS (0–100)", min_value=0, max_value=100, format="%.1f"),
            "Pressure Econ": st.column_config.NumberColumn("Pressure Econ", format="%.2f"),
            "Death Econ": st.column_config.NumberColumn("Death Econ", format="%.2f"),
            "Dot %": st.column_config.NumberColumn("Dot %", format="%.1f%%")
        }
    )

    if len(bowl_sorted) > 0:
        fig_bowl = px.scatter(
            bowl_sorted.head(30),
            x='hp_econ', y='hp_sr', size='hp_balls', color='category',
            hover_name='player_name',
            hover_data={'ipl_2026_team': True, 'BWPRS': ':.1f', 'death_econ': ':.2f'},
            text='player_name',
            color_discrete_map={
                'India': '#E51A7A',
                'Overseas (IPL-Eligible)': '#17316B',
                'Pakistan (Ineligible)': '#94A3B8'
            },
            labels={'hp_econ': 'High-Pressure Economy (Right = More Economical)', 'hp_sr': 'High-Pressure Strike Rate (Top = Faster Wickets)'},
            title="Top 30 Bowlers: Economy Rate vs. Strike Rate (Top-Right = Elite Enforcers)"
        )
        fig_bowl.update_traces(textposition='top center', textfont=dict(size=10, color='#334155'), marker=dict(opacity=0.88))
        fig_bowl.update_yaxes(autorange="reversed")
        fig_bowl.update_xaxes(autorange="reversed")
        st.plotly_chart(style_chart(fig_bowl, 420), use_container_width=True)

    bd1, bd2 = st.columns(2)
    with bd1:
        st.markdown("""
<div class="panel-card">
<div class="card-top">
<div><div class="card-name">Corbin Bosch</div><div class="card-role">MI (2026) · Right-Arm Fast-Medium All-Rounder · South Africa</div></div>
<span class="tag-navy">73.0 BWPRS (#2 Pace)</span>
</div>
<div class="stat-grid">
<div class="stat-cell"><div class="stat-lbl">Pressure Econ</div><div class="stat-val">8.37</div></div>
<div class="stat-cell"><div class="stat-lbl">Dot Ball %</div><div class="stat-val">49.7%</div></div>
<div class="stat-cell"><div class="stat-lbl">Death Econ</div><div class="stat-val">9.12</div></div>
</div>
</div>
""", unsafe_allow_html=True)

    with bd2:
        st.markdown("""
<div class="panel-card">
<div class="card-top">
<div><div class="card-name">Mujeeb Ur Rahman</div><div class="card-role">Free Agent (2026) · Powerplay & Middle Off-Spin · Afghanistan</div></div>
<span class="tag-navy">69.8 BWPRS (#1 Spin)</span>
</div>
<div class="stat-grid">
<div class="stat-cell"><div class="stat-lbl">Pressure Econ</div><div class="stat-val">7.76</div></div>
<div class="stat-cell"><div class="stat-lbl">Bowling SR</div><div class="stat-val">16.8</div></div>
<div class="stat-cell"><div class="stat-lbl">Dot Ball %</div><div class="stat-val">42.4%</div></div>
</div>
</div>
""", unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="table-head-bar"><span class="table-head-title">Delivery Pressure Index (DPI) Scoring Formulation</span><span class="tag-navy">0 – 100 Scale</span></div>', unsafe_allow_html=True)
    st.caption("Each delivery (200,999 total across 867 T20 matches) receives an additive 0–100 pressure score. Deliveries above the threshold feed into recency-weighted BPRS and BWPRS rankings.")

    m1, m2 = st.columns([1, 1.1])
    with m1:
        dpi_rules = pd.DataFrame([
            {"Leverage Trigger": "Death Overs", "Points": "+30", "Match Condition": "Overs 16.1 through 20.0 in either innings"},
            {"Leverage Trigger": "Steep Run Chase", "Points": "+30", "Match Condition": "2nd inn RRR ≥ 10.5 or (Overs ≥ 15 & 8.5 ≤ RRR ≤ 18.0)"},
            {"Leverage Trigger": "Collapse Mitigation", "Points": "+25", "Match Condition": "≥ 2 wkts in PP, ≥ 3 by Over 10, or ≥ 5 wkts down"},
            {"Leverage Trigger": "Knockout Stakes", "Points": "+20", "Match Condition": "Finals, Qualifiers, Eliminators, Semi-Finals, Super 4"},
            {"Leverage Trigger": "Bowling Under Siege", "Points": "+15", "Match Condition": "Overs 7–20 after conceding ≥ 60 runs in Powerplay"}
        ])
        st.dataframe(dpi_rules, use_container_width=True, hide_index=True, height=230)

    with m2:
        fig_dpi = px.bar(
            dpi_dist, x='dpi', y='Deliveries', color='Regime',
            color_discrete_map={f'High Pressure (DPI ≥ {dpi_threshold})': '#E51A7A', 'Standard Leverage': '#CBD5E1'},
            labels={'dpi': 'DPI Score (0–100)', 'Deliveries': 'Deliveries'},
            title="Delivery Count by DPI Pressure Score"
        )
        fig_dpi.update_traces(marker_line_width=0)
        st.plotly_chart(style_chart(fig_dpi, 250), use_container_width=True)

    with st.expander("View Source Tables & Relational Join Keys (6 Source Datasets)"):
        ref_df = pd.DataFrame([
            {"Table": "ball_by_ball.csv", "Rows": "200,999", "Keys": "match_id, striker_id, bowler_id", "Role": "Delivery runs, extras, dismissals, phase, bowling type"},
            {"Table": "matches.csv", "Rows": "883", "Keys": "match_id, comp_id, win_team_id", "Role": "Match stages, knockout flags, DLS target revisions"},
            {"Table": "competitions.csv", "Rows": "141", "Keys": "comp_id", "Role": "Seasons (2022–2026) and tournament format mapping"},
            {"Table": "playing_eleven.csv", "Rows": "28,381", "Keys": "match_id, team_id, player_id", "Role": "Batting order positions and Impact Sub appearances"},
            {"Table": "competition_team_player_mapping.csv", "Rows": "6,413", "Keys": "comp_id, team_id, player_id", "Role": "Franchise rosters and player eligibility classification"},
            {"Table": "teams.csv", "Rows": "353", "Keys": "comp_id, team_id", "Role": "Team identifiers"}
        ])
        st.dataframe(ref_df, use_container_width=True, hide_index=True)
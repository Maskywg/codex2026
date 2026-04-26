"""
自動更新 codex2026 戰力分析資料
- 從 ESPN 抓最新系列賽戰績
- 從 ESPN 抓最新傷兵報告
- 更新 data/playoffs-data.js
"""
import json
import re
import requests
from datetime import datetime, timedelta, timezone

# ── 設定 ─────────────────────────────────────────────
TAIPEI = timezone(timedelta(hours=8))
NOW = datetime.now(TAIPEI)

# ── ESPN 隊名對照（英文 → 中文顯示名）────────────────
TEAM_ZH = {
    "Boston Celtics":           "Celtics",
    "Brooklyn Nets":            "Nets",
    "New York Knicks":          "Knicks",
    "Philadelphia 76ers":       "76ers",
    "Toronto Raptors":          "Raptors",
    "Chicago Bulls":            "Bulls",
    "Cleveland Cavaliers":      "Cavaliers",
    "Detroit Pistons":          "Pistons",
    "Indiana Pacers":           "Pacers",
    "Milwaukee Bucks":          "Bucks",
    "Atlanta Hawks":            "Hawks",
    "Charlotte Hornets":        "Hornets",
    "Miami Heat":               "Heat",
    "Orlando Magic":            "Magic",
    "Washington Wizards":       "Wizards",
    "Denver Nuggets":           "Nuggets",
    "Minnesota Timberwolves":   "Timberwolves",
    "Oklahoma City Thunder":    "Thunder",
    "Portland Trail Blazers":   "Trail Blazers",
    "Utah Jazz":                "Jazz",
    "Golden State Warriors":    "Warriors",
    "LA Clippers":              "Clippers",
    "Los Angeles Lakers":       "Lakers",
    "Phoenix Suns":             "Suns",
    "Sacramento Kings":         "Kings",
    "Dallas Mavericks":         "Mavericks",
    "Houston Rockets":          "Rockets",
    "Memphis Grizzlies":        "Grizzlies",
    "New Orleans Pelicans":     "Pelicans",
    "San Antonio Spurs":        "Spurs",
}

# ── 傷兵狀態對照 ─────────────────────────────────────
STATUS_MAP = {
    "Out":          "Out",
    "Doubtful":     "Doubtful",
    "Questionable": "Questionable",
    "Probable":     "Probable",
    "Day-To-Day":   "Day-To-Day",
}

# ── 重要球員（只顯示這些人的傷兵資訊）────────────────
KEY_PLAYERS = {
    "Jayson Tatum", "Jaylen Brown", "Derrick White",
    "Shai Gilgeous-Alexander", "Jalen Williams",
    "Anthony Davis", "LeBron James", "Luka Doncic", "Austin Reaves",
    "Anthony Edwards", "Donte DiVincenzo", "Karl-Anthony Towns",
    "Nikola Jokic", "Jamal Murray", "Aaron Gordon",
    "Joel Embiid", "Tyrese Maxey",
    "Immanuel Quickley", "Scottie Barnes",
    "Evan Mobley", "Donovan Mitchell", "Darius Garland",
    "Victor Wembanyama", "Devin Vassell",
    "Damian Lillard", "Jerami Grant",
    "Alperen Sengun", "Fred VanVleet", "Kevin Durant",
    "Grayson Allen", "Bradley Beal",
}

def fetch_series():
    """抓最近 10 天的季後賽場次，取得各系列賽戰績"""
    series_map = {}  # key: frozenset(abbr1, abbr2) → summary
    for offset in range(10):
        d = NOW - timedelta(days=offset)
        date_str = d.strftime("%Y%m%d")
        url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?seasontype=3&dates={date_str}"
        try:
            r = requests.get(url, timeout=10)
            events = r.json().get("events", [])
            for event in events:
                comp = event["competitions"][0]
                series = comp.get("series", {})
                summary = series.get("summary", "")
                if not summary:
                    continue
                teams = comp["competitors"]
                abbrs = frozenset(t["team"]["abbreviation"] for t in teams)
                names = {t["team"]["abbreviation"]: t["team"]["displayName"] for t in teams}
                if abbrs not in series_map:
                    series_map[abbrs] = {
                        "summary": summary,
                        "names": names,
                    }
        except Exception as e:
            print(f"  ⚠️  日期 {date_str} 抓取失敗: {e}")
    return series_map

def fetch_injuries():
    """抓各隊傷兵報告，只保留重要球員"""
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/injuries"
    injury_by_team = {}
    try:
        r = requests.get(url, timeout=10)
        items = r.json().get("items", [])
        for item in items:
            team_name = item.get("team", {}).get("displayName", "")
            team_short = TEAM_ZH.get(team_name, team_name.split()[-1])
            injuries = item.get("injuries", [])
            notable = []
            for inj in injuries:
                player = inj.get("athlete", {}).get("displayName", "")
                status = inj.get("status", "")
                if player in KEY_PLAYERS and status in STATUS_MAP:
                    notable.append(f"{player} ({status})")
            if notable:
                injury_by_team[team_short] = notable
    except Exception as e:
        print(f"  ⚠️  傷兵 API 失敗: {e}")
    return injury_by_team

def summary_to_leader(summary: str, names: dict = None) -> str:
    """'OKC leads series 3-0' → 'Oklahoma City 3-0'"""
    if "tied" in summary.lower():
        m = re.search(r"(\d+-\d+)", summary)
        return f"平手 {m.group(1)}" if m else summary
    m = re.match(r"(\S+)\s+leads?\s+series\s+(\d+-\d+)", summary, re.I)
    if m:
        abbr = m.group(1)
        score = m.group(2)
        # 用完整隊名取代縮寫
        full_name = abbr
        if names:
            full_name = names.get(abbr, abbr)
            # 取最後一個字（如 "Los Angeles Lakers" → "Lakers"）
            full_name = full_name.split()[-1] if len(full_name.split()) > 1 else full_name
        return f"{full_name} {score}"
    return summary

def build_injury_groups(injury_by_team: dict) -> list:
    """把傷兵資料組合成 codex 格式的 injuries 陣列"""
    # 已知季後賽對戰配對（可擴充）
    MATCHUPS = [
        ("Timberwolves", "Nuggets"),
        ("Lakers", "Rockets"),
        ("Thunder", "Suns"),
        ("Spurs", "Trail Blazers"),
        ("Celtics", "76ers"),
        ("Cavaliers", "Raptors"),
        ("Knicks", "Hawks"),
        ("Magic", "Pistons"),
    ]

    # 傷兵嚴重程度排序
    SEVERITY = {"Out": 0, "Doubtful": 1, "Questionable": 2, "Day-To-Day": 3, "Probable": 4}

    groups = []
    covered = set()
    for team_a, team_b in MATCHUPS:
        inj_a = injury_by_team.get(team_a, [])
        inj_b = injury_by_team.get(team_b, [])
        all_inj = inj_a + inj_b
        if not all_inj:
            continue
        # 計算健康折扣（Out=8, Doubtful=5, Questionable=2）
        discount = 0
        for inj in all_inj:
            if "Out" in inj:       discount += 8
            elif "Doubtful" in inj: discount += 5
            elif "Questionable" in inj: discount += 2

        team_label = f"{team_a} / {team_b}" if inj_a and inj_b else (team_a if inj_a else team_b)
        detail = "、".join(all_inj)

        # 特殊標記重大傷情
        has_major = any("Out" in i for i in all_inj)
        tag = "⚠️ 重大傷情" if has_major else "核心缺陣"

        groups.append({
            "team": team_label,
            "tag": tag,
            "detail": detail,
            "impact": f"健康折扣 {discount:.1f} 分",
        })
        covered.update([team_a, team_b])

    return sorted(groups, key=lambda x: -float(x["impact"].split()[1]))

def update_js(series_map: dict, injury_groups: list):
    """讀取現有 playoffs-data.js，更新 series leader 和 injuries，寫回"""
    js_path = "data/playoffs-data.js"
    with open(js_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 解析現有資料
    match = re.search(r"window\.PLAYOFFS_DATA\s*=\s*(\{.*\})\s*;", content, re.S)
    if not match:
        print("❌ 找不到 PLAYOFFS_DATA")
        return
    data = json.loads(match.group(1))

    # 更新 series leader
    updated_series = 0
    for conf in ["east", "west"]:
        for item in data["series"][conf]:
            matchup = item["matchup"]  # e.g. "(1) Detroit vs (8) Orlando"
            # 找出兩隊縮寫
            for abbrs, info in series_map.items():
                names = info["names"]
                # 比對隊名是否出現在 matchup 字串中
                matched = sum(
                    1 for full_name in names.values()
                    if any(part in matchup for part in full_name.split()[-2:])
                )
                if matched >= 2:
                    new_leader = summary_to_leader(info["summary"], names)
                    if item["leader"] != new_leader:
                        print(f"  ✅ 更新 {matchup}: {item['leader']} → {new_leader}")
                        item["leader"] = new_leader
                        updated_series += 1
                    break

    # 更新 injuries（保留手動加的特殊項目，合併 ESPN 資料）
    if injury_groups:
        data["injuries"] = injury_groups
        print(f"  ✅ 更新傷兵報告：{len(injury_groups)} 組")
    else:
        print("  ⚠️  ESPN 傷兵資料為空，保留原有資料")

    # 更新時間戳
    data["generatedAt"] = NOW.strftime("%Y-%m-%dT%H:%M:%S")
    data["scheduleDate"] = NOW.strftime("%B %d, %Y")

    # 寫回 JS
    new_content = f"window.PLAYOFFS_DATA = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  ✅ 寫入完成 (系列賽更新 {updated_series} 筆)")

def main():
    print(f"🏀 開始更新 codex2026（台灣時間 {NOW.strftime('%Y-%m-%d %H:%M')}）")

    print("📡 抓取系列賽戰績...")
    series_map = fetch_series()
    print(f"   找到 {len(series_map)} 組系列賽")

    print("🚑 抓取傷兵報告...")
    injury_by_team = fetch_injuries()
    injury_groups = build_injury_groups(injury_by_team)
    print(f"   找到 {len(injury_groups)} 組傷兵資料")

    print("💾 更新 data/playoffs-data.js...")
    update_js(series_map, injury_groups)

    print("✅ 完成！")

if __name__ == "__main__":
    main()

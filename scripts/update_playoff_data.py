#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from html import unescape
from io import BytesIO
from pathlib import Path
from typing import Dict, List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "playoffs-data.js"
SCHEDULE_URL = "https://www.nba.com/news/2026-nba-playoffs-schedule"

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
TEAM_NAMES = [
    "Oklahoma City Thunder",
    "Phoenix Suns",
    "San Antonio Spurs",
    "Portland Trail Blazers",
    "Denver Nuggets",
    "Minnesota Timberwolves",
    "Los Angeles Lakers",
    "Houston Rockets",
    "Detroit Pistons",
    "Orlando Magic",
    "Boston Celtics",
    "Philadelphia 76ers",
    "New York Knicks",
    "Atlanta Hawks",
    "Cleveland Cavaliers",
    "Toronto Raptors",
]
CITY_TO_TEAM = {
    "Detroit": "Detroit Pistons",
    "Orlando": "Orlando Magic",
    "Boston": "Boston Celtics",
    "Philadelphia": "Philadelphia 76ers",
    "New York": "New York Knicks",
    "Atlanta": "Atlanta Hawks",
    "Cleveland": "Cleveland Cavaliers",
    "Toronto": "Toronto Raptors",
    "Oklahoma City": "Oklahoma City Thunder",
    "Phoenix": "Phoenix Suns",
    "San Antonio": "San Antonio Spurs",
    "Portland": "Portland Trail Blazers",
    "Denver": "Denver Nuggets",
    "Minnesota": "Minnesota Timberwolves",
    "Los Angeles": "Los Angeles Lakers",
    "Houston": "Houston Rockets",
}
TEAM_TO_CITY = {value: key for key, value in CITY_TO_TEAM.items()}
TEAM_TO_SHORT = {
    "Detroit Pistons": "Pistons",
    "Orlando Magic": "Magic",
    "Boston Celtics": "Celtics",
    "Philadelphia 76ers": "76ers",
    "New York Knicks": "Knicks",
    "Atlanta Hawks": "Hawks",
    "Cleveland Cavaliers": "Cavaliers",
    "Toronto Raptors": "Raptors",
    "Oklahoma City Thunder": "Thunder",
    "Phoenix Suns": "Suns",
    "San Antonio Spurs": "Spurs",
    "Portland Trail Blazers": "Trail Blazers",
    "Denver Nuggets": "Nuggets",
    "Minnesota Timberwolves": "Timberwolves",
    "Los Angeles Lakers": "Lakers",
    "Houston Rockets": "Rockets",
}
BASE_RATINGS = {
    "Oklahoma City Thunder": 91,
    "Los Angeles Lakers": 89,
    "Boston Celtics": 88,
    "Minnesota Timberwolves": 87,
    "Cleveland Cavaliers": 84,
    "San Antonio Spurs": 83,
    "Denver Nuggets": 82,
    "New York Knicks": 80,
    "Atlanta Hawks": 79,
    "Toronto Raptors": 78,
    "Orlando Magic": 78,
    "Detroit Pistons": 77,
    "Houston Rockets": 77,
    "Philadelphia 76ers": 76,
    "Phoenix Suns": 75,
    "Portland Trail Blazers": 74,
}
CORE_PLAYERS = {
    "Oklahoma City Thunder": {"Shai Gilgeous-Alexander", "Jalen Williams", "Chet Holmgren"},
    "Phoenix Suns": {"Devin Booker", "Bradley Beal", "Mark Williams", "Grayson Allen"},
    "San Antonio Spurs": {"Victor Wembanyama", "De'Aaron Fox", "Stephon Castle"},
    "Portland Trail Blazers": {"Damian Lillard", "Scoot Henderson", "Jerami Grant"},
    "Denver Nuggets": {"Nikola Jokic", "Jamal Murray", "Aaron Gordon"},
    "Minnesota Timberwolves": {"Anthony Edwards", "Rudy Gobert", "Jaden McDaniels"},
    "Los Angeles Lakers": {"LeBron James", "Anthony Davis", "Luka Doncic", "Austin Reaves"},
    "Houston Rockets": {"Kevin Durant", "Alperen Sengun", "Fred VanVleet"},
    "Detroit Pistons": {"Cade Cunningham", "Jalen Duren"},
    "Orlando Magic": {"Paolo Banchero", "Franz Wagner", "Jalen Suggs", "Jonathan Isaac"},
    "Boston Celtics": {"Jayson Tatum", "Jaylen Brown", "Kristaps Porzingis"},
    "Philadelphia 76ers": {"Joel Embiid", "Tyrese Maxey", "Paul George"},
    "New York Knicks": {"Jalen Brunson", "Karl-Anthony Towns", "OG Anunoby"},
    "Atlanta Hawks": {"Trae Young", "Jalen Johnson", "Onyeka Okongwu"},
    "Cleveland Cavaliers": {"Donovan Mitchell", "Darius Garland", "Evan Mobley"},
    "Toronto Raptors": {"Scottie Barnes", "Immanuel Quickley", "RJ Barrett"},
}
STATUS_PENALTY = {
    "Out": 6.0,
    "Doubtful": 4.0,
    "Questionable": 2.5,
    "Probable": 0.8,
    "Available": 0.0,
}
SECONDARY_SCALE = 0.35
PDF_TIMES = [
    f"{hour:02d}_{minute:02d}{meridiem}"
    for meridiem in ("PM", "AM")
    for hour in (range(12, 0, -1) if meridiem == "PM" else range(11, -1, -1))
    for minute in (45, 30, 15, 0)
]


@dataclass
class Series:
    conference: str
    high_seed: int
    high_team: str
    low_seed: int
    low_team: str
    leader_text: str
    high_wins: int
    low_wins: int
    games_text: List[str]


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return response.read()


def fetch_text(url: str) -> str:
    return fetch_bytes(url).decode("utf-8", "ignore")


def normalize_html_text(html: str) -> str:
    text = unescape(re.sub(r"<[^>]+>", " ", html))
    return re.sub(r"\s+", " ", text)


def normalize_pdf_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\x00", " ")).strip()


def latest_schedule_text() -> str:
    html = fetch_text(SCHEDULE_URL)
    return normalize_html_text(html)


def parse_schedule_date(text: str) -> str:
    match = re.search(r"Updated on ([A-Za-z]+ \d{1,2}, \d{4})", text)
    return match.group(1) if match else date.today().isoformat()


def parse_serieses(text: str) -> List[Series]:
    eastern_match = re.search(r"Eastern Conference (.*?) Western Conference", text)
    western_match = re.search(r"Western Conference (.*?) \* = If necessary", text)
    if not eastern_match or not western_match:
        raise RuntimeError("Unable to parse playoff series from schedule page.")

    pattern = re.compile(
        r"\((\d)\)\s+([A-Za-z ]+?)\s+vs\.\s+\((\d)\)\s+([A-Za-z ]+?)\s+(.*?)(Series tied \d-\d|[A-Za-z ]+ lead series \d-\d)",
        re.S,
    )

    serieses: List[Series] = []
    for conference, block in (("east", eastern_match.group(1)), ("west", western_match.group(1))):
        for seed1, city1, seed2, city2, body, leader in pattern.findall(block):
            high_team = CITY_TO_TEAM[city1.strip()]
            low_team = CITY_TO_TEAM[city2.strip()]
            games_text = [
                game.strip()
                for game in re.findall(r"Game \d+:[^G]+?(?=Game \d+:|$)", body)
                if "|" not in game
            ]
            if leader.startswith("Series tied"):
                high_wins, low_wins = map(int, re.search(r"(\d)-(\d)", leader).groups())
            else:
                leader_name, wins, losses = re.search(r"(.+?) lead series (\d)-(\d)", leader).groups()
                wins = int(wins)
                losses = int(losses)
                if TEAM_TO_SHORT[high_team] == leader_name.strip():
                    high_wins, low_wins = wins, losses
                else:
                    high_wins, low_wins = losses, wins

            serieses.append(
                Series(
                    conference=conference,
                    high_seed=int(seed1),
                    high_team=high_team,
                    low_seed=int(seed2),
                    low_team=low_team,
                    leader_text=leader.strip(),
                    high_wins=high_wins,
                    low_wins=low_wins,
                    games_text=games_text,
                )
            )
    return serieses


def find_latest_pdf_for_day(target_day: date) -> str | None:
    day_text = target_day.strftime("%Y-%m-%d")
    for suffix in PDF_TIMES:
        url = f"https://ak-static.cms.nba.com/referee/injury/Injury-Report_{day_text}_{suffix}.pdf"
        request = Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
        try:
            with urlopen(request, timeout=8) as response:
                if response.status == 200:
                    return url
        except (HTTPError, URLError):
            continue
    return None


def extract_injury_rows(pdf_text: str, playoff_teams: set[str]) -> Dict[str, Dict[str, Dict[str, str]]]:
    normalized = normalize_pdf_text(pdf_text)
    team_pattern = "|".join(re.escape(name) for name in sorted(playoff_teams, key=len, reverse=True))
    parts = re.split(f"({team_pattern})", normalized)
    rows: Dict[str, Dict[str, Dict[str, str]]] = {}

    for index in range(1, len(parts), 2):
        team = parts[index]
        block = parts[index + 1]
        next_stop = re.search(r"(?:\d{2}/\d{2}/\d{4}|\d{1,2}:\d{2} \(ET\)|Page \d+ of \d+|Injury Report:)", block)
        if next_stop:
            block = block[: next_stop.start()]
        player_pattern = re.compile(
            r"([A-Za-z'\.\-]+,\s+[A-Za-z'\.\- ]+?)\s+(Out|Doubtful|Questionable|Probable|Available)\s+(.*?)(?=(?:[A-Za-z'\.\-]+,\s+[A-Za-z])|$)"
        )
        for player, status, reason in player_pattern.findall(block):
            clean_name = normalize_player_name(player)
            rows.setdefault(team, {})[clean_name] = {
                "status": status,
                "reason": reason.strip(),
            }
    return rows


def normalize_player_name(player: str) -> str:
    last, first = [part.strip() for part in player.split(",", 1)]
    return f"{first} {last}"


def collect_injuries(playoff_teams: set[str]) -> tuple[Dict[str, Dict[str, Dict[str, str]]], List[str]]:
    collected: Dict[str, Dict[str, Dict[str, str]]] = {team: {} for team in playoff_teams}
    sources: List[str] = []
    found_teams: set[str] = set()

    for offset in range(4):
        target_day = date.today() - timedelta(days=offset)
        pdf_url = find_latest_pdf_for_day(target_day)
        if not pdf_url:
            continue
        sources.append(pdf_url)
        pdf_bytes = fetch_bytes(pdf_url)
        text = "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(pdf_bytes)).pages)
        rows = extract_injury_rows(text, playoff_teams)
        for team, players in rows.items():
            if not players:
                continue
            found_teams.add(team)
            for player_name, info in players.items():
                collected[team].setdefault(player_name, info)
        if found_teams == playoff_teams:
            break

    return collected, sources


def build_team_scores(serieses: List[Series], injuries: Dict[str, Dict[str, Dict[str, str]]]) -> Dict[str, Dict[str, object]]:
    team_data: Dict[str, Dict[str, object]] = {}
    series_lookup: Dict[str, Series] = {}
    for series in serieses:
        series_lookup[series.high_team] = series
        series_lookup[series.low_team] = series

    for team, base in BASE_RATINGS.items():
        if team not in series_lookup:
            continue
        series = series_lookup[team]
        wins = series.high_wins if team == series.high_team else series.low_wins
        losses = series.low_wins if team == series.high_team else series.high_wins
        margin = wins - losses
        series_bonus = wins * 1.8 - losses * 0.7 + max(margin, 0) * 1.2

        injury_items = []
        penalty = 0.0
        for player_name, info in injuries.get(team, {}).items():
            status = info["status"]
            if status == "Available":
                continue
            is_core = player_name in CORE_PLAYERS.get(team, set())
            weight = 1.0 if is_core else SECONDARY_SCALE
            impact = STATUS_PENALTY.get(status, 0.0) * weight
            if impact <= 0:
                continue
            penalty += impact
            injury_items.append(
                {
                    "player": player_name,
                    "status": status,
                    "reason": info["reason"],
                    "core": is_core,
                    "impact": round(impact, 1),
                }
            )

        score = round(base + series_bonus - penalty, 1)
        team_data[team] = {
            "team": team,
            "score": score,
            "wins": wins,
            "losses": losses,
            "series_margin": margin,
            "injuryPenalty": round(penalty, 1),
            "injuries": sorted(injury_items, key=lambda item: (-item["core"], -item["impact"], item["player"])),
        }
    return team_data


def build_tiers(team_scores: Dict[str, Dict[str, object]]) -> List[Dict[str, object]]:
    ordered = sorted(team_scores.values(), key=lambda item: item["score"], reverse=True)[:8]
    groups = [ordered[0:2], ordered[2:4], ordered[4:6], ordered[6:8]]
    titles = [
        ("Tier 1", "爭冠第一梯", "系列賽控制力與健康狀態都仍在高位。"),
        ("Tier 2", "穩定晉級梯", "具備深輪次實力，但傷兵或對位開始壓縮上限。"),
        ("Tier 3", "對位波動梯", "內容不差，但健康與節奏穩定度讓每場起伏偏大。"),
        ("Tier 4", "危險邊緣梯", "沒有足夠緩衝，任何核心傷停都會快速放大。"),
    ]
    tiers = []
    for (label, title, note), group in zip(titles, groups):
        teams = [{"name": TEAM_TO_SHORT[item["team"]], "score": round(item["score"])} for item in group]
        tiers.append({"label": label, "title": title, "note": note, "teams": teams})
    return tiers


def matchup_label(series: Series) -> str:
    return f"({series.high_seed}) {TEAM_TO_CITY[series.high_team]} vs ({series.low_seed}) {TEAM_TO_CITY[series.low_team]}"


def format_leader(series: Series) -> str:
    if series.high_wins == series.low_wins:
        return f"{series.high_wins}-{series.low_wins} 平手"
    leader_team = series.high_team if series.high_wins > series.low_wins else series.low_team
    wins = max(series.high_wins, series.low_wins)
    losses = min(series.high_wins, series.low_wins)
    return f"{TEAM_TO_CITY[leader_team]} {wins}-{losses}"


def build_series_angle(series: Series, team_scores: Dict[str, Dict[str, object]]) -> str:
    high = team_scores[series.high_team]
    low = team_scores[series.low_team]
    margin = abs(series.high_wins - series.low_wins)
    if series.high_wins == series.low_wins:
        base = "目前仍是五五波對撞，雙方都還沒把節奏完全鎖進自己手裡。"
    elif margin >= 3:
        leader = series.high_team if series.high_wins > series.low_wins else series.low_team
        base = f"{TEAM_TO_SHORT[leader]} 已把系列賽推進到接近收官的位置，控制權相當明顯。"
    elif (series.low_wins > series.high_wins and series.low_seed - series.high_seed >= 2):
        base = "低種子一方已經把對位壓力翻轉成實質優勢，下剋上風險非常真實。"
    else:
        base = "目前優勢方有些微主導權，但系列賽還沒有完全脫離反撲區。"

    health_notes = []
    for team in (series.high_team, series.low_team):
        injuries = team_scores[team]["injuries"]
        core_notes = [item for item in injuries if item["core"]][:2]
        if core_notes:
            statuses = "、".join(f"{item['player']} {item['status']}" for item in core_notes)
            health_notes.append(f"{TEAM_TO_SHORT[team]} 端有 {statuses}")

    if health_notes:
        return f"{base} 傷兵面則要留意 {'；'.join(health_notes)}。"
    return base


def build_series_cards(serieses: List[Series], team_scores: Dict[str, Dict[str, object]]) -> Dict[str, List[Dict[str, object]]]:
    cards = {"east": [], "west": []}
    for series in serieses:
        power = round(max(team_scores[series.high_team]["score"], team_scores[series.low_team]["score"]))
        cards[series.conference].append(
            {
                "matchup": matchup_label(series),
                "leader": format_leader(series),
                "angle": build_series_angle(series, team_scores),
                "power": power,
            }
        )
    return cards


def build_injury_watch(serieses: List[Series], team_scores: Dict[str, Dict[str, object]]) -> List[Dict[str, str]]:
    watch = []
    for series in serieses:
        combined = []
        penalty = 0.0
        for team in (series.high_team, series.low_team):
            data = team_scores[team]
            penalty += data["injuryPenalty"]
            combined.extend(
                f"{item['player']} ({item['status']})"
                for item in data["injuries"]
                if item["core"]
            )
        if not combined and penalty < 4:
            continue
        watch.append(
            {
                "team": f"{TEAM_TO_SHORT[series.high_team]} / {TEAM_TO_SHORT[series.low_team]}",
                "tag": "核心缺陣" if combined else "輪替警戒",
                "detail": "、".join(combined[:4]) if combined else "主要是角色球員傷停，會壓縮輪替彈性。",
                "impact": f"健康折扣 {round(penalty, 1)} 分",
                "penalty": penalty,
            }
        )
    ordered = sorted(watch, key=lambda item: item["penalty"], reverse=True)[:3]
    return [{k: v for k, v in item.items() if k != "penalty"} for item in ordered]


def build_highlights(serieses: List[Series], team_scores: Dict[str, Dict[str, object]]) -> List[Dict[str, str]]:
    east = [series for series in serieses if series.conference == "east"]
    west = [series for series in serieses if series.conference == "west"]
    east_tight = min(east, key=lambda item: abs(item.high_wins - item.low_wins))
    west_closeout = max(west, key=lambda item: abs(item.high_wins - item.low_wins))
    upset_candidates = [
        item
        for item in serieses
        if item.low_wins > item.high_wins or (item.low_wins == item.high_wins and item.low_seed - item.high_seed >= 2)
    ]
    upset = upset_candidates[0] if upset_candidates else max(serieses, key=lambda item: item.low_seed - item.high_seed)

    def summary(series: Series) -> str:
        high_short = TEAM_TO_SHORT[series.high_team]
        low_short = TEAM_TO_SHORT[series.low_team]
        return f"{high_short} {series.high_wins}-{series.low_wins} {low_short}" if series.high_wins >= series.low_wins else f"{low_short} {series.low_wins}-{series.high_wins} {high_short}"

    return [
        {
            "label": "東區最膠著",
            "title": f"{TEAM_TO_SHORT[east_tight.high_team]} vs {TEAM_TO_SHORT[east_tight.low_team]}",
            "text": f"{summary(east_tight)}，暫時還沒有哪一邊真正把對位做成單向。"
        },
        {
            "label": "西區最接近收官",
            "title": f"{TEAM_TO_SHORT[west_closeout.high_team]} vs {TEAM_TO_SHORT[west_closeout.low_team]}",
            "text": f"{summary(west_closeout)}，比分已經把壓力大幅推向落後方。"
        },
        {
            "label": "最危險下剋上",
            "title": f"{TEAM_TO_SHORT[upset.high_team]} vs {TEAM_TO_SHORT[upset.low_team]}",
            "text": f"{summary(upset)}，種子序與場上主導權正在出現錯位。"
        },
    ]


def build_analyses(team_scores: Dict[str, Dict[str, object]]) -> List[Dict[str, str]]:
    most_hurt = max(team_scores.values(), key=lambda item: item["injuryPenalty"])
    hottest = max(team_scores.values(), key=lambda item: item["score"])
    biggest_swing = max(team_scores.values(), key=lambda item: item["series_margin"])
    return [
        {
            "eyebrow": "Health Weight",
            "title": "關鍵觀察 01",
            "text": f"{TEAM_TO_SHORT[most_hurt['team']]} 目前吃到最大的健康折扣，代表看比分時必須同時把核心可用性算進去。"
        },
        {
            "eyebrow": "Control Signal",
            "title": "關鍵觀察 02",
            "text": f"{TEAM_TO_SHORT[hottest['team']]} 目前仍是綜合分數最高的隊伍，代表系列賽控制力與健康狀態同時在線。"
        },
        {
            "eyebrow": "Series Swing",
            "title": "關鍵觀察 03",
            "text": f"{TEAM_TO_SHORT[biggest_swing['team']]} 已經把系列賽差距拉開，這種主導權通常比單場手感更能預測下一步走向。"
        },
    ]


def build_featured(team_scores: Dict[str, Dict[str, object]], tiers: List[Dict[str, object]]) -> Dict[str, str]:
    top = max(team_scores.values(), key=lambda item: item["score"])
    tier_name = next(
        tier["title"]
        for tier in tiers
        if any(team["name"] == TEAM_TO_SHORT[top["team"]] for team in tier["teams"])
    )
    return {
        "team": top["team"],
        "record": f"{top['wins']}-{top['losses']}",
        "score": f"{round(top['score'])} / 100",
        "tier": tier_name,
        "summary": f"{TEAM_TO_SHORT[top['team']]} 目前綜合分數最高，系列賽內容與健康狀態都還保有足夠緩衝。",
    }


def build_payload() -> Dict[str, object]:
    schedule_text = latest_schedule_text()
    serieses = parse_serieses(schedule_text)
    playoff_teams = {series.high_team for series in serieses} | {series.low_team for series in serieses}
    injuries, injury_sources = collect_injuries(playoff_teams)
    team_scores = build_team_scores(serieses, injuries)
    tiers = build_tiers(team_scores)

    payload = {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "scheduleDate": parse_schedule_date(schedule_text),
        "sources": {
            "schedule": SCHEDULE_URL,
            "injuryReports": injury_sources,
        },
        "featured": build_featured(team_scores, tiers),
        "tiers": tiers,
        "injuries": build_injury_watch(serieses, team_scores),
        "highlights": build_highlights(serieses, team_scores),
        "series": build_series_cards(serieses, team_scores),
        "analyses": build_analyses(team_scores),
        "method": [
            {"score": "40%", "title": "攻守效率", "text": "看高針對性回合下，球隊能否維持穩定得失分品質。"},
            {"score": "35%", "title": "球星主導力", "text": "核心球員是否能在末節與半場攻防持續解題。"},
            {"score": "25%", "title": "健康折扣", "text": "核心可用性與輪替完整度，直接影響戰力分數能不能兌現。"},
        ],
    }
    return payload


def write_output(payload: Dict[str, object]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "window.PLAYOFFS_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )


def main() -> None:
    payload = build_payload()
    write_output(payload)
    print(f"Updated {OUTPUT}")


if __name__ == "__main__":
    main()

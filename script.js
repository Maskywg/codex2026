const fallbackData = {
  generatedAt: "",
  scheduleDate: "資料尚未更新",
  sources: { schedule: "", injuryReports: [] },
  featured: {
    team: "Oklahoma City Thunder",
    record: "3-0",
    score: "97 / 100",
    tier: "爭冠第一梯",
    summary: "尚未載入自動更新資料，請先執行更新腳本。"
  },
  tiers: [],
  injuries: [],
  highlights: [],
  series: { east: [], west: [] },
  analyses: [],
  method: [
    { score: "40%", title: "攻守效率", text: "看高針對性回合下，球隊能否維持穩定得失分品質。" },
    { score: "35%", title: "球星主導力", text: "核心球員是否能在末節與半場攻防持續解題。" },
    { score: "25%", title: "健康折扣", text: "核心可用性與輪替完整度，直接影響戰力分數能不能兌現。" }
  ]
};

const data = window.PLAYOFFS_DATA || fallbackData;

function renderTiers() {
  const root = document.getElementById("tiers");
  root.innerHTML = data.tiers
    .map(
      (tier) => `
        <article class="tier-card">
          <span class="power-badge">${tier.label}</span>
          <h3>${tier.title}</h3>
          <p>${tier.note}</p>
          <ul class="tier-list">
            ${tier.teams
              .map(
                (team) => `
                  <li>
                    <span>${team.name}</span>
                    <span class="score-number">${team.score}</span>
                  </li>
                `
              )
              .join("")}
          </ul>
        </article>
      `
    )
    .join("");
}

function renderInjuries() {
  const root = document.getElementById("injury-grid");
  root.innerHTML = data.injuries
    .map(
      (item) => `
        <article class="injury-card">
          <span class="injury-tag">${item.tag}</span>
          <h3>${item.team}</h3>
          <p>${item.detail}</p>
          <span class="injury-impact">${item.impact}</span>
        </article>
      `
    )
    .join("");
}

function renderSeries(group, targetId) {
  const root = document.getElementById(targetId);
  root.innerHTML = group
    .map(
      (item) => `
        <article class="series-card">
          <div class="series-head">
            <strong>${item.matchup}</strong>
            <span class="series-meta">${item.leader}</span>
          </div>
          <p>${item.angle}</p>
          <div class="series-strength">
            <small>戰力熱度</small>
            <div class="strength-bar" aria-hidden="true">
              <span style="width: ${item.power}%"></span>
            </div>
            <small>${item.power}</small>
          </div>
        </article>
      `
    )
    .join("");
}

function renderHighlights() {
  const root = document.querySelector(".highlight-strip");
  root.innerHTML = data.highlights
    .map(
      (item) => `
        <article>
          <span class="strip-label">${item.label}</span>
          <strong>${item.title}</strong>
          <p>${item.text}</p>
        </article>
      `
    )
    .join("");
}

function renderAnalyses() {
  const root = document.querySelector(".analysis-grid");
  root.innerHTML = data.analyses
    .map(
      (item) => `
        <article class="analysis-card">
          <p class="eyebrow">${item.eyebrow}</p>
          <h2>${item.title}</h2>
          <p>${item.text}</p>
        </article>
      `
    )
    .join("");
}

function renderMethod() {
  const root = document.querySelector(".method-grid");
  root.innerHTML = data.method
    .map(
      (item) => `
        <article class="method-card">
          <span class="method-score">${item.score}</span>
          <h3>${item.title}</h3>
          <p>${item.text}</p>
        </article>
      `
    )
    .join("");
}

function renderFeatured() {
  document.querySelector(".featured-team h2").textContent = data.featured.team;
  document.querySelector(".featured-team p").textContent = data.featured.summary;

  const stats = document.querySelectorAll(".panel-stats strong");
  stats[0].textContent = data.featured.score;
  stats[1].textContent = data.featured.record;
  stats[2].textContent = data.featured.tier;
}

function renderDates() {
  const heroNotes = document.querySelectorAll(".hero-notes li");
  heroNotes[0].textContent = `資料基準日：${data.scheduleDate}`;
  heroNotes[1].textContent = `最近更新：${data.generatedAt || "未產生資料"}`;

  const footer = document.querySelector(".footer p");
  footer.textContent = `內容依官方季後賽賽程與傷兵報告整理。資料基準日為 ${data.scheduleDate}，產生時間為 ${data.generatedAt || "未產生"}。`;
}

function renderBenchMob() {
  const root = document.getElementById("bench-mob");
  if (!root || !data.benchMob) return;
  root.innerHTML = data.benchMob.map(p => {
    const fires = "🔥".repeat(p.fire) + "🩶".repeat(5 - p.fire);
    const bar = `<div class="bench-bar"><span style="width:${p.index}%"></span></div>`;
    return `
      <article class="bench-card">
        <div class="bench-head">
          <div>
            <span class="bench-role">${p.role}</span>
            <h3 class="bench-name">${p.player}</h3>
            <span class="bench-team">${p.team}</span>
          </div>
          <div class="bench-index">
            <div class="bench-index-num">${p.index}</div>
            <div class="bench-fires">${fires}</div>
          </div>
        </div>
        <div class="bench-highlight">⚡ ${p.highlight}</div>
        <p class="bench-note">${p.note}</p>
        ${bar}
      </article>`;
  }).join("");
}

renderFeatured();
renderDates();
renderTiers();
renderInjuries();
renderHighlights();
renderSeries(data.series.east, "east-series");
renderSeries(data.series.west, "west-series");
renderAnalyses();
renderBenchMob();
renderMethod();

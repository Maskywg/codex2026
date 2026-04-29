const draftData = {
  timeline: [
    {
      date: "Apr 24",
      title: "Early Entry 申請截止",
      text: "想投入 2026 NBA Draft 的 early entry 球員需在美東時間 11:59 PM 前完成申請。"
    },
    {
      date: "May 8-10",
      title: "NBA G League Combine",
      text: "芝加哥預熱場，部分球員會藉由這裡爭取正式 Combine 入場券。"
    },
    {
      date: "May 10",
      title: "NBA Draft Lottery",
      text: "抽出前四順位，Washington、Indiana、Brooklyn 目前並列最高狀元機率。"
    },
    {
      date: "May 10-17",
      title: "NBA Draft Combine",
      text: "體測、面試、對抗賽與醫療資訊會重塑首輪排序。"
    },
    {
      date: "Jun 13",
      title: "Early Entry 退選截止",
      text: "球員需在美東時間 5 PM 前決定是否保留選秀資格。"
    },
    {
      date: "Jun 23-24",
      title: "Draft Nights",
      text: "第一輪 6 月 23 日，第二輪 6 月 24 日，兩晚皆於 8 PM ET 開始。"
    }
  ],
  lottery: [
    { team: "Washington", record: "17-65", odds: 14 },
    { team: "Indiana", record: "19-63", odds: 14 },
    { team: "Brooklyn", record: "20-62", odds: 14 },
    { team: "Utah", record: "22-60", odds: 11.5 },
    { team: "Sacramento", record: "22-60", odds: 11.5 },
    { team: "Memphis", record: "25-57", odds: 9 },
    { team: "New Orleans", record: "26-56", odds: 6.8 },
    { team: "Dallas", record: "26-56", odds: 6.7 },
    { team: "Chicago", record: "31-51", odds: 4.5 },
    { team: "Milwaukee", record: "32-50", odds: 3 }
  ],
  prospects: [
    {
      name: "AJ Dybantsa",
      school: "BYU",
      role: "6'9 側翼",
      type: "wing",
      text: "兼具身材、運動能力與雙向天花板，若外線穩定度繼續提升，會是狀元討論核心。",
      tags: ["two-way upside", "shot creation", "transition"]
    },
    {
      name: "Darryn Peterson",
      school: "Kansas",
      role: "後衛",
      type: "guard",
      text: "純得分能力突出，能持球、接球與高難度投籃；健康狀態會影響最終順位。",
      tags: ["pull-up scoring", "handle", "tough shots"]
    },
    {
      name: "Cameron Boozer",
      school: "Duke",
      role: "前場核心",
      type: "frontcourt",
      text: "籃板、傳球與護框讓他不只是得分手，而是能撐起攻防架構的高地板新秀。",
      tags: ["rebounding", "passing", "rim protection"]
    },
    {
      name: "Kingston Flemings",
      school: "Houston",
      role: "後衛",
      type: "guard",
      text: "爆發型後場，若能把組織與防守穩定性補上，會持續逼近前三集團。",
      tags: ["burst", "paint touch", "pressure"]
    },
    {
      name: "Caleb Wilson",
      school: "UNC",
      role: "前場",
      type: "frontcourt",
      text: "長度、活動力與防守覆蓋面是賣點，適合需要前場機動性的重建球隊。",
      tags: ["length", "switching", "finishing"]
    },
    {
      name: "Mikel Brown Jr.",
      school: "Louisville",
      role: "控球後衛",
      type: "guard",
      text: "節奏感與傳控創造力讓他有首輪上升空間，關鍵在於對抗與防守承受度。",
      tags: ["playmaking", "tempo", "touch"]
    }
  ],
  notes: [
    {
      title: "狀元籤不是單純選最好球員",
      text: "Dybantsa、Peterson、Boozer 的排序很可能取決於抽中球隊缺口：側翼門面、持球得分或前場支點。"
    },
    {
      title: "Combine 會改變中段首輪",
      text: "體測數據、醫療報告與面試通常對第 8 到第 25 順位影響最大，尤其是角色定位還沒定型的球員。"
    },
    {
      title: "籤權交易會讓順位更複雜",
      text: "NBA 官方順位已包含多個可能轉讓註記；樂透結果出爐後，實際持有者才會更清楚。"
    }
  ]
};

function renderTimeline() {
  const root = document.getElementById("timeline-list");
  root.innerHTML = draftData.timeline
    .map(
      (item) => `
        <article>
          <time>${item.date}</time>
          <div>
            <h3>${item.title}</h3>
            <p>${item.text}</p>
          </div>
        </article>
      `
    )
    .join("");
}

function renderLottery() {
  const root = document.getElementById("lottery-grid");
  root.innerHTML = draftData.lottery
    .map((team, index) => {
      const height = Math.max(18, team.odds * 5);
      return `
        <article class="lottery-card" style="--bar-height: ${height}%">
          <div class="rank-number">${index + 1}</div>
          <h3>${team.team}</h3>
          <span class="lottery-odds">${team.odds.toFixed(1)}% No.1 odds</span>
          <p>${team.record}</p>
        </article>
      `;
    })
    .join("");
}

function renderProspects(filter = "all") {
  const root = document.getElementById("prospect-grid");
  const prospects =
    filter === "all"
      ? draftData.prospects
      : draftData.prospects.filter((prospect) => prospect.type === filter);

  root.innerHTML = prospects
    .map(
      (prospect) => `
        <article class="prospect-card">
          <header>
            <div>
              <span class="prospect-meta">${prospect.school} · ${prospect.role}</span>
              <h3>${prospect.name}</h3>
            </div>
          </header>
          <p>${prospect.text}</p>
          <div class="skill-tags">
            ${prospect.tags.map((tag) => `<span>${tag}</span>`).join("")}
          </div>
        </article>
      `
    )
    .join("");
}

function renderNotes() {
  const root = document.getElementById("notes-grid");
  root.innerHTML = draftData.notes
    .map(
      (note) => `
        <article class="note-card">
          <h3>${note.title}</h3>
          <p>${note.text}</p>
        </article>
      `
    )
    .join("");
}

function bindFilters() {
  document.querySelectorAll(".filter-button").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".filter-button").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      renderProspects(button.dataset.filter);
    });
  });
}

renderTimeline();
renderLottery();
renderProspects();
renderNotes();
bindFilters();

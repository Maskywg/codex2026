const draftData = {
  timeline: [
    {
      date: "Apr 24",
      title: "Early Entry 申請截止",
      status: "已結束",
      text: "想投入 2026 NBA Draft 的 early entry 球員需在美東時間 11:59 PM 前完成申請。"
    },
    {
      date: "May 8-10",
      title: "NBA G League Combine",
      status: "已結束",
      text: "芝加哥預熱場，部分球員會藉由這裡爭取正式 Combine 入場券。"
    },
    {
      date: "May 10",
      title: "NBA Draft Lottery",
      status: "已開獎",
      text: "Washington 抽中狀元籤，Utah、Memphis、Chicago 補上前四順位。"
    },
    {
      date: "May 10-17",
      title: "NBA Draft Combine",
      status: "進行中",
      text: "體測、面試、對抗賽與醫療資訊會重塑首輪排序，尤其是中段首輪。"
    },
    {
      date: "Jun 13",
      title: "Early Entry 退選截止",
      status: "下一個關卡",
      text: "球員需在美東時間 5 PM 前決定是否保留選秀資格。"
    },
    {
      date: "Jun 23-24",
      title: "Draft Nights",
      status: "選秀夜",
      text: "第一輪 6 月 23 日，第二輪 6 月 24 日，兩晚皆於 8 PM ET 開始。"
    }
  ],
  lottery: [
    { pick: 1, team: "Washington", original: "14.0%", movement: "守住狀元區" },
    { pick: 2, team: "Utah", original: "11.5%", movement: "上升" },
    { pick: 3, team: "Memphis", original: "9.0%", movement: "上升" },
    { pick: 4, team: "Chicago", original: "4.5%", movement: "大幅上升" },
    { pick: 5, team: "LA Clippers via Indiana", original: "14.0%", movement: "由 Indiana 籤轉讓" },
    { pick: 6, team: "Brooklyn", original: "14.0%", movement: "下滑" },
    { pick: 7, team: "Sacramento", original: "11.5%", movement: "下滑" },
    { pick: 8, team: "Atlanta via New Orleans", original: "6.8%", movement: "可能轉讓" },
    { pick: 9, team: "Dallas", original: "6.7%", movement: "原區間" },
    { pick: 10, team: "Milwaukee", original: "3.0%", movement: "待轉讓註記" },
    { pick: 11, team: "Miami", original: "1.0%", movement: "上升" },
    { pick: 12, team: "Oklahoma City via LA Clippers", original: "1.5%", movement: "由 Clippers 籤轉讓" },
    { pick: 13, team: "Miami", original: "1.0%", movement: "第二支樂透籤" },
    { pick: 14, team: "Charlotte", original: "0.5%", movement: "樂透末段" }
  ],
  prospects: [
    {
      name: "AJ Dybantsa",
      school: "BYU",
      role: "6'9 側翼",
      type: "wing",
      text: "具備門面級側翼身材與雙向天花板，若外線穩定度延續，會是 Washington 狀元籤討論核心。",
      tags: ["two-way upside", "shot creation", "transition"]
    },
    {
      name: "Darryn Peterson",
      school: "Kansas",
      role: "後衛",
      type: "guard",
      text: "純得分能力突出，能持球、接球與高難度投籃；適合需要半場進攻主引擎的球隊。",
      tags: ["pull-up scoring", "handle", "tough shots"]
    },
    {
      name: "Cameron Boozer",
      school: "Duke",
      role: "前場核心",
      type: "frontcourt",
      text: "籃板、傳球與禁區攻防讓他不只是得分手，而是能撐起球隊結構的高地板新秀。",
      tags: ["rebounding", "passing", "paint force"]
    },
    {
      name: "Kingston Flemings",
      school: "Houston",
      role: "後衛",
      type: "guard",
      text: "爆發型後場，能製造油漆區壓力；Combine 與面試會影響他能否逼近前三集團。",
      tags: ["burst", "paint touch", "pressure"]
    },
    {
      name: "Caleb Wilson",
      school: "UNC",
      role: "前場",
      type: "frontcourt",
      text: "長度、活動力與防守覆蓋面是賣點，適合需要前場機動性與防守彈性的重建隊。",
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
      title: "狀元籤變成 Washington 的重建方向題",
      text: "巫師可以選最高天花板側翼，也可以用狀元籤重塑持球核心；真正問題不是誰最有名，而是誰能成為第一進攻選項。"
    },
    {
      title: "Utah、Memphis、Chicago 抽進前四，交易市場會更吵",
      text: "這三隊的位置都足以進入 Dybantsa、Peterson、Boozer 討論區，也會讓想搶高順位的隊伍開始報價。"
    },
    {
      title: "Brooklyn 下滑到第六，選擇會更偏向板塊補洞",
      text: "第六順位仍有好球員，但很可能從狀元級三人討論，轉成後衛、側翼或長人哪個更補陣容缺口。"
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
            <span class="movement">${item.status}</span>
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
    .map((team) => {
      const height = Math.max(18, 100 - team.pick * 4.5);
      return `
        <article class="lottery-card" style="--bar-height: ${height}%">
          <div class="pick-number">${team.pick}</div>
          <h3>${team.team}</h3>
          <span class="lottery-odds">${team.original} original No.1 odds</span>
          <p>${team.movement}</p>
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
          <span class="prospect-meta">${prospect.school} · ${prospect.role}</span>
          <h3>${prospect.name}</h3>
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

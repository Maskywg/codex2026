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
      status: "已結束",
      text: "體測、面試、對抗賽與醫療資訊已進入各隊內部板塊，尤其影響樂透後段到首輪中段。"
    },
    {
      date: "Jun 13",
      title: "Early Entry 退選截止",
      status: "已截止",
      text: "最終退選期限已過，參選名單大致定案，球隊開始把注意力放在最後試訓與交易報價。"
    },
    {
      date: "Jun 23-24",
      title: "Draft Nights",
      status: "倒數中",
      text: "第一輪 6 月 24 日台灣時間早上 8 點，第二輪 6 月 25 日台灣時間早上 8 點。"
    }
  ],
  updates: [
    {
      label: "狀元籤最後風向",
      title: "Washington 仍以 Dybantsa 為主線，但 Peterson 已進入真討論",
      text: "最新報導指出 Wizards 內部對 Darryn Peterson 的興趣升溫，讓原本偏向 AJ Dybantsa 的狀元討論出現最後懸念。"
    },
    {
      label: "樂透第 11 順位",
      title: "Golden State 成為交易觀察點",
      text: "Warriors 持有第 11 順位，管理層公開表示會評估自選、向後交易或搭配其他操作補強陣容。"
    },
    {
      label: "名單狀態",
      title: "退選截止已過，板塊進入最後收斂",
      text: "6 月 13 日退選期限後，球隊更能鎖定可選名單；接下來的變化多半來自醫療資訊、試訓回饋與選秀夜交易。"
    },
    {
      label: "觀戰提醒",
      title: "台灣觀眾是 6/24、6/25 早上 8 點",
      text: "美東 6/23、6/24 晚間 8 點開選，換算台灣時間分別是 6/24、6/25 早上 8 點。"
    },
    {
      label: "國際球員",
      title: "Karim Lopez、Sergio de Larrea 領銜 5 人名單",
      text: "NBA 官方 6/15 更新後，仍有 5 位國際 early entry 球員保留參選資格，Suigo 等 3 人已退選。"
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
    { pick: 11, team: "Golden State", original: "2.0%", movement: "交易觀察點" },
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
      text: "純得分能力突出，能持球、接球與高難度投籃；最新風向讓他成為 Washington 狀元籤的真正變數。",
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
      name: "Nate Ament",
      school: "Tennessee",
      role: "側翼前場",
      type: "wing",
      text: "具備尺寸、投射與防守想像空間，是樂透區後段最容易被交易上搶的高上限拼圖之一。",
      tags: ["size", "shooting", "upside"]
    },
    {
      name: "Darius Acuff Jr.",
      school: "Arkansas",
      role: "後衛",
      type: "guard",
      text: "具備得分爆發與持球侵略性，若球隊需要第二波創造者，他會是首輪前段到中段的熱門名字。",
      tags: ["rim pressure", "scoring", "creator"]
    },
    {
      name: "Mikel Brown Jr.",
      school: "Louisville",
      role: "控球後衛",
      type: "guard",
      text: "節奏感與傳控創造力讓他有首輪上升空間，關鍵在於對抗與防守承受度。",
      tags: ["playmaking", "tempo", "touch"]
    },
    {
      name: "Chris Cenac Jr.",
      school: "Houston",
      role: "前場",
      type: "frontcourt",
      text: "身材與活動力讓他成為中後段樂透到首輪中段的長線投資，最後順位會取決於球隊對養成時間的耐心。",
      tags: ["mobility", "rim play", "development"]
    },
    {
      name: "Labaron Philon Jr.",
      school: "Alabama",
      role: "後衛",
      type: "guard",
      text: "近期多支中段首輪球隊被連在一起，賣點是進攻直覺、節奏變化與能否補上後場火力。",
      tags: ["pace", "touch", "guard depth"]
    }
  ],
  international: [
    {
      name: "Karim Lopez",
      team: "New Zealand Breakers",
      country: "Mexico / Australia",
      height: "6'8",
      status: "2007 DOB",
      text: "墨西哥側翼，NBL 職業賽經驗與年齡優勢是賣點；若球隊願意押國際養成，會是今年最值得追的國際名字。",
      tags: ["wing size", "NBL reps", "first-round watch"]
    },
    {
      name: "Sergio de Larrea",
      team: "Valencia",
      country: "Spain",
      height: "6'6",
      status: "2005 DOB",
      text: "西班牙大型後衛，具備 ACB 與 EuroLeague 背景；成熟度、傳控視野與投射穩定性讓他適合後段首輪到二輪初觀察。",
      tags: ["big guard", "EuroLeague", "playmaking"]
    },
    {
      name: "Mohammad Amini",
      team: "Nancy",
      country: "Iran / France",
      height: "6'7",
      status: "2005 DOB",
      text: "具備側翼尺寸的後場球員，若能展現防守對位彈性與穩定外線，會是二輪與雙向合約區間的國際觀察點。",
      tags: ["size", "guard wing", "development"]
    },
    {
      name: "Vsevolod Ishchenko",
      team: "Lokomotiv",
      country: "Russia",
      height: "6'3",
      status: "2005 DOB",
      text: "俄羅斯後衛，仍保留 early entry 資格；重點會在控場、投射與是否有足夠 NBA 後場身材對抗。",
      tags: ["guard", "shooting", "stash watch"]
    },
    {
      name: "Jack Kayil",
      team: "Alba Berlin",
      country: "Germany",
      height: "6'3",
      status: "2006 DOB",
      text: "德國後衛，Alba Berlin 體系出身；年齡與歐洲養成背景讓他偏向長線觀察或 draft-and-stash 討論。",
      tags: ["Germany", "guard", "stash upside"]
    }
  ],
  notes: [
    {
      title: "狀元籤不只是 Dybantsa 單選題",
      text: "Dybantsa 的側翼天花板仍最直觀，但 Peterson 的持球得分與半場主攻能力讓 Washington 必須重新確認重建核心的形狀。"
    },
    {
      title: "Utah、Memphis、Chicago 抽進前四，交易市場會更吵",
      text: "這三隊的位置都足以進入 Dybantsa、Peterson、Boozer 討論區，也會讓想搶高順位的隊伍開始報價。"
    },
    {
      title: "第 11 順位可能是樂透區交易開關",
      text: "Golden State 的位置剛好卡在樂透後段，若有球隊想跳上來搶 Ament、Acuff、Burries 或前場長人，這裡會是熱門電話區。"
    }
  ]
};

function renderUpdates() {
  const root = document.getElementById("update-grid");
  root.innerHTML = draftData.updates
    .map(
      (item) => `
        <article class="update-card">
          <span>${item.label}</span>
          <h3>${item.title}</h3>
          <p>${item.text}</p>
        </article>
      `
    )
    .join("");
}

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

function renderInternational() {
  const root = document.getElementById("international-grid");
  root.innerHTML = draftData.international
    .map(
      (player) => `
        <article class="international-card">
          <span class="prospect-meta">${player.country} · ${player.height} · ${player.status}</span>
          <h3>${player.name}</h3>
          <strong>${player.team}</strong>
          <p>${player.text}</p>
          <div class="skill-tags">
            ${player.tags.map((tag) => `<span>${tag}</span>`).join("")}
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

function bindMusic() {
  const audio = document.getElementById("page-music");
  const button = document.getElementById("music-toggle");
  const label = document.getElementById("music-toggle-text");

  if (!audio || !button || !label) return;

  audio.volume = 0.45;

  const syncButton = () => {
    const isPlaying = !audio.paused;
    button.classList.toggle("is-playing", isPlaying);
    button.setAttribute("aria-pressed", String(isPlaying));
    button.setAttribute("aria-label", isPlaying ? "暫停背景音樂" : "播放背景音樂");
    label.textContent = isPlaying ? "暫停音樂" : "播放音樂";
  };

  const startMusic = () => {
    audio.play().then(syncButton).catch(syncButton);
  };

  button.addEventListener("click", () => {
    if (audio.paused) {
      startMusic();
      return;
    }

    audio.pause();
    syncButton();
  });

  audio.addEventListener("play", syncButton);
  audio.addEventListener("pause", syncButton);
  startMusic();

  ["pointerdown", "keydown", "touchstart", "scroll"].forEach((eventName) => {
    window.addEventListener(
      eventName,
      () => {
        if (audio.paused) startMusic();
      },
      { once: true, passive: true }
    );
  });
}

renderUpdates();
renderTimeline();
renderLottery();
renderProspects();
renderInternational();
renderNotes();
bindFilters();
bindMusic();

const CATEGORIES = [
  "Affiliate License-Licensee",
  "Affiliate License-Licensor",
  "Agreement Date",
  "Anti-Assignment",
  "Audit Rights",
  "Cap On Liability",
  "Change Of Control",
  "Competitive Restriction Exception",
  "Covenant Not To Sue",
  "Document Name",
  "Effective Date",
  "Exclusivity",
  "Expiration Date",
  "Governing Law",
  "Insurance",
  "Ip Ownership Assignment",
  "Irrevocable Or Perpetual License",
  "Joint Ip Ownership",
  "License Grant",
  "Liquidated Damages",
  "Minimum Commitment",
  "Most Favored Nation",
  "No-Solicit Of Customers",
  "No-Solicit Of Employees",
  "Non-Compete",
  "Non-Disparagement",
  "Non-Transferable License",
  "Notice Period To Terminate Renewal",
  "Parties",
  "Post-Termination Services",
  "Price Restrictions",
  "Renewal Term",
  "Revenue/Profit Sharing",
  "Rofr/Rofo/Rofn",
  "Source Code Escrow",
  "Termination For Convenience",
  "Third Party Beneficiary",
  "Uncapped Liability",
  "Unlimited/All-You-Can-Eat-License",
  "Volume Restriction",
  "Warranty Duration",
];

// Extracted directly from the CUAD dataset: each category has exactly one
// canonical "Details" phrasing (verified: 0/41 categories have more than one).
const CATEGORY_DETAILS = {
  "Affiliate License-Licensee": "Does the contract contain a license grant to a licensee (incl. sublicensor) and the affiliates of such licensee/sublicensor?",
  "Affiliate License-Licensor": "Does the contract contain a license grant by affiliates of the licensor or that includes intellectual property of affiliates of the licensor?",
  "Agreement Date": "The date of the contract",
  "Anti-Assignment": "Is consent or notice required of a party if the contract is assigned to a third party?",
  "Audit Rights": "Does a party have the right to  audit the books, records, or physical locations of the counterparty to ensure compliance with the contract?",
  "Cap On Liability": "Does the contract include a cap on liability upon the breach of a party’s obligation? This includes time limitation for the counterparty to bring claims or maximum amount for recovery.",
  "Change Of Control": "Does one party have the right to terminate or is consent or notice required of the counterparty if such party undergoes a change of control, such as a merger, stock sale, transfer of all or substantially all of its assets or business, or assignment by operation of law?",
  "Competitive Restriction Exception": "This category includes the exceptions or carveouts to Non-Compete, Exclusivity and No-Solicit of Customers above.",
  "Covenant Not To Sue": "Is a party restricted from contesting the validity of the counterparty’s ownership of intellectual property or otherwise bringing a claim against the counterparty for matters unrelated to the contract?",
  "Document Name": "The name of the contract",
  "Effective Date": "The date when the contract is effective",
  "Exclusivity": "Is there an exclusive dealing  commitment with the counterparty? This includes a commitment to procure all “requirements” from one party of certain technology, goods, or services or a prohibition on licensing or selling technology, goods or services to third parties, or a prohibition on  collaborating or working with other parties), whether during the contract or  after the contract ends (or both).",
  "Expiration Date": "On what date will the contract's initial term expire?",
  "Governing Law": "Which state/country's law governs the interpretation of the contract?",
  "Insurance": "Is there a requirement for insurance that must be maintained by one party for the benefit of the counterparty?",
  "Ip Ownership Assignment": "Does intellectual property created  by one party become the property of the counterparty, either per the terms of the contract or upon the occurrence of certain events?",
  "Irrevocable Or Perpetual License": "Does the contract contain a  license grant that is irrevocable or perpetual?",
  "Joint Ip Ownership": "Is there any clause providing for joint or shared ownership of intellectual property between the parties to the contract?",
  "License Grant": "Does the contract contain a license granted by one party to its counterparty?",
  "Liquidated Damages": "Does the contract contain a clause that would award either party liquidated damages for breach or a fee upon the termination of a contract (termination fee)?",
  "Minimum Commitment": "Is there a minimum order size or minimum amount or units per-time period that one party must buy from the counterparty under the contract?",
  "Most Favored Nation": "Is there a clause that if a third party gets better terms on the licensing or sale of technology/goods/services described in the contract, the buyer of such technology/goods/services under the contract shall be entitled to those better terms?",
  "No-Solicit Of Customers": "Is a party restricted from contracting or soliciting customers or partners of the counterparty, whether during the contract or after the contract ends (or both)?",
  "No-Solicit Of Employees": "Is there a restriction on a party’s soliciting or hiring employees and/or contractors from the  counterparty, whether during the contract or after the contract ends (or both)?",
  "Non-Compete": "Is there a restriction on the ability of a party to compete with the counterparty or operate in a certain geography or business or technology sector?",
  "Non-Disparagement": "Is there a requirement on a party not to disparage the counterparty?",
  "Non-Transferable License": "Does the contract limit the ability of a party to transfer the license being granted to a third party?",
  "Notice Period To Terminate Renewal": "What is the notice period required to terminate renewal?",
  "Parties": "The two or more parties who signed the contract",
  "Post-Termination Services": "Is a party subject to obligations after the termination or expiration of a contract, including any post-termination transition, payment, transfer of IP, wind-down, last-buy, or similar commitments?",
  "Price Restrictions": "Is there a restriction on the  ability of a party to raise or reduce prices of technology, goods, or  services provided?",
  "Renewal Term": "What is the renewal term after the initial term expires? This includes automatic extensions and unilateral extensions with prior notice.",
  "Revenue/Profit Sharing": "Is one party required to share revenue or profit with the counterparty for any technology, goods, or services?",
  "Rofr/Rofo/Rofn": "Is there a clause granting one party a right of first refusal, right of first offer or right of first negotiation to purchase, license, market, or distribute equity interest, technology, assets, products or services?",
  "Source Code Escrow": "Is one party required to deposit its source code into escrow with a third party, which can be released to the counterparty upon the occurrence of certain events (bankruptcy,  insolvency, etc.)?",
  "Termination For Convenience": "Can a party terminate this  contract without cause (solely by giving a notice and allowing a waiting  period to expire)?",
  "Third Party Beneficiary": "Is there a non-contracting party who is a beneficiary to some or all of the clauses in the contract and therefore can enforce its rights against a contracting party?",
  "Uncapped Liability": "Is a party’s liability uncapped upon the breach of its obligation in the contract? This also includes uncap liability for a particular type of breach such as IP infringement or breach of confidentiality obligation.",
  "Unlimited/All-You-Can-Eat-License": "Is there a clause granting one party an “enterprise,” “all you can eat” or unlimited usage license?",
  "Volume Restriction": "Is there a fee increase or consent requirement, etc. if one party’s use of the product/services exceeds certain threshold?",
  "Warranty Duration": "What is the duration of any  warranty against defects or errors in technology, products, or services  provided under the contract?",
};

const PASSAGE_TRUNCATE_LENGTH = 220;

const ICONS = {
  chevronDown: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>',
  chevronUp: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="18 15 12 9 6 15"/></svg>',
  sparkle: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v4M12 17v4M4.2 4.2l2.9 2.9M16.9 16.9l2.9 2.9M3 12h4M17 12h4M4.2 19.8l2.9-2.9M16.9 7.1l2.9-2.9"/></svg>',
  check: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>',
  thumbUp: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 10v12"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a2.5 2.5 0 0 1 3 2.5v1.38"/></svg>',
  thumbDown: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="transform:scaleY(-1)"><path d="M7 10v12"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a2.5 2.5 0 0 1 3 2.5v1.38"/></svg>',
};

// ---------- Element references ----------

const loginScreen = document.getElementById("login-screen");
const loginForm = document.getElementById("login-form");
const loginUsername = document.getElementById("login-username");
const loginPassword = document.getElementById("login-password");
const loginError = document.getElementById("login-error");
const appRoot = document.getElementById("app-root");
const accountUsername = document.getElementById("account-username");
const logoutBtn = document.getElementById("logout-btn");
const adminBtn = document.getElementById("admin-btn");
const adminModal = document.getElementById("admin-modal");
const adminCloseBtn = document.getElementById("admin-close-btn");
const feedbackStatsEl = document.getElementById("feedback-stats");
const createUserForm = document.getElementById("create-user-form");
const newUserUsername = document.getElementById("new-user-username");
const newUserPassword = document.getElementById("new-user-password");
const newUserRole = document.getElementById("new-user-role");
const createUserError = document.getElementById("create-user-error");
const adminUsersList = document.getElementById("admin-users-list");
const adminHistoryHeading = document.getElementById("admin-history-heading");
const adminHistoryList = document.getElementById("admin-history-list");

const titleInput = document.getElementById("title");
const titleSuggestionsEl = document.getElementById("title-suggestions");
const categorySelect = document.getElementById("category");
const detailsInput = document.getElementById("details");
const suggestionChip = document.getElementById("suggestion-chip");
const submitBtn = document.getElementById("submit-btn");
const newQuestionBtn = document.getElementById("new-question-btn");
const answerPanel = document.getElementById("answer-panel");
const historyList = document.getElementById("history-list");
const historyEmpty = document.getElementById("history-empty");
const healthDot = document.getElementById("health-dot");
const healthPill = document.getElementById("health-pill");

// ---------- State ----------

let allContracts = [];
let history = [];
let activeHistoryId = null;
let suggestionApplied = false;
let currentUser = null;

// ---------- Init ----------

for (const category of CATEGORIES) {
  const option = document.createElement("option");
  option.value = category;
  option.textContent = category;
  categorySelect.appendChild(option);
}

checkAuth();

// ---------- Auth ----------

async function checkAuth() {
  try {
    const res = await fetch("/auth/me");
    if (!res.ok) throw new Error("not authenticated");
    currentUser = await res.json();
    showApp();
  } catch {
    showLogin();
  }
}

function showLogin() {
  loginScreen.classList.remove("hidden");
  appRoot.classList.add("hidden");
}

function showApp() {
  loginScreen.classList.add("hidden");
  appRoot.classList.remove("hidden");
  accountUsername.textContent = currentUser.username;
  adminBtn.classList.toggle("hidden", currentUser.role !== "admin");

  renderEmptyAnswerPanel();
  refreshHealth();
  loadContracts();
  loadHistory();
}

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  loginError.classList.add("hidden");
  try {
    const res = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: loginUsername.value, password: loginPassword.value }),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      loginError.textContent = data.detail || "Login failed.";
      loginError.classList.remove("hidden");
      return;
    }
    currentUser = await res.json();
    loginPassword.value = "";
    showApp();
  } catch {
    loginError.textContent = "Could not reach the API.";
    loginError.classList.remove("hidden");
  }
});

logoutBtn.addEventListener("click", async () => {
  try {
    await fetch("/auth/logout", { method: "POST" });
  } catch {
    // ignore network errors on logout
  }
  currentUser = null;
  history = [];
  activeHistoryId = null;
  adminModal.classList.add("hidden");
  showLogin();
});

// ---------- Admin ----------

adminBtn.addEventListener("click", () => {
  adminModal.classList.remove("hidden");
  loadFeedbackStats();
  loadAdminUsers();
  adminHistoryHeading.textContent = "User history";
  adminHistoryList.innerHTML = "";
});

adminCloseBtn.addEventListener("click", () => {
  adminModal.classList.add("hidden");
});

async function loadFeedbackStats() {
  feedbackStatsEl.textContent = "Loading…";
  try {
    const res = await fetch("/admin/feedback-stats");
    if (!res.ok) {
      feedbackStatsEl.textContent = "Could not load stats.";
      return;
    }
    const stats = await res.json();
    feedbackStatsEl.innerHTML = "";
    const items = [
      ["Likes", stats.like_count],
      ["Dislikes", stats.dislike_count],
      ["Total", stats.total_feedback],
      ["Like ratio", stats.like_ratio !== null ? `${Math.round(stats.like_ratio * 100)}%` : "—"],
    ];
    for (const [label, value] of items) {
      const box = document.createElement("div");
      const val = document.createElement("span");
      val.className = "stat-value";
      val.textContent = value;
      const lab = document.createElement("span");
      lab.className = "stat-label";
      lab.textContent = label;
      box.appendChild(val);
      box.appendChild(lab);
      feedbackStatsEl.appendChild(box);
    }
  } catch {
    feedbackStatsEl.textContent = "Could not load stats.";
  }
}

async function loadAdminUsers() {
  adminUsersList.innerHTML = "";
  try {
    const res = await fetch("/admin/users");
    if (!res.ok) return;
    const users = await res.json();
    for (const u of users) {
      const row = document.createElement("div");
      row.className = "admin-user-row";
      const label = document.createElement("span");
      label.textContent = `${u.username} (${u.role})`;
      const viewBtn = document.createElement("button");
      viewBtn.type = "button";
      viewBtn.textContent = "View history";
      viewBtn.addEventListener("click", () => loadAdminHistory(u));
      row.appendChild(label);
      row.appendChild(viewBtn);
      adminUsersList.appendChild(row);
    }
  } catch {
    // leave the list empty on failure
  }
}

async function loadAdminHistory(user) {
  adminHistoryHeading.textContent = `History — ${user.username}`;
  adminHistoryList.innerHTML = "Loading…";
  try {
    const res = await fetch(`/admin/history?user_id=${encodeURIComponent(user.id)}`);
    if (!res.ok) {
      adminHistoryList.textContent = "Could not load history.";
      return;
    }
    const entries = await res.json();
    adminHistoryList.innerHTML = "";
    if (entries.length === 0) {
      adminHistoryList.textContent = "No questions yet.";
      return;
    }
    for (const entry of entries) {
      const item = document.createElement("div");
      item.className = "admin-history-item";

      const meta = document.createElement("div");
      meta.className = "admin-history-meta";
      meta.textContent = `${entry.category} · ${entry.title}`;
      item.appendChild(meta);

      const q = document.createElement("div");
      q.className = "admin-history-question";
      q.textContent = entry.question;
      item.appendChild(q);

      const a = document.createElement("div");
      a.className = "admin-history-answer";
      a.textContent = entry.answer;
      item.appendChild(a);

      adminHistoryList.appendChild(item);
    }
  } catch {
    adminHistoryList.textContent = "Could not load history.";
  }
}

createUserForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  createUserError.classList.add("hidden");
  try {
    const res = await fetch("/admin/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: newUserUsername.value,
        password: newUserPassword.value,
        role: newUserRole.value,
      }),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      createUserError.textContent = data.detail || "Could not create user.";
      createUserError.classList.remove("hidden");
      return;
    }
    newUserUsername.value = "";
    newUserPassword.value = "";
    newUserRole.selectedIndex = 0;
    loadAdminUsers();
  } catch {
    createUserError.textContent = "Could not reach the API.";
    createUserError.classList.remove("hidden");
  }
});

// ---------- Health ----------

async function refreshHealth() {
  try {
    const res = await fetch("/health");
    if (!res.ok) throw new Error("not ok");
    healthDot.className = "health-dot online";
    healthPill.title = "API online";
  } catch {
    healthDot.className = "health-dot offline";
    healthPill.title = "API unreachable";
  }
}

// ---------- Contracts autocomplete ----------

async function loadContracts() {
  try {
    const res = await fetch("/contracts");
    if (!res.ok) return;
    allContracts = await res.json();
  } catch {
    allContracts = [];
  }
}

// ---------- History (persisted) ----------

async function loadHistory() {
  try {
    const res = await fetch("/history");
    if (!res.ok) return;
    const entries = await res.json();
    history = entries.map((entry) => ({
      id: entry.id,
      category: entry.category,
      title: entry.title,
      question: entry.question,
      answer: entry.answer,
      contexts: entry.contexts,
      time: new Date(entry.timestamp),
      feedback: null,
      comment: null,
    }));
    renderHistoryList();
  } catch {
    // keep whatever history is already rendered on failure
  }
}

function renderTitleSuggestions(query) {
  titleSuggestionsEl.innerHTML = "";
  const q = query.trim().toLowerCase();
  const matches = (q ? allContracts.filter((t) => t.toLowerCase().includes(q)) : allContracts).slice(0, 8);

  if (matches.length === 0) {
    titleSuggestionsEl.classList.add("hidden");
    return;
  }

  for (const t of matches) {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "title-suggestion";
    const label = document.createElement("span");
    label.textContent = t;
    item.appendChild(label);
    item.addEventListener("click", () => {
      titleInput.value = t;
      titleSuggestionsEl.classList.add("hidden");
    });
    titleSuggestionsEl.appendChild(item);
  }
  titleSuggestionsEl.classList.remove("hidden");
}

titleInput.addEventListener("input", () => renderTitleSuggestions(titleInput.value));
titleInput.addEventListener("focus", () => renderTitleSuggestions(titleInput.value));

document.addEventListener("click", (e) => {
  if (e.target !== titleInput && !titleSuggestionsEl.contains(e.target)) {
    titleSuggestionsEl.classList.add("hidden");
  }
});

// ---------- Details suggestion ----------

function updateSuggestionChip() {
  const suggestion = CATEGORY_DETAILS[categorySelect.value];
  if (!suggestion) {
    suggestionChip.classList.add("hidden");
    return;
  }
  suggestionChip.classList.remove("hidden");
  if (suggestionApplied) {
    suggestionChip.classList.add("applied");
    suggestionChip.innerHTML = `${ICONS.check} Suggestion applied`;
  } else {
    suggestionChip.classList.remove("applied");
    suggestionChip.innerHTML = `${ICONS.sparkle} Use suggested detail`;
  }
}

categorySelect.addEventListener("change", () => {
  suggestionApplied = false;
  const suggestion = CATEGORY_DETAILS[categorySelect.value];
  if (suggestion && detailsInput.value.trim() === "") {
    detailsInput.value = suggestion;
    suggestionApplied = true;
  }
  updateSuggestionChip();
});

suggestionChip.addEventListener("click", () => {
  const suggestion = CATEGORY_DETAILS[categorySelect.value];
  if (!suggestion) return;
  if (!suggestionApplied) {
    detailsInput.value = suggestion;
  }
  suggestionApplied = !suggestionApplied;
  updateSuggestionChip();
});

// Apply the first category's suggestion on initial load too.
(function applyInitialSuggestion() {
  const suggestion = CATEGORY_DETAILS[categorySelect.value];
  if (suggestion) {
    detailsInput.value = suggestion;
    suggestionApplied = true;
  }
  updateSuggestionChip();
})();

// ---------- New question ----------

newQuestionBtn.addEventListener("click", () => {
  titleInput.value = "";
  categorySelect.selectedIndex = 0;
  detailsInput.value = "";
  suggestionApplied = false;
  updateSuggestionChip();
  categorySelect.dispatchEvent(new Event("change"));
  activeHistoryId = null;
  renderHistoryList();
  renderEmptyAnswerPanel();
  titleInput.focus();
});

// ---------- Ask ----------

submitBtn.addEventListener("click", async () => {
  const title = titleInput.value.trim();
  const category = categorySelect.value;
  const details = detailsInput.value.trim();

  if (!title || !details) {
    alert("Contract title and details are both required.");
    return;
  }

  const question = `Highlight the parts (if any) of this contract related to "${category}" that should be reviewed by a lawyer. Details: ${details}`;

  answerPanel.innerHTML = "";
  const loading = document.createElement("div");
  loading.className = "answer-card";
  loading.innerHTML = '<p class="loading-text">Retrieving clauses and generating the answer…</p>';
  answerPanel.appendChild(loading);

  submitBtn.disabled = true;

  try {
    const response = await fetch(`/contracts/${encodeURIComponent(title)}/questions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (response.status === 401) {
      showLogin();
      return;
    }

    if (!response.ok) {
      const text = await response.text();
      answerPanel.innerHTML = "";
      const errorCard = document.createElement("div");
      errorCard.className = "answer-card";
      const errorMsg = document.createElement("div");
      errorMsg.className = "answer-error";
      errorMsg.textContent = `Error ${response.status}: ${text}`;
      errorCard.appendChild(errorMsg);
      answerPanel.appendChild(errorCard);
      return;
    }

    await loadHistory(); // the new Q&A was already written to qa_history server-side
    if (history.length > 0) {
      activeHistoryId = history[0].id;
      renderHistoryList();
      renderAnswerCard(history[0]);
    }
  } catch (err) {
    answerPanel.innerHTML = "";
    const errorCard = document.createElement("div");
    errorCard.className = "answer-card";
    const errorMsg = document.createElement("div");
    errorMsg.className = "answer-error";
    errorMsg.textContent = `Could not reach the API: ${err.message}`;
    errorCard.appendChild(errorMsg);
    answerPanel.appendChild(errorCard);
  } finally {
    submitBtn.disabled = false;
  }
});

// ---------- History list ----------

function formatTime(date) {
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function renderHistoryList() {
  historyList.innerHTML = "";
  historyEmpty.style.display = history.length === 0 ? "block" : "none";

  for (const entry of history) {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "history-item" + (entry.id === activeHistoryId ? " active" : "");

    const categoryEl = document.createElement("div");
    categoryEl.className = "history-item-category";
    categoryEl.textContent = entry.category;
    item.appendChild(categoryEl);

    const metaEl = document.createElement("div");
    metaEl.className = "history-item-meta";
    const titleEl = document.createElement("span");
    titleEl.className = "history-item-title";
    titleEl.textContent = entry.title;
    const timeEl = document.createElement("span");
    timeEl.textContent = formatTime(entry.time);
    metaEl.appendChild(titleEl);
    metaEl.appendChild(timeEl);
    item.appendChild(metaEl);

    item.addEventListener("click", () => {
      activeHistoryId = entry.id;
      renderHistoryList();
      renderAnswerCard(entry);
    });

    historyList.appendChild(item);
  }
}

// ---------- Answer panel ----------

function renderEmptyAnswerPanel() {
  answerPanel.innerHTML = "";
  const empty = document.createElement("div");
  empty.className = "answer-empty-state";
  empty.textContent = "Ask a question about a known contract to see the answer here.";
  answerPanel.appendChild(empty);
}

function renderAnswerCard(entry) {
  answerPanel.innerHTML = "";

  const card = document.createElement("div");
  card.className = "answer-card";

  const meta = document.createElement("div");
  meta.className = "answer-meta";
  meta.textContent = `${entry.category} · ${entry.title}`;
  card.appendChild(meta);

  const answerText = document.createElement("p");
  answerText.className = "answer-text";
  answerText.textContent = entry.answer;
  card.appendChild(answerText);

  if (entry.contexts.length > 0) {
    card.appendChild(renderPassages(entry.contexts));
  }

  card.appendChild(renderFeedbackRow(entry));

  answerPanel.appendChild(card);
}

function renderPassages(contexts) {
  const wrapper = document.createElement("div");

  let open = false;
  const toggleBtn = document.createElement("button");
  toggleBtn.type = "button";
  toggleBtn.className = "passages-toggle";
  toggleBtn.innerHTML = `${ICONS.chevronDown} Retrieved passages (${contexts.length})`;

  const list = document.createElement("div");
  list.className = "passages-list";
  list.style.display = "none";

  contexts.forEach((context, i) => {
    list.appendChild(renderPassageItem(context, i));
  });

  toggleBtn.addEventListener("click", () => {
    open = !open;
    list.style.display = open ? "flex" : "none";
    toggleBtn.innerHTML = `${open ? ICONS.chevronUp : ICONS.chevronDown} Retrieved passages (${contexts.length})`;
  });

  wrapper.appendChild(toggleBtn);
  wrapper.appendChild(list);
  return wrapper;
}

function renderPassageItem(context, index) {
  const item = document.createElement("div");
  item.className = "passage-item";

  const label = document.createElement("span");
  label.className = "passage-label";
  label.textContent = `Passage ${index + 1}`;
  item.appendChild(label);

  const body = document.createElement("span");
  item.appendChild(body);

  const hint = document.createElement("span");
  hint.className = "passage-hint";
  item.appendChild(hint);

  const truncatable = context.length > PASSAGE_TRUNCATE_LENGTH;
  let expanded = false;

  function render() {
    if (truncatable && !expanded) {
      body.textContent = `${context.slice(0, PASSAGE_TRUNCATE_LENGTH)}…`;
      hint.textContent = "Click to show the full passage";
    } else {
      body.textContent = context;
      hint.textContent = truncatable ? "Click to collapse" : "";
    }
  }
  render();

  if (truncatable) {
    item.addEventListener("click", () => {
      expanded = !expanded;
      render();
    });
  }

  return item;
}

function renderFeedbackRow(entry) {
  const row = document.createElement("div");
  row.className = "feedback-row";

  const label = document.createElement("span");
  label.className = "feedback-label";
  label.textContent = "Was this helpful?";
  row.appendChild(label);

  const likeBtn = document.createElement("button");
  likeBtn.type = "button";
  likeBtn.className = "feedback-btn";
  likeBtn.innerHTML = `${ICONS.thumbUp} Helpful`;

  const dislikeBtn = document.createElement("button");
  dislikeBtn.type = "button";
  dislikeBtn.className = "feedback-btn";
  dislikeBtn.innerHTML = `${ICONS.thumbDown} Not helpful`;

  row.appendChild(likeBtn);
  row.appendChild(dislikeBtn);

  const commentBox = document.createElement("div");
  commentBox.className = "feedback-comment";
  const commentTextarea = document.createElement("textarea");
  commentTextarea.rows = 2;
  commentTextarea.placeholder = "Optional: tell us what was wrong...";
  const commentSubmit = document.createElement("button");
  commentSubmit.type = "button";
  commentSubmit.className = "new-question-btn";
  commentSubmit.style.width = "auto";
  commentSubmit.style.color = "var(--text)";
  commentSubmit.style.borderColor = "var(--border)";
  commentSubmit.textContent = "Send feedback";
  commentBox.appendChild(commentTextarea);
  commentBox.appendChild(commentSubmit);

  const sentLabel = document.createElement("div");
  sentLabel.className = "feedback-sent";

  function syncButtons() {
    likeBtn.classList.toggle("active-like", entry.feedback === "like");
    dislikeBtn.classList.toggle("active-dislike", entry.feedback === "dislike");
    commentBox.classList.toggle("visible", entry.feedback === "dislike" && entry.comment === null);
  }
  syncButtons();

  async function sendFeedback(rating, comment) {
    entry.feedback = rating;
    entry.comment = comment;
    try {
      await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: entry.title, question: entry.question, answer: entry.answer, rating, comment }),
      });
      sentLabel.textContent = "Thanks for your feedback!";
    } catch {
      sentLabel.textContent = "Could not send feedback.";
    }
  }

  likeBtn.addEventListener("click", () => {
    syncButtons();
    sendFeedback("like", null);
    likeBtn.classList.add("active-like");
    dislikeBtn.classList.remove("active-dislike");
    commentBox.classList.remove("visible");
  });

  dislikeBtn.addEventListener("click", () => {
    dislikeBtn.classList.add("active-dislike");
    likeBtn.classList.remove("active-like");
    commentBox.classList.add("visible");
  });

  commentSubmit.addEventListener("click", () => {
    sendFeedback("dislike", commentTextarea.value.trim() || null);
    commentBox.classList.remove("visible");
  });

  const column = document.createElement("div");
  column.style.display = "flex";
  column.style.flexDirection = "column";
  column.style.gap = "8px";
  column.appendChild(row);
  column.appendChild(commentBox);
  column.appendChild(sentLabel);
  return column;
}

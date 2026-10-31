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

const categorySelect = document.getElementById("category");
for (const category of CATEGORIES) {
  const option = document.createElement("option");
  option.value = category;
  option.textContent = category;
  categorySelect.appendChild(option);
}

const titleInput = document.getElementById("title");
const detailsInput = document.getElementById("details");
const submitBtn = document.getElementById("submit-btn");
const chatHistory = document.getElementById("chat-history");
const clearBtn = document.getElementById("clear-btn");

clearBtn.addEventListener("click", () => {
  chatHistory.innerHTML = "";
});

submitBtn.addEventListener("click", async () => {
  const title = titleInput.value.trim();
  const category = categorySelect.value;
  const details = detailsInput.value.trim();

  if (!title || !details) {
    alert("Contract title and details are both required.");
    return;
  }

  const question = `Highlight the parts (if any) of this contract related to "${category}" that should be reviewed by a lawyer. Details: ${details}`;

  const exchange = document.createElement("div");
  exchange.className = "exchange";

  const userBubble = document.createElement("div");
  userBubble.className = "bubble bubble-user";
  userBubble.textContent = question;
  exchange.appendChild(userBubble);

  const loadingBubble = document.createElement("div");
  loadingBubble.className = "loading-bubble";
  loadingBubble.textContent = "Retrieving clauses and generating the answer…";
  exchange.appendChild(loadingBubble);

  chatHistory.appendChild(exchange);
  exchange.scrollIntoView({ behavior: "smooth", block: "end" });

  submitBtn.disabled = true;

  try {
    const response = await fetch(`/contracts/${encodeURIComponent(title)}/questions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    loadingBubble.remove();

    if (!response.ok) {
      const text = await response.text();
      const errorBubble = document.createElement("div");
      errorBubble.className = "bubble bubble-assistant bubble-error";
      errorBubble.textContent = `Error ${response.status}: ${text}`;
      exchange.appendChild(errorBubble);
      return;
    }

    const data = await response.json();
    renderAnswer(exchange, title, question, data);
  } catch (err) {
    loadingBubble.remove();
    const errorBubble = document.createElement("div");
    errorBubble.className = "bubble bubble-assistant bubble-error";
    errorBubble.textContent = `Could not reach the API: ${err.message}`;
    exchange.appendChild(errorBubble);
  } finally {
    submitBtn.disabled = false;
    exchange.scrollIntoView({ behavior: "smooth", block: "end" });
  }
});

function renderAnswer(exchange, title, question, data) {
  const answerBubble = document.createElement("div");
  answerBubble.className = "bubble bubble-assistant";
  answerBubble.textContent = data.answer;
  exchange.appendChild(answerBubble);

  if (data.contexts && data.contexts.length > 0) {
    const detailsEl = document.createElement("details");
    const summary = document.createElement("summary");
    summary.textContent = `Retrieved passages (${data.contexts.length})`;
    detailsEl.appendChild(summary);

    const list = document.createElement("div");
    data.contexts.forEach((context, i) => {
      const item = document.createElement("div");
      item.className = "context-item";
      const label = document.createElement("span");
      label.className = "context-label";
      label.textContent = `Passage ${i + 1}`;
      item.appendChild(label);
      item.appendChild(document.createTextNode(context));
      list.appendChild(item);
    });
    detailsEl.appendChild(list);
    exchange.appendChild(detailsEl);
  }

  const feedbackRow = document.createElement("div");
  feedbackRow.className = "feedback-row";

  const likeBtn = document.createElement("button");
  likeBtn.className = "feedback-btn";
  likeBtn.textContent = "👍";
  likeBtn.type = "button";

  const dislikeBtn = document.createElement("button");
  dislikeBtn.className = "feedback-btn";
  dislikeBtn.textContent = "👎";
  dislikeBtn.type = "button";

  feedbackRow.appendChild(likeBtn);
  feedbackRow.appendChild(dislikeBtn);
  exchange.appendChild(feedbackRow);

  const commentBox = document.createElement("div");
  commentBox.className = "feedback-comment";
  const commentTextarea = document.createElement("textarea");
  commentTextarea.rows = 2;
  commentTextarea.placeholder = "Optional: tell us what was wrong...";
  const commentSubmit = document.createElement("button");
  commentSubmit.className = "secondary-btn";
  commentSubmit.textContent = "Send feedback";
  commentSubmit.type = "button";
  commentBox.appendChild(commentTextarea);
  commentBox.appendChild(document.createElement("br"));
  commentBox.appendChild(commentSubmit);
  exchange.appendChild(commentBox);

  const sentLabel = document.createElement("div");
  sentLabel.className = "feedback-sent";
  exchange.appendChild(sentLabel);

  async function sendFeedback(rating, comment) {
    try {
      await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, question, answer: data.answer, rating, comment: comment || null }),
      });
      sentLabel.textContent = "Thanks for your feedback!";
    } catch (err) {
      sentLabel.textContent = "Could not send feedback.";
    }
  }

  likeBtn.addEventListener("click", () => {
    likeBtn.classList.add("active-like");
    dislikeBtn.classList.remove("active-dislike");
    commentBox.classList.remove("visible");
    sendFeedback("like", null);
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
}

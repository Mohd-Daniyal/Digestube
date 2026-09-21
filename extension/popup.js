const API_URL = "http://127.0.0.1:5000/summary";
const views = ["home", "loading", "result", "error"];
const el = (id) => document.getElementById(id);

let currentVideoId = null;

function showView(name) {
    for (const v of views) {
        el(`view-${v}`).classList.toggle("hidden", v !== name);
    }
}

function showError(message, action) {
    el("errorMessage").textContent = message;
    el("errorActionLabel").textContent = "Try again";
    el("errorActionBtn").onclick = action;
    showView("error");
}

async function runSummarize() {
    if (!currentVideoId) {
        showError("Open a YouTube video first.", () => showView("home"));
        return;
    }

    showView("loading");
    el("loadingLabel").textContent = "Fetching transcript & summarizing…";

    try {
        const res = await fetch(`${API_URL}?id=${currentVideoId}`);
        const data = await res.json().catch(() => null);

        if (!res.ok) {
            showError(data?.error || `Server error (${res.status}). Is app.py running?`, runSummarize);
            return;
        }

        el("summaryText").textContent = data.summary;
        showView("result");
    } catch (err) {
        showError(
            "Couldn't reach the local server. Make sure app.py is running (python app.py).",
            runSummarize
        );
    }
}

function init() {
    chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
        const isWatchPage = Boolean(tab?.url && tab.url.includes("youtube.com") && tab.url.includes("/watch"));
        if (isWatchPage) {
            currentVideoId = new URL(tab.url).searchParams.get("v");
            el("videoTitle").textContent = tab.title.replace(/ - YouTube$/, "");
        } else {
            el("homeHint").textContent = "Open a YouTube video, then reopen this popup.";
            el("summarizeBtn").disabled = true;
        }
    });

    showView("home");
}

el("summarizeBtn").addEventListener("click", runSummarize);
el("resetBtn").addEventListener("click", () => showView("home"));
el("copyBtn").addEventListener("click", async () => {
    await navigator.clipboard.writeText(el("summaryText").textContent);
    const btn = el("copyBtn");
    const original = btn.textContent;
    btn.textContent = "Copied";
    setTimeout(() => (btn.textContent = original), 1200);
});

init();
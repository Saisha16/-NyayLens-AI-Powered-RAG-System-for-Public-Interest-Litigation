const statusEl = document.getElementById("status");
const newsSelect = document.getElementById("newsSelect");
const topicSelect = document.getElementById("topicSelect");
const excerptEl = document.getElementById("excerpt");
let newsItems = [];

function setStatus(msg, type = "info") {
    statusEl.textContent = msg;
    statusEl.className = `status ${type}`;
}

async function loadTopics() {
    try {
        const res = await fetch("http://localhost:8001/topics");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const topics = data.topics || [];
        topicSelect.innerHTML = "";
        const allOpt = document.createElement("option");
        allOpt.value = "";
        allOpt.textContent = "All topics";
        topicSelect.appendChild(allOpt);
        topics.forEach(t => {
            const opt = document.createElement("option");
            opt.value = t;
            opt.textContent = t.replace(/_/g, " ");
            topicSelect.appendChild(opt);
        });
    } catch (err) {
        console.error("loadTopics error", err);
    }
}

async function loadNews() {
    const topicVal = topicSelect.value || "";
    const topicParam = topicVal ? `?topic=${encodeURIComponent(topicVal)}` : "";
    setStatus("Loading news...", "info");
    try {
        const res = await fetch(`http://localhost:8001/news${topicParam}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        newsItems = data.items || [];

        newsSelect.innerHTML = "";
        newsItems.forEach(item => {
            const opt = document.createElement("option");
            opt.value = item.index;
            opt.textContent = item.title || `Article ${item.index}`;
            newsSelect.appendChild(opt);
        });

        if (newsItems.length === 0) {
            setStatus("No news available. Run ingest or change topic.", "error");
            excerptEl.textContent = "—";
            document.getElementById("summary").textContent = "—";
            return;
        }

        // Auto-load first article
        newsSelect.value = newsItems[0].index;
        setStatus("News loaded. Generating first article...", "info");
        await generatePIL(true, newsItems[0].index);
    } catch (err) {
        console.error("loadNews error", err);
        setStatus("Failed to load news: " + err.message, "error");
    }
}

async function generatePIL(auto = false, idx = null) {
    const selIdx = idx !== null ? idx : Number(newsSelect.value || 0);
    const topicVal = topicSelect.value || "";
    const topicParam = topicVal ? `&topic=${encodeURIComponent(topicVal)}` : "";
    setStatus(auto ? "Loading PIL..." : "Generating PIL...", "info");
    try {
        const response = await fetch(`http://localhost:8001/generate-pil?idx=${selIdx}${topicParam}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        const data = await response.json();

        document.getElementById("newsTitle").innerText = data.news_title || "No title";
        document.getElementById("severityScore").innerText = data.severity_score ?? "—";
        document.getElementById("summary").textContent = data.summary || "—";
        document.getElementById("articleSource").textContent = data.source || "";
        document.getElementById("articleDate").textContent = data.published || "";

        excerptEl.textContent = data.excerpt || "—";
        if (data.news_index !== undefined) {
            newsSelect.value = data.news_index;
        }

        const priority = document.getElementById("priorityLevel");
        priority.innerText = data.priority_level || "—";
        priority.className = data.priority_level || "";

        const entityList = document.getElementById("entityList");
        entityList.innerHTML = "";
        (data.entities_detected || []).forEach(ent => {
            const li = document.createElement("li");
            li.innerText = ent;
            entityList.appendChild(li);
        });

        setStatus("Ready.", "success");
    } catch (err) {
        console.error("generatePIL error", err);
        setStatus("Backend unreachable or error: " + err.message, "error");
    }
}

function downloadPDF() {
    setStatus("Downloading PDF...", "info");
    window.open("http://localhost:8001/download-pil", "_blank");
}

async function addCustomNews() {
    const url = document.getElementById("customUrl").value;
    const title = document.getElementById("customTitle").value || undefined;

    if (!url) {
        setStatus("Please enter a valid URL", "error");
        return;
    }

    setStatus("Adding custom article...", "info");
    try {
        const params = new URLSearchParams();
        params.append("url", url);
        if (title) params.append("title", title);

        const res = await fetch(`http://localhost:8001/add-custom-news?${params}`, { method: "POST" });
        let data;
        try {
            data = await res.json();
        } catch (_) {
            data = { success: false, error: `HTTP ${res.status}` };
        }

        if (data.success) {
            setStatus("Custom article added! Reloading...", "success");
            document.getElementById("customUrl").value = "";
            document.getElementById("customTitle").value = "";
            await loadNews();
        } else {
            setStatus("Failed to add article: " + (data.error || `HTTP ${res.status}`), "error");
        }
    } catch (err) {
        console.error("addCustomNews error", err);
        setStatus("Error adding custom article: " + err.message, "error");
    }
}

window.addEventListener("DOMContentLoaded", () => {
    loadTopics().then(() => loadNews());
    topicSelect.addEventListener("change", () => loadNews());
});

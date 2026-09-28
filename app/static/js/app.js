// Module configuration
const modules = {
    generate: {
        title: "Generate Code",
        desc: "Describe what you need, pick a language, and generate clean code.",
        actionText: "Generate",
        inputLabel: "Requirement",
        inputPlaceholder: "Describe the program you want to build...",
        endpoint: "/generate/",
        responseKey: "code",
        outputKeys: ["explanation"],
    },
    explain: {
        title: "Explain Code",
        desc: "Paste source code and receive a detailed explanation of how it works.",
        actionText: "Explain",
        inputLabel: "Optional Context",
        inputPlaceholder: "Paste the code in the editor and add optional context here...",
        endpoint: "/explain/",
        responseKey: "code",
        outputKeys: ["summary", "functions", "line_by_line", "io_complexity"],
    },
    debug: {
        title: "Debug Code",
        desc: "Paste buggy code and get issue analysis plus corrected code.",
        actionText: "Debug",
        inputLabel: "Error Message (optional)",
        inputPlaceholder: "Paste any error message here, or leave blank...",
        endpoint: "/debug/",
        responseKey: "corrected_code",
        outputKeys: ["issues", "suggestions"],
    },
    optimize: {
        title: "Optimize Code",
        desc: "Paste existing code and get an optimized version with improvements.",
        actionText: "Optimize",
        inputLabel: "Optional Notes",
        inputPlaceholder: "Paste the code in the editor and add optimization notes here...",
        endpoint: "/optimize/",
        responseKey: "optimized_code",
        outputKeys: ["improvements"],
    },
};

let currentModule = "generate";
let editor;

const languageMap = {
    python: "python",
    java: "java",
    c: "c",
    cpp: "cpp",
    javascript: "javascript",
    sql: "sql",
};

// DOM elements
const navBtns = document.querySelectorAll(".nav-btn");
const moduleTitle = document.getElementById("module-title");
const moduleDesc = document.getElementById("module-desc");
const inputLabel = document.getElementById("input-label");
const promptInput = document.getElementById("prompt-input");
const actionBtn = document.getElementById("action-btn");
const actionText = document.getElementById("action-text");
const actionIcon = document.getElementById("action-icon");
const languageSelect = document.getElementById("language");
const outputPanel = document.getElementById("output-panel");
const loading = document.getElementById("loading");
const clearBtn = document.getElementById("clear-btn");
const copyBtn = document.getElementById("copy-btn");
const toastContainer = document.getElementById("toast-container");

// Initialize Monaco editor
require.config({ paths: { vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs" } });
require(["vs/editor/editor.main"], () => {
    editor = monaco.editor.create(document.getElementById("editor"), {
        value: "",
        language: "python",
        theme: "vs-light",
        automaticLayout: true,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        fontSize: 14,
        padding: { top: 16 },
    });
});

// Module switching
function switchModule(name) {
    currentModule = name;
    const config = modules[name];

    moduleTitle.textContent = config.title;
    moduleDesc.textContent = config.desc;
    inputLabel.textContent = config.inputLabel;
    promptInput.placeholder = config.inputPlaceholder;
    actionText.textContent = config.actionText;

    // Update icons
    const icons = {
        generate: "M13 10V3L4 14h7v7l9-11h-7z",
        explain: "M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z",
        debug: "M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
        optimize: "M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z",
    };
    actionIcon.querySelector("path").setAttribute("d", icons[name]);

    navBtns.forEach((btn) => {
        if (btn.dataset.action === name) {
            btn.classList.add("bg-blue-600", "hover:bg-blue-500");
            btn.classList.remove("hover:bg-slate-800");
        } else {
            btn.classList.remove("bg-blue-600", "hover:bg-blue-500");
            btn.classList.add("hover:bg-slate-800");
        }
    });

    outputPanel.innerHTML = "";
}

navBtns.forEach((btn) => {
    btn.addEventListener("click", () => switchModule(btn.dataset.action));
});

// Language change updates Monaco model
languageSelect.addEventListener("change", () => {
    const lang = languageMap[languageSelect.value] || "python";
    if (editor) {
        monaco.editor.setModelLanguage(editor.getModel(), lang);
    }
});

// Clear handler
clearBtn.addEventListener("click", () => {
    promptInput.value = "";
    if (editor) editor.setValue("");
    outputPanel.innerHTML = "";
});

// Copy handler
copyBtn.addEventListener("click", async () => {
    const code = editor ? editor.getValue() : "";
    if (!code.trim()) {
        showToast("Nothing to copy", "error");
        return;
    }
    try {
        await navigator.clipboard.writeText(code);
        showToast("Code copied to clipboard", "success");
    } catch {
        showToast("Failed to copy code", "error");
    }
});

// Build payload based on module
function buildPayload() {
    const language = languageSelect.value;
    const context = promptInput.value.trim();

    switch (currentModule) {
        case "generate":
            return { requirement: context || "No specific requirement provided", language };
        case "explain":
            return { code: editor.getValue(), language };
        case "debug":
            return { code: editor.getValue(), language, error_message: context };
        case "optimize":
            return { code: editor.getValue(), language };
        default:
            return {};
    }
}

// Render output
function renderOutput(data) {
    const config = modules[currentModule];
    const frag = document.createDocumentFragment();

    config.outputKeys.forEach((key) => {
        if (data[key]) {
            const heading = document.createElement("h4");
            heading.className = "text-blue-700 font-semibold capitalize mt-4 mb-1";
            heading.textContent = key.replace(/_/g, " ");

            const content = document.createElement("div");
            content.className = "text-slate-700";
            content.textContent = data[key];

            frag.appendChild(heading);
            frag.appendChild(content);
        }
    });

    outputPanel.innerHTML = "";
    outputPanel.appendChild(frag);
}

// API call
async function handleAction() {
    const config = modules[currentModule];
    const payload = buildPayload();

    // Validation
    if (currentModule === "generate" && !promptInput.value.trim()) {
        showToast("Please enter a requirement", "error");
        return;
    }
    if (["explain", "debug", "optimize"].includes(currentModule) && !editor.getValue().trim()) {
        showToast("Please paste code in the editor", "error");
        return;
    }

    setLoading(true);

    try {
        const response = await fetch(config.endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }

        // Update editor with the main code field when available
        if (data[config.responseKey]) {
            editor.setValue(data[config.responseKey]);
        }

        renderOutput(data);
        showToast(`${config.actionText} completed successfully`, "success");
    } catch (err) {
        console.error(err);
        showToast(err.message || "An error occurred", "error");
        outputPanel.textContent = `Error: ${err.message}`;
    } finally {
        setLoading(false);
    }
}

actionBtn.addEventListener("click", handleAction);

// Loading state
function setLoading(isLoading) {
    if (isLoading) {
        loading.classList.remove("hidden");
        loading.classList.add("flex");
        actionBtn.disabled = true;
        actionBtn.classList.add("opacity-75", "cursor-not-allowed");
    } else {
        loading.classList.add("hidden");
        loading.classList.remove("flex");
        actionBtn.disabled = false;
        actionBtn.classList.remove("opacity-75", "cursor-not-allowed");
    }
}

// Toast notifications
function showToast(message, type = "success") {
    const toast = document.createElement("div");
    const bgClass = type === "success" ? "bg-green-600" : "bg-red-600";
    toast.className = `toast ${bgClass} text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-2 min-w-[240px]`;
    toast.textContent = message;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("hide");
        toast.addEventListener("animationend", () => toast.remove());
    }, 3000);
}

// Initialize
switchModule("generate");

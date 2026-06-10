// Keep track of chart memory instances to prevent rendering overlay bugs
let riskDonutInstance = null;
let riskPieInstance = null;

function renderAnalysisPage(data) {
    const resultsView = document.getElementById("results-view");
    if (resultsView) resultsView.classList.remove("hidden");
    
    document.getElementById("res-contract-name").innerText = (data.contract_name || "DOCUMENT_MANIFEST.PDF").toUpperCase();
    document.getElementById("res-safety-score").innerText = `${data.overall_safety_score}/100`;
    document.getElementById("res-summary").innerText = data.executive_summary;

    // Apply color to overall score threshold matrix values
    const scoreMetric = document.getElementById("res-safety-score");
    if (data.overall_safety_score >= 75) {
        scoreMetric.className = "text-4xl font-black my-3 font-mono text-emerald-400";
    } else if (data.overall_safety_score >= 40) {
        scoreMetric.className = "text-4xl font-black my-3 font-mono text-amber-400";
    } else {
        scoreMetric.className = "text-4xl font-black my-3 font-mono text-red-400";
    }

    // Render strategic action recommendations list
    const tipsContainer = document.getElementById("res-recommendations-list");
    tipsContainer.innerHTML = (data.recommendations || []).map(tip => `
        <li class="flex items-start gap-2 bg-slate-950 p-2 border border-slate-800 my-1 font-mono text-[10px]">
            <span class="text-blue-400 font-bold">»</span>
            <span class="text-slate-300">${tip.toUpperCase()}</span>
        </li>
    `).join("");

    // Initialize counts for chart distribution values
    let criticalCount = 0;
    let cautionCount = 0;
    let standardCount = 0;

    // Render traffic-light clause layouts
    const clausesContainer = document.getElementById("res-clauses-highlight-panel");
    clausesContainer.innerHTML = (data.clauses || []).map(clause => {
        let severityColors = "border-emerald-500/30 bg-emerald-500/5"; 
        let badgeColors = "bg-emerald-500/20 text-emerald-400 border-emerald-500/30";
        
        const normalizedRisk = String(clause.risk_level || "").toLowerCase();
        
        // Traffic Light Mapping Framework Matrix
        if (normalizedRisk.includes("critical") || normalizedRisk.includes("high")) {
            criticalCount++;
            severityColors = "border-red-500/40 bg-red-500/5";
            badgeColors = "bg-red-500/20 text-red-400 border-red-500/30 font-bold";
        } else if (normalizedRisk.includes("caution") || normalizedRisk.includes("warning")) {
            cautionCount++;
            severityColors = "border-amber-500/40 bg-amber-500/5";
            badgeColors = "bg-amber-500/20 text-amber-400 border-amber-500/30 font-bold";
        } else {
            standardCount++;
            severityColors = "border-emerald-500/40 bg-emerald-500/5";
            badgeColors = "bg-emerald-500/20 text-emerald-400 border-emerald-500/30 font-bold";
        }

        return `
            <div class="p-4 border rounded bg-slate-950/40 relative font-mono ${severityColors}">
                <div class="flex justify-between items-center mb-2">
                    <strong class="text-xs font-bold text-slate-200 uppercase tracking-wider">${clause.clause_title}</strong>
                    <span class="px-2 py-0.5 rounded text-[9px] uppercase border ${badgeColors}">${clause.risk_level}</span>
                </div>
                <p class="text-xs italic bg-slate-950 p-2.5 rounded text-slate-400 border border-slate-900 select-all my-2 font-sans">"${clause.extracted_text}"</p>
                <p class="text-xs text-slate-300 leading-relaxed font-sans"><strong class="font-mono text-[10px] text-slate-500 uppercase tracking-wide block mb-0.5">Analysis Metrics Assessment:</strong> ${clause.explanation}</p>
            </div>
        `;
    }).join("");

    // Paint both graphic assets simultaneously
    generateVisualizationCharts(criticalCount, cautionCount, standardCount);
    
    document.getElementById("results-view").scrollIntoView({ behavior: 'smooth' });
}

function generateVisualizationCharts(critical, caution, standard) {
    const donutCtx = document.getElementById('riskDonutChart');
    const pieCtx = document.getElementById('riskPieChart');
    
    if (!donutCtx || !pieCtx) return;

    // Destroy existing canvas contexts to prevent layout flickering during new uploads
    if (riskDonutInstance) riskDonutInstance.destroy();
    if (riskPieInstance) riskPieInstance.destroy();

    // Default safety values if document has clean properties
    if (critical === 0 && caution === 0 && standard === 0) {
        standard = 1;
    }

    const chartDataset = {
        labels: ['CRITICAL', 'CAUTION', 'STANDARD'],
        datasets: [{
            data: [critical, caution, standard],
            backgroundColor: ['rgba(239, 68, 68, 0.15)', 'rgba(245, 158, 11, 0.15)', 'rgba(16, 185, 129, 0.15)'],
            borderColor: ['rgb(239, 68, 68)', 'rgb(245, 158, 11)', 'rgb(16, 185, 129)'],
            borderWidth: 1
        }]
    };

    const displayOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } }
    };

    // 1. Build Donut Instance
    riskDonutInstance = new Chart(donutCtx, {
        type: 'doughnut',
        data: chartDataset,
        options: { ...displayOptions, cutout: '75%' }
    });

    // 2. Build Pie Instance
    riskPieInstance = new Chart(pieCtx, {
        type: 'pie',
        data: chartDataset,
        options: displayOptions
    });
}
// --- PLACE THIS AT THE BASE OF YOUR app.js ---

// 1. Structural View Router State Management
function handleAuth(actionType, email, password) {
    if (email && password) {
        // Toggle high-tech view layouts
        document.getElementById("login-view").classList.add("hidden");
        document.getElementById("dashboard-view").classList.remove("hidden");
        
        // Populate historical sidebars with mock data on entrance initialization
        fetchHistoryLogs();
    } else {
        alert("SECURITY EXCEPTION: Operational credentials required.");
    }
}

function handleLogout() {
    document.getElementById("dashboard-view").classList.add("hidden");
    document.getElementById("login-view").classList.remove("hidden");
}

// Mock historical log system to keep initial render states clean
async function fetchHistoryLogs() {
    try {
        const response = await fetch("http://127.0.0.1:8000/history");
        if (response.ok) {
            const historyData = await response.json();
            document.getElementById("log-count").innerText = historyData.length;
            
            const logContainer = document.getElementById("history-items-list");
            logContainer.innerHTML = historyData.map(item => `
                <div class="p-2 bg-slate-950/60 border border-slate-850 hover:border-slate-700 rounded cursor-pointer transition">
                    <p class="text-[10px] uppercase font-bold tracking-wide text-slate-300 truncate">${item.contract_name}</p>
                    <span class="text-[9px] text-emerald-400 font-mono">Score: ${item.overall_safety_score}/100</span>
                </div>
            `).join("");
        }
    } catch (err) {
        console.error("Historical log fetching interrupted: ", err);
    }
}

// 2. Active File Upload Binary Stream Capture
document.addEventListener("DOMContentLoaded", () => {
    const filePicker = document.getElementById("contract-file-picker");
    
    if (filePicker) {
        filePicker.addEventListener("change", async (event) => {
            const selectedFile = event.target.files[0];
            if (!selectedFile) return;

            // Trigger loading animation feedback tracking layers
            document.getElementById("upload-loading-state").classList.remove("hidden");

            // Build multipart form packet payload stream
            const formPacket = new FormData();
            formPacket.append("file", selectedFile);

            try {
                // Point directly to your active FastAPI multipart handling route
                const targetEndpoint = "http://127.0.0.1:8000/analyze";
                const pipelineResponse = await fetch(targetEndpoint, {
                    method: "POST",
                    body: formPacket // Do NOT set content-type headers manually when passing FormData!
                });

                if (!pipelineResponse.ok) {
                    throw new Error(`Pipeline processing execution failure: Status ${pipelineResponse.status}`);
                }

                const structuredAnalysisResult = await pipelineResponse.json();
                
                // Forward target text output structures straight to the Chart rendering matrices
                renderAnalysisPage(structuredAnalysisResult);

            } catch (pipelineError) {
                console.error("Ingestion processing failure: ", pipelineError);
                alert(`PROCESSING FAILURE: ${pipelineError.message}`);
            } finally {
                // Kill loading loop animation indicators
                document.getElementById("upload-loading-state").classList.add("hidden");
            }
        });
    }
});

// Mock print function layer to keep anchor buttons error-free
function downloadCurrentPDFReport() {
    window.print();
}
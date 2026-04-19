const sourceInput = document.getElementById("sourceInput");
const compileBtn = document.getElementById("compileBtn");
const clearBtn = document.getElementById("clearBtn");
const exampleBtn = document.getElementById("exampleBtn");
const formatBtn = document.getElementById("formatBtn");
const fileUpload = document.getElementById("fileUpload");
const traceMode = document.getElementById("traceMode");
const lineNumbers = document.getElementById("lineNumbers");

const statusBadge = document.getElementById("statusBadge");
const stageBox = document.getElementById("stageBox");
const outputBox = document.getElementById("outputBox");
const errorBox = document.getElementById("errorBox");
const warningBox = document.getElementById("warningBox");
const traceBox = document.getElementById("traceBox");
const symbolBox = document.getElementById("symbolBox");
const tokenBox = document.getElementById("tokenBox");
const astBox = document.getElementById("astBox");
const irBox = document.getElementById("irBox");
const astDiagram = document.getElementById("astDiagram");
const astRawBtn = document.getElementById("astRawBtn");
const astDiagramBtn = document.getElementById("astDiagramBtn");

let currentAstMermaid = "";
let astMode = "raw";

const EXAMPLE_CODE = `int total;
float tax;
total = 100;
tax = total * 0.18;
printf("total=%d", total);
print("tax=", tax);`;

if (window.mermaid) {
  window.mermaid.initialize({ startOnLoad: false, securityLevel: "loose" });
}

function setBadge(label, mode) {
  statusBadge.textContent = label;
  statusBadge.className = `badge ${mode}`;
}

function updateLineNumbers() {
  const lineCount = Math.max(1, (sourceInput.value.match(/\n/g) || []).length + 1);
  const nums = [];
  for (let i = 1; i <= lineCount; i += 1) {
    nums.push(String(i));
  }
  lineNumbers.textContent = nums.join("\n");
}

function resizeEditor() {
  sourceInput.style.height = "auto";
  lineNumbers.style.height = "auto";

  const nextHeight = Math.max(sourceInput.scrollHeight, 420);
  sourceInput.style.height = `${nextHeight}px`;
  lineNumbers.style.height = `${nextHeight}px`;
}

function setEditorValue(value) {
  sourceInput.value = value;
  updateLineNumbers();
  resizeEditor();
  syncLineNumberScroll();
}

function syncLineNumberScroll() {
  lineNumbers.scrollTop = sourceInput.scrollTop;
}

function renderSymbols(symbols) {
  const entries = Object.entries(symbols || {});
  if (!entries.length) {
    return "No symbols declared.";
  }
  return entries.map(([name, type]) => `${name}: ${type}`).join("\n");
}

function renderTokens(tokens) {
  if (!tokens || !tokens.length) {
    return "No tokens.";
  }
  return tokens.map((t) => `${t.type.padEnd(10)} value=${String(t.value)} line=${t.line}`).join("\n");
}

function renderAst(ast) {
  if (!ast || !ast.length) {
    return "No AST generated.";
  }
  return JSON.stringify(ast, null, 2);
}

function renderStages(stages) {
  if (!stages || !stages.length) {
    return "No stage data yet.";
  }

  return stages
    .map((s, i) => `${i + 1}. ${s.name} [${String(s.status).toUpperCase()}]\n   ${s.detail}`)
    .join("\n\n");
}

function renderIr(ir) {
  if (!ir || !ir.length) {
    return "No IR generated.";
  }
  return ir.map((line, idx) => `${idx + 1}. ${line}`).join("\n");
}

function renderWarnings(warnings) {
  if (!warnings || !warnings.length) {
    return "No warnings.";
  }
  return warnings.map((w, i) => `${i + 1}. ${w}`).join("\n");
}

function renderTrace(trace) {
  if (!trace || !trace.length) {
    return "Trace is empty.";
  }
  return trace.map((step, i) => `[Step ${i + 1}] ${step}`).join("\n");
}

async function renderAstDiagram(markup) {
  if (!markup || !window.mermaid) {
    astDiagram.textContent = "No AST diagram available.";
    return;
  }

  try {
    const id = `ast-${Date.now()}`;
    const result = await window.mermaid.render(id, markup);
    astDiagram.innerHTML = result.svg;
  } catch (error) {
    astDiagram.textContent = `Failed to render AST diagram: ${error.message}`;
  }
}

function syncAstMode() {
  const showRaw = astMode === "raw";
  astBox.classList.toggle("hidden", !showRaw);
  astDiagram.classList.toggle("hidden", showRaw);
  astRawBtn.classList.toggle("active", showRaw);
  astDiagramBtn.classList.toggle("active", !showRaw);
}

function renderDiagnostics(diagnostics) {
  if (!diagnostics || !diagnostics.length) {
    return "No errors.";
  }

  return diagnostics
    .map((d, i) => {
      const lineText = d.line ? `Line ${d.line}` : "Unknown line";
      const colText = d.col ? `, Col ${d.col}` : "";
      const codeFrame = d.codeLine
        ? `\nCode: ${d.codeLine}\n      ${d.pointer || "^"}`
        : "";
      return `${i + 1}. [${d.category}] ${lineText}${colText}\nIssue: ${d.message}${codeFrame}\nFix: ${d.hint}`;
    })
    .join("\n\n");
}

function buildOutputSummary(result) {
  const astCount = Array.isArray(result.ast) ? result.ast.length : 0;
  const runtimeEntries = Object.entries(result.runtimeValues || {});
  const runtimeState = runtimeEntries.length
    ? runtimeEntries.map(([k, v]) => `${k} = ${v}`).join("\n")
    : "No tracked variables.";

  if (result.success) {
    const runtimeOutput = (result.output && result.output.length)
      ? result.output.join("\n")
      : "No runtime output.";
    return `Compilation successful.\nStatements parsed: ${astCount}\n\nRuntime Output:\n${runtimeOutput}\n\nFinal Variable Values:\n${runtimeState}`;
  }

  const hints = [...new Set((result.errorDiagnostics || result.diagnostics || []).map((d) => d.hint))];
  const hintBlock = hints.length
    ? hints.map((h, i) => `${i + 1}. ${h}`).join("\n")
    : "1. Check syntax and variable declarations.";

  return `Compilation failed.\nStatements parsed before error: ${astCount}\n\nHow to solve:\n${hintBlock}`;
}

async function renderCompileResult(result) {
  if (result.success) {
    setBadge("Success", "success");
  } else {
    setBadge("Failed", "error");
  }

  stageBox.textContent = renderStages(result.stages || []);
  outputBox.textContent = buildOutputSummary(result);
  errorBox.textContent = renderDiagnostics(result.errorDiagnostics || result.diagnostics || []);
  warningBox.textContent = renderDiagnostics(result.warningDiagnostics || []);
  traceBox.textContent = renderTrace(result.trace || []);

  symbolBox.textContent = renderSymbols(result.symbols);
  tokenBox.textContent = renderTokens(result.tokens);
  astBox.textContent = renderAst(result.ast);
  irBox.textContent = renderIr(result.ir);

  currentAstMermaid = result.astMermaid || "";
  await renderAstDiagram(currentAstMermaid);
  syncAstMode();
}

async function compileSource() {
  const source = sourceInput.value;
  if (!source.trim()) {
    setBadge("No Code", "error");
    errorBox.textContent = "Please type code or upload a file first.";
    return;
  }

  setBadge("Compiling", "idle");

  try {
    const response = await fetch("/api/compile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ source, trace: traceMode.checked }),
    });

    const result = await response.json();

    if (!response.ok) {
      setBadge("Failed", "error");
      errorBox.textContent = (result.errors || ["Compile request failed."]).join("\n");
      return;
    }

    await renderCompileResult(result);
  } catch (error) {
    setBadge("Failed", "error");
    errorBox.textContent = `Request error: ${error.message}`;
  }
}

async function formatSource() {
  const source = sourceInput.value;
  if (!source.trim()) {
    return;
  }

  try {
    const response = await fetch("/api/format", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ source }),
    });

    const result = await response.json();
    if (response.ok && result.formatted) {
      setEditorValue(result.formatted);
    }
  } catch (error) {
    errorBox.textContent = `Format error: ${error.message}`;
  }
}

compileBtn.addEventListener("click", compileSource);
formatBtn.addEventListener("click", formatSource);

sourceInput.addEventListener("input", updateLineNumbers);
sourceInput.addEventListener("scroll", syncLineNumberScroll);
sourceInput.addEventListener("input", () => {
  updateLineNumbers();
  resizeEditor();
});
sourceInput.addEventListener("keyup", () => {
  updateLineNumbers();
  resizeEditor();
});
sourceInput.addEventListener("change", () => {
  updateLineNumbers();
  resizeEditor();
});
sourceInput.addEventListener("paste", () => setTimeout(() => {
  updateLineNumbers();
  resizeEditor();
}, 0));
sourceInput.addEventListener("cut", () => setTimeout(() => {
  updateLineNumbers();
  resizeEditor();
}, 0));
sourceInput.addEventListener("drop", () => setTimeout(() => {
  updateLineNumbers();
  resizeEditor();
}, 0));

clearBtn.addEventListener("click", () => {
  setEditorValue("");
  setBadge("Idle", "idle");
  stageBox.textContent = "No stage data yet.";
  outputBox.textContent = "No output yet.";
  errorBox.textContent = "No errors.";
  warningBox.textContent = "No warnings.";
  traceBox.textContent = "Trace is empty.";
  symbolBox.textContent = "No symbols yet.";
  tokenBox.textContent = "No tokens yet.";
  astBox.textContent = "No AST yet.";
  irBox.textContent = "No IR yet.";
  astDiagram.textContent = "No AST diagram yet.";
  currentAstMermaid = "";
  astMode = "raw";
  syncAstMode();
});

exampleBtn.addEventListener("click", () => {
  setEditorValue(EXAMPLE_CODE);
});

fileUpload.addEventListener("change", (event) => {
  const file = event.target.files && event.target.files[0];
  if (!file) {
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    setEditorValue(String(e.target.result || ""));
  };
  reader.readAsText(file);
});

astRawBtn.addEventListener("click", () => {
  astMode = "raw";
  syncAstMode();
});

astDiagramBtn.addEventListener("click", async () => {
  astMode = "diagram";
  syncAstMode();
  await renderAstDiagram(currentAstMermaid);
});

updateLineNumbers();
resizeEditor();

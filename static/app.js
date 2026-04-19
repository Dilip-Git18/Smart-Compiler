const sourceInput = document.getElementById("sourceInput");
const compileBtn = document.getElementById("compileBtn");
const clearBtn = document.getElementById("clearBtn");
const exampleBtn = document.getElementById("exampleBtn");
const fileUpload = document.getElementById("fileUpload");

const statusBadge = document.getElementById("statusBadge");
const outputBox = document.getElementById("outputBox");
const errorBox = document.getElementById("errorBox");
const symbolBox = document.getElementById("symbolBox");
const tokenBox = document.getElementById("tokenBox");
const astBox = document.getElementById("astBox");

const EXAMPLE_CODE = `int total;
float tax;
total = 100;
tax = total * 0.18;
printf("total=%d", total);
print(tax);`;

function setBadge(label, mode) {
  statusBadge.textContent = label;
  statusBadge.className = `badge ${mode}`;
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

function renderDiagnostics(diagnostics) {
  if (!diagnostics || !diagnostics.length) {
    return "No errors.";
  }

  return diagnostics
    .map((d, i) => {
      const lineText = d.line ? `Line ${d.line}` : "Unknown line";
      return `${i + 1}. [${d.category}] ${lineText}\nIssue: ${d.message}\nFix: ${d.hint}`;
    })
    .join("\n\n");
}

function buildOutputSummary(result) {
  const astCount = Array.isArray(result.ast) ? result.ast.length : 0;

  if (result.success) {
    const runtimeOutput = (result.output && result.output.length)
      ? result.output.join("\n")
      : "No runtime output.";
    return `Compilation successful.\nStatements parsed: ${astCount}\n\nRuntime Output:\n${runtimeOutput}`;
  }

  const hints = [...new Set((result.diagnostics || []).map((d) => d.hint))];
  const hintBlock = hints.length
    ? hints.map((h, i) => `${i + 1}. ${h}`).join("\n")
    : "1. Check syntax and variable declarations.";

  return `Compilation failed.\nStatements parsed before error: ${astCount}\n\nHow to solve:\n${hintBlock}`;
}

function renderCompileResult(result) {
  if (result.success) {
    setBadge("Success", "success");
  } else {
    setBadge("Failed", "error");
  }

  outputBox.textContent = buildOutputSummary(result);
  errorBox.textContent = renderDiagnostics(result.diagnostics || []);

  symbolBox.textContent = renderSymbols(result.symbols);
  tokenBox.textContent = renderTokens(result.tokens);
  astBox.textContent = renderAst(result.ast);
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
      body: JSON.stringify({ source }),
    });

    const result = await response.json();

    if (!response.ok) {
      setBadge("Failed", "error");
      errorBox.textContent = (result.errors || ["Compile request failed."]).join("\n");
      return;
    }

    renderCompileResult(result);
  } catch (error) {
    setBadge("Failed", "error");
    errorBox.textContent = `Request error: ${error.message}`;
  }
}

compileBtn.addEventListener("click", compileSource);

clearBtn.addEventListener("click", () => {
  sourceInput.value = "";
  setBadge("Idle", "idle");
  outputBox.textContent = "No output yet.";
  errorBox.textContent = "No errors.";
  symbolBox.textContent = "No symbols yet.";
  tokenBox.textContent = "No tokens yet.";
  astBox.textContent = "No AST yet.";
});

exampleBtn.addEventListener("click", () => {
  sourceInput.value = EXAMPLE_CODE;
});

fileUpload.addEventListener("change", (event) => {
  const file = event.target.files && event.target.files[0];
  if (!file) {
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    sourceInput.value = String(e.target.result || "");
  };
  reader.readAsText(file);
});

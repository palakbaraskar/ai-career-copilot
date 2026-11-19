/**
 * AI Career Co-Pilot - Client Controller
 * Handles client-side state, API calls, file uploads, and dynamic DOM rendering.
 */

// ── Sample Demonstration Data ────────────────────────────────────────────────
const SAMPLE_RESUME = `ALEX CHEN
Full-Stack Software Engineer | San Francisco, CA | alex.chen@email.com | github.com/alexchen | linkedin.com/in/alexchen

SUMMARY:
Results-driven Software Engineer with 3+ years of experience designing scalable web services, microservices, and reactive user interfaces. Proficient in Python, JavaScript/TypeScript, React, Flask, Node.js, and PostgreSQL. Experienced in Docker containerization, RESTful API architecture, and CI/CD pipelines.

TECHNICAL SKILLS:
- Languages: Python, JavaScript (ES6+), TypeScript, SQL, HTML5, CSS3
- Frameworks & Libraries: React, Flask, Express.js, Redux, Tailwind CSS, Jest
- Databases & Tools: PostgreSQL, MongoDB, Redis, Docker, Git, AWS (S3, EC2), Postman

PROFESSIONAL EXPERIENCE:
Software Engineer | CloudScale Tech (2022 - Present)
- Developed and maintained 15+ RESTful microservices using Python Flask and PostgreSQL, serving 120,000+ daily active users.
- Redesigned user onboarding flow with React and Redux, improving user conversion rate by 24%.
- Optimized complex SQL queries and introduced Redis caching, reducing average API response latency by 42%.
- Collaborated in an agile team of 8 engineers, conducting code reviews and maintaining 85%+ unit test coverage.

Junior Web Developer | Innovate Labs (2021 - 2022)
- Built interactive customer dashboards using React, CSS Modules, and Node.js.
- Integrated Stripe payment processing API with webhooks, securely processing $250k+ in quarterly subscriptions.
- Automated deployment scripts with GitHub Actions, cutting staging release times by 30%.

EDUCATION:
Bachelor of Science in Computer Science | University of California (2017 - 2021)
- GPA: 3.8/4.0, Dean's Honors List
- Relevant Coursework: Data Structures & Algorithms, Distributed Systems, Database Management.`;

const SAMPLE_JOB_DESC = `Senior Full-Stack Engineer (Python / React)
Company: NextWave AI Platform
Location: Remote (US)

About the Role:
We are looking for a Senior Full-Stack Engineer to architect and build our next-generation AI-powered enterprise applications. You will be responsible for end-to-end feature delivery, designing robust backend APIs, and crafting intuitive, responsive frontends.

Responsibilities:
- Architect and develop high-throughput APIs using Python (FastAPI/Flask) and event-driven architecture.
- Build clean, performant React/TypeScript user interfaces with modern state management.
- Design database schemas and optimize query execution on PostgreSQL and Redis.
- Collaborate with AI/ML engineers to integrate LLM endpoints (Gemini / OpenAI) into production workflows.
- Implement automated testing, CI/CD pipelines, and infrastructure as code using Docker and Kubernetes.

Requirements:
- 3+ years of professional full-stack development experience.
- Strong proficiency in Python and modern JavaScript/TypeScript.
- Hands-on experience with React, state management, and modern component architecture.
- Demonstrated experience with relational databases (PostgreSQL), schema design, and caching strategies (Redis).
- Experience deploying microservices with Docker; familiarity with Kubernetes or AWS is a strong plus.
- Excellent communication and collaboration skills in a remote, fast-paced environment.`;

// ── Global Toast Utility ─────────────────────────────────────────────────────
function showToast(message, type = "info") {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `toast ${type === "error" ? "toast-error" : "toast-success"}`;
    
    const icon = type === "error" ? "fa-circle-exclamation" : "fa-circle-check";
    toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
    
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ── DOM Initializer ──────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    initResumeAnalyzer();
    initJobMatcher();
    initInterviewPrep();
});

// ══════════════════════════════════════════════════════════════════════════════
// PROJECT 1: RESUME ATS ANALYZER
// ══════════════════════════════════════════════════════════════════════════════
function initResumeAnalyzer() {
    const resumeForm = document.getElementById("resume-form");
    if (!resumeForm) return;

    // Tabs Switcher (Upload vs Paste)
    const tabButtons = document.querySelectorAll(".input-tabs .tab-btn");
    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            tabButtons.forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
            
            btn.classList.add("active");
            const targetId = btn.getAttribute("data-tab");
            document.getElementById(targetId)?.classList.add("active");
        });
    });

    // File Drag & Drop Setup
    const dropzone = document.getElementById("resume-dropzone");
    const fileInput = document.getElementById("resume-file");
    const selectedInfo = document.getElementById("selected-file-info");
    const fileNameDisplay = document.getElementById("file-name-display");
    const removeFileBtn = document.getElementById("remove-file-btn");

    if (dropzone && fileInput) {
        dropzone.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropzone.classList.add("dragover");
        });

        dropzone.addEventListener("dragleave", () => {
            dropzone.classList.remove("dragover");
        });

        dropzone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropzone.classList.remove("dragover");
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updateFileDisplay();
            }
        });

        fileInput.addEventListener("change", updateFileDisplay);

        removeFileBtn?.addEventListener("click", (e) => {
            e.stopPropagation();
            fileInput.value = "";
            selectedInfo.classList.add("hidden");
            dropzone.querySelector(".dropzone-inner").classList.remove("hidden");
        });
    }

    function updateFileDisplay() {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            fileNameDisplay.textContent = file.name;
            dropzone.querySelector(".dropzone-inner").classList.add("hidden");
            selectedInfo.classList.remove("hidden");
        }
    }

    // Load Sample Resume Button
    const sampleBtn = document.getElementById("load-sample-resume-btn");
    if (sampleBtn) {
        sampleBtn.addEventListener("click", () => {
            // Switch to Paste tab
            const pasteTabBtn = document.querySelector('[data-tab="paste-tab"]');
            pasteTabBtn?.click();
            const textarea = document.getElementById("resume-text");
            if (textarea) textarea.value = SAMPLE_RESUME;
            showToast("Sample candidate resume loaded!", "success");
        });
    }

    // Form Submission
    resumeForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData();
        const activeTab = document.querySelector(".tab-content.active")?.id;

        if (activeTab === "upload-tab") {
            if (!fileInput.files.length) {
                showToast("Please choose or drop a resume PDF file first.", "error");
                return;
            }
            formData.append("file", fileInput.files[0]);
        } else {
            const textVal = document.getElementById("resume-text")?.value.trim();
            if (!textVal) {
                showToast("Please paste your resume text.", "error");
                return;
            }
            formData.append("text", textVal);
        }

        // Toggle UI State to Loading
        setResumeState("loading");

        try {
            const res = await fetch("/api/analyze-resume", {
                method: "POST",
                body: formData
            });

            let data;
            try {
                data = await res.json();
            } catch (err) {
                throw new Error("Server response format error. Please refresh and retry.");
            }

            if (!res.ok || data.error) {
                throw new Error(data.error || "Analysis failed");
            }

            renderResumeResults(data);
            setResumeState("results");
            showToast("Resume ATS analysis completed!", "success");
        } catch (err) {
            console.error(err);
            setResumeState("initial");
            showToast(err.message, "error");
        }
    });

    function setResumeState(state) {
        const initialEl = document.getElementById("initial-state");
        const loadingEl = document.getElementById("loading-state");
        const contentEl = document.getElementById("analysis-content");
        const submitBtn = document.getElementById("analyze-resume-btn");

        initialEl?.classList.toggle("hidden", state !== "initial");
        loadingEl?.classList.toggle("hidden", state !== "loading");
        contentEl?.classList.toggle("hidden", state !== "results");

        if (submitBtn) {
            submitBtn.disabled = state === "loading";
            submitBtn.innerHTML = state === "loading"
                ? `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing with Gemini...`
                : `<i class="fa-solid fa-sparkles"></i> Run Gemini ATS Audit`;
        }
    }

    function renderResumeResults(data) {
        // Overall ATS Score
        const scoreVal = document.getElementById("ats-score-value");
        if (scoreVal) scoreVal.textContent = data.ats_score || 0;

        // Elevator Pitch & Summary
        document.getElementById("candidate-pitch").textContent = data.one_liner_pitch || "";
        document.getElementById("candidate-summary").textContent = data.summary || "";

        // Section Breakdown
        const sections = data.section_scores || {};
        updateBar("bar-exp", "bar-exp-val", sections.experience || 75);
        updateBar("bar-skills", "bar-skills-val", sections.skills || 80);
        updateBar("bar-edu", "bar-edu-val", sections.education || 85);
        updateBar("bar-format", "bar-format-val", sections.formatting || 70);

        // Best-fit Roles
        const rolesContainer = document.getElementById("top-roles-container");
        rolesContainer.innerHTML = "";
        (data.top_roles || []).forEach(role => {
            const span = document.createElement("span");
            span.className = "role-pill";
            span.textContent = role;
            rolesContainer.appendChild(span);
        });

        // Strengths & Weaknesses
        populateList("strengths-list", data.strengths || []);
        populateList("weaknesses-list", data.weaknesses || []);

        // Keywords to Add
        const kwContainer = document.getElementById("keywords-container");
        kwContainer.innerHTML = "";
        (data.keywords_missing || []).forEach(kw => {
            const span = document.createElement("span");
            span.className = "tag-pill";
            span.textContent = `+ ${kw}`;
            kwContainer.appendChild(span);
        });

        // Improvements
        const impContainer = document.getElementById("improvements-container");
        impContainer.innerHTML = "";
        (data.improvements || []).forEach(imp => {
            const div = document.createElement("div");
            div.className = "improvement-item";
            div.innerHTML = `<i class="fa-solid fa-angle-right"></i> ${imp}`;
            impContainer.appendChild(div);
        });
    }

    function updateBar(barId, valId, score) {
        const bar = document.getElementById(barId);
        const val = document.getElementById(valId);
        if (bar) bar.style.width = `${score}%`;
        if (val) val.textContent = `${score}%`;
    }

    function populateList(id, items) {
        const el = document.getElementById(id);
        if (!el) return;
        el.innerHTML = "";
        items.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            el.appendChild(li);
        });
    }
}

// ══════════════════════════════════════════════════════════════════════════════
// PROJECT 2: SMART JOB MATCHER & GAP ANALYZER
// ══════════════════════════════════════════════════════════════════════════════
function initJobMatcher() {
    const matchForm = document.getElementById("job-match-form");
    if (!matchForm) return;

    // Load Sample Button
    const sampleBtn = document.getElementById("load-sample-match-btn");
    if (sampleBtn) {
        sampleBtn.addEventListener("click", () => {
            const resInput = document.getElementById("match-resume-text");
            const jdInput = document.getElementById("match-job-desc");
            if (resInput) resInput.value = SAMPLE_RESUME;
            if (jdInput) jdInput.value = SAMPLE_JOB_DESC;
            showToast("Sample Resume and Job Description loaded!", "success");
        });
    }

    // Copy Summary Button
    const copyBtn = document.getElementById("copy-summary-btn");
    if (copyBtn) {
        copyBtn.addEventListener("click", () => {
            const summaryText = document.getElementById("tailored-summary-content")?.innerText;
            if (summaryText) {
                navigator.clipboard.writeText(summaryText);
                showToast("Tailored summary copied to clipboard!", "success");
            }
        });
    }

    matchForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const resume = document.getElementById("match-resume-text")?.value.trim();
        const jd = document.getElementById("match-job-desc")?.value.trim();

        if (!resume || !jd) {
            showToast("Please provide both your resume and target job description.", "error");
            return;
        }

        setMatchState("loading");

        try {
            const res = await fetch("/api/match-job", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ resume, job_description: jd })
            });

            let data;
            try {
                data = await res.json();
            } catch (err) {
                throw new Error("Server response format error. Please refresh and retry.");
            }

            if (!res.ok || data.error) {
                throw new Error(data.error || "Job match failed");
            }

            renderMatchResults(data);
            setMatchState("results");
            showToast("Job compatibility & gap analysis ready!", "success");
        } catch (err) {
            console.error(err);
            setMatchState("initial");
            showToast(err.message, "error");
        }
    });

    function setMatchState(state) {
        const initialEl = document.getElementById("match-initial-state");
        const loadingEl = document.getElementById("match-loading-state");
        const contentEl = document.getElementById("match-content");
        const submitBtn = document.getElementById("run-match-btn");

        initialEl?.classList.toggle("hidden", state !== "initial");
        loadingEl?.classList.toggle("hidden", state !== "loading");
        contentEl?.classList.toggle("hidden", state !== "results");

        if (submitBtn) {
            submitBtn.disabled = state === "loading";
            submitBtn.innerHTML = state === "loading"
                ? `<i class="fa-solid fa-spinner fa-spin"></i> Cross-referencing with Gemini...`
                : `<i class="fa-solid fa-crosshairs"></i> Run Semantic Gap Analysis`;
        }
    }

    function renderMatchResults(data) {
        // Score & Verdict
        const scoreVal = document.getElementById("match-score-val");
        if (scoreVal) scoreVal.textContent = `${data.match_score || 0}%`;

        document.getElementById("match-verdict-pill").textContent = data.verdict || "Match";
        document.getElementById("experience-match-pill").textContent = data.experience_match || "Meets Requirements";
        document.getElementById("match-verdict-reason").textContent = data.verdict_reason || "";
        document.getElementById("salary-range-display").textContent = data.salary_range || "$100,000 - $140,000";

        // Matched vs Missing Skills
        populateTags("matched-skills-container", data.matched_skills || []);
        populateTags("missing-skills-container", data.missing_skills || []);

        // Tailored Summary
        document.getElementById("tailored-summary-content").textContent = data.tailored_summary || "";

        // Learning Roadmap
        const roadmapEl = document.getElementById("roadmap-container");
        roadmapEl.innerHTML = "";
        (data.learning_roadmap || []).forEach((step, idx) => {
            const div = document.createElement("div");
            div.className = "roadmap-step";
            div.innerHTML = `
                <div class="roadmap-step-left">
                    <span class="roadmap-num">${idx + 1}</span>
                    <div class="roadmap-step-info">
                        <strong>${step.skill}</strong>
                        <span>${step.resource}</span>
                    </div>
                </div>
                <span class="roadmap-time-badge"><i class="fa-regular fa-clock"></i> ${step.time}</span>
            `;
            roadmapEl.appendChild(div);
        });

        // Insider Interview Tip
        document.getElementById("interview-tip-text").textContent = data.interview_tip || "";
    }

    function populateTags(containerId, items) {
        const container = document.getElementById(containerId);
        if (!container) return;
        container.innerHTML = "";
        items.forEach(item => {
            const span = document.createElement("span");
            span.className = "tag-pill";
            span.textContent = item;
            container.appendChild(span);
        });
    }
}

// ══════════════════════════════════════════════════════════════════════════════
// PROJECT 3: AI INTERVIEW PREP LAB
// ══════════════════════════════════════════════════════════════════════════════
function initInterviewPrep() {
    const setupForm = document.getElementById("generate-questions-form");
    if (!setupForm) return;

    let activeQuestions = [];
    let currentQuestion = null;
    let targetRole = "";

    // Load Sample Button
    const sampleBtn = document.getElementById("load-sample-role-btn");
    if (sampleBtn) {
        sampleBtn.addEventListener("click", () => {
            document.getElementById("prep-job-title").value = "Full-Stack Software Engineer (Python / React)";
            document.getElementById("prep-job-desc").value = SAMPLE_JOB_DESC.slice(0, 350) + "...";
            document.getElementById("prep-resume").value = "3 years building Flask microservices, React UIs, and PostgreSQL databases.";
            showToast("Sample engineering role filled!", "success");
        });
    }

    // Step 1: Generate Questions
    setupForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const jobTitle = document.getElementById("prep-job-title")?.value.trim();
        const jobDesc = document.getElementById("prep-job-desc")?.value.trim();
        const resume = document.getElementById("prep-resume")?.value.trim();

        if (!jobTitle) {
            showToast("Please provide at least a Target Job Title.", "error");
            return;
        }

        targetRole = jobTitle;
        const generateBtn = document.getElementById("generate-questions-btn");
        generateBtn.disabled = true;
        generateBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Generating Session with Gemini...`;

        try {
            const res = await fetch("/api/generate-questions", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    job_title: jobTitle,
                    job_description: jobDesc,
                    resume: resume
                })
            });

            let data;
            try {
                data = await res.json();
            } catch (err) {
                throw new Error("Server response format error. Please refresh and retry.");
            }

            if (!res.ok || data.error) {
                throw new Error(data.error || "Failed to generate questions");
            }

            activeQuestions = data.questions || [];
            document.getElementById("interviewer-intro-text").textContent = `"${data.intro || 'Welcome to your interview simulation round.'}"`;
            renderQuestionsBank(activeQuestions);

            document.getElementById("interview-session-container")?.classList.remove("hidden");
            document.getElementById("interview-session-container")?.scrollIntoView({ behavior: "smooth" });
            showToast(`Generated ${activeQuestions.length} interview questions!`, "success");
        } catch (err) {
            console.error(err);
            showToast(err.message, "error");
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = `<i class="fa-solid fa-sparkles"></i> Generate AI Mock Interview Session`;
        }
    });

    function renderQuestionsBank(questions) {
        const listEl = document.getElementById("questions-list");
        const countEl = document.getElementById("question-count");
        if (countEl) countEl.textContent = questions.length;
        if (!listEl) return;

        listEl.innerHTML = "";

        questions.forEach((q, idx) => {
            const item = document.createElement("div");
            item.className = "question-item";
            item.setAttribute("data-id", q.id);
            item.innerHTML = `
                <div class="q-meta">
                    <span class="q-category">${q.category}</span>
                    <span class="q-difficulty">${q.difficulty}</span>
                </div>
                <div class="q-title">${idx + 1}. ${q.question}</div>
            `;

            item.addEventListener("click", () => selectQuestion(q, item));
            listEl.appendChild(item);
        });

        // Automatically select first question
        if (questions.length > 0) {
            selectQuestion(questions[0], listEl.children[0]);
        }
    }

    function selectQuestion(q, element) {
        currentQuestion = q;

        // Highlight in list
        document.querySelectorAll(".question-item").forEach(el => el.classList.remove("active"));
        element?.classList.add("active");

        // Update Answer Studio
        document.getElementById("active-question-category").textContent = `${q.category} (${q.difficulty})`;
        document.getElementById("current-question-text").textContent = q.question;

        const hintContainer = document.getElementById("current-question-hint");
        const hintText = document.getElementById("hint-text");
        if (q.hint) {
            hintText.textContent = q.hint;
            hintContainer.classList.remove("hidden");
        } else {
            hintContainer.classList.add("hidden");
        }

        // Reset answer field & evaluation
        document.getElementById("candidate-answer-input").value = "";
        document.getElementById("evaluate-answer-btn").disabled = false;
        document.getElementById("evaluation-result")?.classList.add("hidden");
    }

    // Step 2: Evaluate Answer Form
    const answerForm = document.getElementById("submit-answer-form");
    if (answerForm) {
        answerForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            if (!currentQuestion) {
                showToast("Please choose an interview question first.", "error");
                return;
            }

            const answer = document.getElementById("candidate-answer-input")?.value.trim();
            if (!answer || answer.length < 15) {
                showToast("Please provide a more complete answer (at least 2-3 sentences).", "error");
                return;
            }

            const evalBtn = document.getElementById("evaluate-answer-btn");
            const loadingEl = document.getElementById("eval-loading");
            const resultEl = document.getElementById("evaluation-result");

            evalBtn.disabled = true;
            loadingEl.classList.remove("hidden");
            resultEl.classList.add("hidden");

            try {
                const res = await fetch("/api/evaluate-answer", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        job_title: targetRole,
                        question: currentQuestion.question,
                        category: currentQuestion.category,
                        answer: answer
                    })
                });

                const data = await res.json();
                if (!res.ok || data.error) {
                    throw new Error(data.error || "Evaluation failed");
                }

                renderEvaluation(data);
                resultEl.classList.remove("hidden");
                showToast("Response evaluated!", "success");
            } catch (err) {
                console.error(err);
                showToast(err.message, "error");
            } finally {
                evalBtn.disabled = false;
                loadingEl.classList.add("hidden");
            }
        });
    }

    function renderEvaluation(data) {
        document.getElementById("eval-score-num").textContent = data.score ?? 0;
        document.getElementById("eval-grade-badge").textContent = data.grade || "Evaluated";
        document.getElementById("eval-feedback-text").textContent = data.feedback || "";

        // STAR breakdown
        const star = data.star_analysis || {};
        document.getElementById("star-situation").textContent = star.situation || "N/A";
        document.getElementById("star-task").textContent = star.task || "N/A";
        document.getElementById("star-action").textContent = star.action || "N/A";
        document.getElementById("star-result").textContent = star.result || "N/A";

        // Strengths & Improvements
        populateEvalList("eval-strengths", data.what_worked || []);
        populateEvalList("eval-improvements", data.what_to_improve || []);

        // Ideal Answer Model
        document.getElementById("ideal-answer-text").textContent = data.ideal_answer_outline || "";

        // Follow up probe
        document.getElementById("follow-up-text").textContent = data.follow_up_question || "Can you expand further on this experience?";
    }

    function populateEvalList(id, items) {
        const el = document.getElementById(id);
        if (!el) return;
        el.innerHTML = "";
        items.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            el.appendChild(li);
        });
    }
}

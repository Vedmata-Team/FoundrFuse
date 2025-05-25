

    // Toggle Founder/Investor View
    const founderBtn = document.getElementById("founderBtn");
    const investorBtn = document.getElementById("investorBtn");
    const founderVisual = document.getElementById("founderVisual");
    const investorVisual = document.getElementById("investorVisual");
    const userTypeField = document.getElementById("id_user_type");
    const startupDateField = document.getElementById("startupDateField");
    const investorQuestions = document.getElementById("investorQuestions");

    founderBtn.addEventListener("click", () => {
        founderBtn.classList.add("active");
        investorBtn.classList.remove("active");
        founderVisual.style.display = "block";
        investorVisual.style.display = "none";
        startupDateField.style.display = "block";
        investorQuestions.style.display = "none";
        userTypeField.value = "founder";
    });

    investorBtn.addEventListener("click", () => {
        investorBtn.classList.add("active");
        founderBtn.classList.remove("active");
        founderVisual.style.display = "none";
        investorVisual.style.display = "block";
        startupDateField.style.display = "none";
        investorQuestions.style.display = "block";
        userTypeField.value = "investor";
    });

    // Show/hide "Other" field based on selection
    function toggleOtherFocus() {
        const select = document.getElementById("id_investment_focus_select");
        const otherContainer = document.getElementById("otherFocusContainer");
        if (select.value === "Other") {
            otherContainer.style.display = "block";
        } else {
            otherContainer.style.display = "none";
        }
    }

    // Update investment range display
    function updateRangeDisplay(value) {
        const display = document.getElementById("rangeDisplay");
        const formatted = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(value);
        display.textContent = formatted.replace('₹', '₹ ');
    }

    // Progress Bar
    const form = document.getElementById("registerForm");
    const progressBar = document.getElementById("registerProgress");
    const inputs = form.querySelectorAll("input, select");

    function updateProgress() {
        let filled = 0;
        inputs.forEach(input => {
            if ((input.type !== "hidden") && input.offsetParent !== null && input.value.trim() !== "") {
                filled += 1;
            }
        });
        const totalVisible = Array.from(inputs).filter(input => input.offsetParent !== null && input.type !== "hidden").length;
        const progress = Math.round((filled / totalVisible) * 100);
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute("aria-valuenow", progress);
        progressBar.textContent = `${progress}%`;
    }

    inputs.forEach(input => {
        input.addEventListener("input", updateProgress);
        input.addEventListener("change", updateProgress);
    });

    document.addEventListener("DOMContentLoaded", updateProgress);


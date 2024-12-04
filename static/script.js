const inputField = document.getElementById("input-link");
const spinner = document.getElementById("loading-spinner");

document.getElementById("submit-button").addEventListener("click", async () => {
    const url = inputField.value.trim();
    const summaryBox = document.getElementById("summary-box");

    if (!url) {
        alertInputField();
        return;
    }

    toggleSpinner("block"); // Show spinner

    try {
        // Send request to backend
        const response = await fetch('http://127.0.0.1:8000/summarize-video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ youtube_link: url }),
        });

        const data = await response.json();
        toggleSpinner("none"); // Hide spinner

        if (response.ok) {
            // Update the summary box with the generated summary
            summaryBox.innerHTML = data.summary;
        } else {
            alertInputField();
            showToast(`Error: ${data.detail}`);
        }
    } 
    catch (error) {
        toggleSpinner("none");
        alertInputField();
        showToast(`Error: ${error.message}`);
    }
});

// Functions for Visual Feedback 
function showToast(message) {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 10000); // Toast disappears after 3 seconds
}

function toggleSpinner(display_type){
    spinner.style.display = display_type;
}

function alertInputField(){
    inputField.classList.add("input-error");
    setTimeout(() => inputField.classList.remove("input-error"), 1000);
}
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
            showToast(`Error: ${data.detail}`, 0);
        }
    } 
    catch (error) {
        toggleSpinner("none");
        alertInputField();
        showToast(`Error: ${error.message}`, 0);
    }
});

document.getElementById('summary-box').addEventListener('click', function () {
    // Select the content inside the summary-box
    let summaryContent = document.getElementById('summary-box');

    // Use the Clipboard API to copy the text
    navigator.clipboard.writeText(summaryContent.innerText)
        .then(function() {
            // Optionally, show a toast or alert to notify the user
            showToast('Summary copied to clipboard!', 1);
        })
        .catch(function(err) {
            // Handle error if copying fails
            showToast(err, 0);
        });
});

// Functions for Visual Feedback 
function showToast(message, message_type) {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.classList.add("show");
    let toast_duration = 3000;

    if (message_type == 1){
        toast.style.backgroundColor = "rgba(61, 227, 150, 0.8)";
    }
    else {
        toast.style.backgroundColor = "rgba(255, 0, 0, 0.8)";
    }

    setTimeout(() => {
        toast.classList.remove("show");
    }, toast_duration); 
}

function toggleSpinner(display_type){
    spinner.style.display = display_type;
}

function alertInputField(){
    inputField.classList.add("input-error");
    setTimeout(() => inputField.classList.remove("input-error"), 1000);
}
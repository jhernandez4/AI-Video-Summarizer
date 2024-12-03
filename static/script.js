document.getElementById("submit-button").addEventListener("click", async () => {
    const url = document.getElementById("input-link").value;
    const summaryBox = document.getElementById("summary-box");
    const spinner = document.getElementById("loading-spinner");

    if (!url) {
        alert('Please enter a YouTube link');
        return;
    }

    spinner.style.display = "block"; // Show the spinner

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
        spinner.style.display = "none"; // Hide the spinner

        if (response.ok) {
            // Update the summary box with the generated summary
            summaryBox.innerHTML = data.summary;
        } else {
            // Show error details in the summary box
            summaryBox.innerHTML = `Error: ${data.detail}`;
        }
    } 
    catch (error) {
        spinner.style.display = "none"; // Hide the spinner
        summaryBox.innerHTML = `Error: ${error.message}`;
    }
});
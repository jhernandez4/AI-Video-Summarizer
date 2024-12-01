document.getElementById("submit-button").addEventListener("click", async () => {
    const url = document.getElementById("input-link").value;
    const summaryBox = document.getElementById("summary-box");

    if (!url) {
        alert('Please enter a YouTube link');
        return;
    }

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

        if (response.ok) {
            // Update the summary box with the generated summary
            summaryBox.innerHTML = "";
            summaryBox.innerHTML = data.summary;
        } else {
            // Show error details in the summary box
            summaryBox.innerHTML = `Error: ${data.detail}`;
        }
    } 
    catch (error) {
        summaryBox.innerHTML = `Error: ${error.message}`;
    }
});
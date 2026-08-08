{
    document.getElementById("homeForm").addEventListener("submit", (e) => {
        if (!confirm("Are you sure you want to leave this game? Your current progress will be lost.")) {
            e.preventDefault();
        }
    });
}
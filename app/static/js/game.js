    {
    let map = null;
    let marker = null;

    const modal = document.getElementById("mapModal");
    const submitBtn = document.getElementById("submitBtn");
    const latInput = document.getElementById("lat");
    const lngInput = document.getElementById("lng");

    modal.style.display = "block";
    submitBtn.focus();

    map = L.map("map").setView(
        [15.392514, 73.880434],
        15
    );

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: "&copy; OpenStreetMap contributors"
        }
    ).addTo(map);

    map.on("click", handleMapClick);

    /* ===========================
    Resize Map
    =========================== */

    const mapPanel = document.getElementById("mapModal");
    const imagePanel = document.querySelector(".image-section");
    const resizeBtn = document.getElementById("resizeMapBtn");

    resizeBtn.addEventListener("click", () => {

        mapPanel.classList.toggle("expand");
        imagePanel.classList.toggle("shrink");

        setTimeout(() => {

            map.invalidateSize();

        }, 300);

    });

    function handleMapClick(e) {

        if (marker) {
            marker.remove();
        }

        latInput.value = e.latlng.lat;
        lngInput.value = e.latlng.lng;

        marker = L.marker(e.latlng).addTo(map);

        submitBtn.disabled = false;
        submitBtn.textContent = "Submit Guess";
        submitBtn.focus();

    }
    
}

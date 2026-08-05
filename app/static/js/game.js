    {
    let map = null;
    let marker = null;

    const openBtn = document.getElementById("openMapBtn");
    const closeBtn = document.getElementById("closeMapBtn");
    const modal = document.getElementById("mapModal");
    const submitBtn = document.getElementById("submitBtn");
    const latInput = document.getElementById("lat");
    const lngInput = document.getElementById("lng");

    openBtn.addEventListener("click", () => {

        modal.style.display = "block";
        submitBtn.focus();

        if (!map) {

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

        } else {

            map.invalidateSize();

        }

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

    closeBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });

    modal.addEventListener("click", (e) => {

        if (e.target === modal) {
            modal.style.display = "none";
            openBtn.focus();
        }

    });

    document.addEventListener("keydown", (event) => {

        if (event.key === "Escape") {
            modal.style.display = "none";
            openBtn.focus();
        }

    });
}

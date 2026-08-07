    {
    let map = null;
    let marker = null;

    const modal = document.getElementById("mapModal");
    const submitBtn = document.getElementById("submitBtn");
    const latInput = document.getElementById("lat");
    const lngInput = document.getElementById("lng");

    const guessIcon = L.icon({
        iconUrl: "/static/images/leaf-icons/leaf-red.png",
        shadowUrl: "/static/images/leaf-icons/leaf-shadow.png",

        iconSize:     [19, 47.5], // size of the icon
        shadowSize:   [25, 32], // size of the shadow
        iconAnchor:   [11, 47], // point of the icon which will correspond to marker's location
        shadowAnchor: [2, 32],  // the same for the shadow
        popupAnchor:  [-1.5, -38] // point from which the popup should open relative to the iconAnchor

    });

    modal.style.display = "block";
    submitBtn.focus();

    map = L.map("map").setView(                         // render map
        [15.391514, 73.879034],
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

    function handleResizeClick() {                      // resize function
        mapPanel.classList.toggle("expand");
        imagePanel.classList.toggle("shrink");

        setTimeout(() => {

            map.invalidateSize();

        }, 300);
    };

    resizeBtn.addEventListener("click", () => {         // mouse resize
        handleResizeClick();
    });

    window.addEventListener('keydown', (e)=>{           // keyboard resize
        if(e.key==='f'){
            handleResizeClick();
        };
    });

    window.addEventListener('keydown', (e)=>{           // Keyboard Shortcuts
        const pixelDistance = 100;

        const animOptions = {
            animate: true,
            duration: 0.5,                              // Animation length in seconds
            easeLinearity: 0.25
        };

        if (e.key === '+' || e.key === '=' || e.key === ']' || e.key.toLowerCase() === 'e') {
            map.zoomIn(1, animOptions);                 // Zoom in by 1 level
        } 
        else if (e.key === '-' || e.key === '_' || e.key === '[' || e.key.toLowerCase() === 'q') {
            map.zoomOut(1, animOptions);                // Zoom out by 1 level
        }
        else if (e.key === 'ArrowUp' || e.key.toLowerCase() === 'w') {
            map.panBy([0, -pixelDistance], animOptions); // Pan up
        } else if (e.key === 'ArrowDown' || e.key.toLowerCase() === 's') {
            map.panBy([0, pixelDistance], animOptions);  // Pan down
        } else if (e.key === 'ArrowLeft' || e.key.toLowerCase() === 'a') {
            map.panBy([-pixelDistance, 0], animOptions); // Pan left
        } else if (e.key === 'ArrowRight' || e.key.toLowerCase() === 'd') {
            map.panBy([pixelDistance, 0], animOptions);  // Pan right
        }
        if (e.key === 'r') {
            handleRClick(latlng = map.getCenter());
        };
    });

    function handleRClick(){                            // keyboard marker placement

        if (marker) {
            marker.remove();
        }

        latInput.value = latlng.lat;
        lngInput.value = latlng.lng;

        marker = L.marker(
            map.getCenter(), 
            { icon: guessIcon }
        ).addTo(map);

        submitBtn.disabled = false;
        submitBtn.textContent = "Submit Guess";
        submitBtn.focus();

    };

    function handleMapClick(e) {                        // mouse marker placement

        if (marker) {
            marker.remove();
        }

        latInput.value = e.latlng.lat;
        lngInput.value = e.latlng.lng;

        marker = L.marker(
            e.latlng, 
            { icon: guessIcon }
        ).addTo(map);

        submitBtn.disabled = false;
        submitBtn.textContent = "Submit Guess";
        submitBtn.focus();

    }
    
}

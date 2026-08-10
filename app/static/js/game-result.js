{
    const mapElement = document.getElementById("gameResultMap");
    const rounds = JSON.parse(mapElement.dataset.rounds);

    const map = L.map("gameResultMap");

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    ).addTo(map);
    map.attributionControl.setPrefix(false);

    const bounds = [];

    const guessIcon = L.icon({
        iconUrl: "/static/images/leaf-icons/leaf-red.png",
        shadowUrl: "/static/images/leaf-icons/leaf-shadow.png",

        iconSize:     [19, 47.5], // size of the icon
        shadowSize:   [25, 32], // size of the shadow
        iconAnchor:   [11, 47], // point of the icon which will correspond to marker's location
        shadowAnchor: [2, 32],  // the same for the shadow
        popupAnchor:  [-1.5, -38] // point from which the popup should open relative to the iconAnchor

    });

    const answerIcon = L.icon({
        iconUrl: "/static/images/leaf-icons/leaf-green.png",
        shadowUrl: "/static/images/leaf-icons/leaf-shadow.png",

        iconSize:     [19, 47.5], // size of the icon
        shadowSize:   [25, 32], // size of the shadow
        iconAnchor:   [11, 47], // point of the icon which will correspond to marker's location
        shadowAnchor: [2, 32],  // the same for the shadow
        popupAnchor:  [-1.5, -38] // point from which the popup should open relative to the iconAnchor

    });

    const roundMarkers = [];

    rounds.forEach((round, index) => {

        const guess = round.guess;
        const answer = round.answer;

        bounds.push(guess);
        bounds.push(answer);

        const guessMarker = L.marker(guess, {
            icon: guessIcon
        })
        .bindPopup(`
            <b>Round ${index + 1}</b><br>
            <strong>Your Guess</strong><br>
            Score: ${round.score} pts<br>
            Distance: ${round.distance} m
        `)
        .addTo(map);

        const answerMarker = L.marker(answer, {
            icon: answerIcon
        })
        .bindPopup(`
            <b>Round ${index + 1}</b><br>
            <strong>Actual Location</strong><br>
            Score: ${round.score} pts<br>
            Distance: ${round.distance} m
        `)
        .addTo(map);

        L.polyline(
            [guess, answer],
            {
                dashArray: "10 8",
                weight: 3
            }
        ).addTo(map);

        roundMarkers.push({
            guess: guessMarker,
            answer: answerMarker
        });

    });

    map.fitBounds(bounds, {
        padding: [40, 40]
    });


    mapElement.addEventListener('keydown', (e)=>{
        const pixelDistance = 100;

        const animOptions = {
            animate: true,
            duration: 0.5, // Animation length in seconds
            easeLinearity: 0.25
        };

        if (e.key === '+' || e.key === '=' || e.key === ']' || e.key.toLowerCase() === 'e') {
            map.zoomIn(1, animOptions); // Zoom in by 1 level
        } 
        else if (e.key === '-' || e.key === '_' || e.key === '[' || e.key.toLowerCase() === 'q') {
            map.zoomOut(1, animOptions); // Zoom out by 1 level
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
    });

    const summaryRows = document.querySelectorAll(".summary-row");

    summaryRows.forEach((row, index) => {

        row.style.cursor = "pointer";

        row.addEventListener("click", () => {

            const guessMarker = roundMarkers[index].guess;
            const answerMarker = roundMarkers[index].answer;

            map.fitBounds(
                [
                    guessMarker.getLatLng(),
                    answerMarker.getLatLng()
                ],
                {
                    padding: [60, 60],
                    animate: true
                }
            );

            guessMarker.openPopup();

        });

    });

}
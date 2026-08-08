/*{
    const card = document.querySelector(".card");

    document.addEventListener("mousemove", (e) => {

        const x = (e.clientX - window.innerWidth / 2) / 40;
        const y = (e.clientY - window.innerHeight / 2) / 40;

        card.style.transform =
            `translate(${x}px, ${y}px)
            rotateY(${x/4}deg)
            rotateX(${-y/4}deg)`;

    });

    document.addEventListener("mouseleave", () => {

        card.style.transform =
            "translate(0,0) rotateX(0) rotateY(0)";

    });
}*/

{
    const mapElement = document.getElementById("map");

    const GUESS_LAT = parseFloat(mapElement.dataset.guessLat);
    const GUESS_LNG = parseFloat(mapElement.dataset.guessLng);

    const ANSWER_LAT = parseFloat(mapElement.dataset.answerLat);
    const ANSWER_LNG = parseFloat(mapElement.dataset.answerLng);

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

    let map = L.map("map").setView(
        [15.392514, 73.880434],
        15
    );
    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    ).addTo(map);
    const guessMarker = L.marker(
        [GUESS_LAT, GUESS_LNG],
        { icon: guessIcon }
    ).addTo(map);

    guessMarker.bindTooltip("Your Guess", {
        permanent: false,
        direction: "bottom"
    });

    const answerMarker = L.marker(
        [ANSWER_LAT, ANSWER_LNG],
        { icon: answerIcon }
    ).addTo(map);

    answerMarker.bindTooltip("Correct Location", {
        permanent: false,
        direction: "bottom"
    });
    const line = L.polyline([
        [GUESS_LAT, GUESS_LNG],
        [ANSWER_LAT, ANSWER_LNG]
    ],{
        color:"#231F72",
        weight:4,
        opacity:.8,
        dashArray: "10, 10"
    }).addTo(map);

    map.fitBounds(line.getBounds(), {
        padding:[40,40]
    });

    map.dragging.disable();
    map.scrollWheelZoom.disable();
    map.doubleClickZoom.disable();
    map.boxZoom.disable();
    map.keyboard.disable();
    map.touchZoom.disable();
}
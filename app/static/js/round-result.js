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
    const mapElement = document.getElementById("resultMap");

    const GUESS_LAT = parseFloat(mapElement.dataset.guessLat);
    const GUESS_LNG = parseFloat(mapElement.dataset.guessLng);

    const ANSWER_LAT = parseFloat(mapElement.dataset.answerLat);
    const ANSWER_LNG = parseFloat(mapElement.dataset.answerLng);

    const guessIcon = L.icon({
        iconUrl: "/static/images/leaf-icons/leaf-red.png",
        shadowUrl: "/static/images/leaf-icons/leaf-shadow.png",

        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    const answerIcon = L.icon({
        iconUrl: "/static/images/leaf-icons/leaf-green.png",
        shadowUrl: "/static/images/leaf-icons/leaf-shadow.png",

        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    let map = L.map("resultMap").setView(
        [15.392514, 73.880434],
        15
    );
    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: "&copy; OpenStreetMap contributors"
        }
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
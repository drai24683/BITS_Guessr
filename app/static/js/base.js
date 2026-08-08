{
    const backgrounds = [
        "/static/images/background/BdomeHD.jpeg",
        "/static/images/background/NAB_Path.jpeg"
    ];

    const randomImage =
        backgrounds[Math.floor(Math.random() * backgrounds.length)];

    document.getElementById("background").style.backgroundImage =
        `url("${randomImage}")`;

    const infoBtn = document.getElementById("infoBtn");
    const infoModal = document.getElementById("infoModal");
    const closeInfo = document.getElementById("closeInfo");

    infoBtn.addEventListener("click", () => {

        infoModal.classList.remove("hidden");

    });

    closeInfo.addEventListener("click", () => {

        infoModal.classList.add("hidden");

    });

    infoModal.addEventListener("click", (event) => {

        if (event.target === infoModal) {

            infoModal.classList.add("hidden");

        }

    });

    window.addEventListener("keydown", (event) => {

        if (event.key.toLowerCase() === "i") {

            infoModal.classList.toggle("hidden");

        }

    });

}
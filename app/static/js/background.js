{
    const backgrounds = [
        "/static/images/background/BdomeHD.jpeg",
        "/static/images/background/NAB_Path.jpeg"
    ];

    const randomImage =
        backgrounds[Math.floor(Math.random() * backgrounds.length)];

    document.getElementById("background").style.backgroundImage =
        `url("${randomImage}")`;
}
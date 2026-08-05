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
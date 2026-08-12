{
    const guestBtn = document.getElementById("guestBtn");
    const loginForm = document.getElementById("loginForm");
    const homeDesc = document.getElementById("homeDesc");

    guestBtn.addEventListener("click", () => {
        guestBtn.classList.add("hidden");
        setTimeout(() => {
            loginForm.classList.remove("hidden");
            homeDesc.style.color = "grey";
        }, 300);
    });
}
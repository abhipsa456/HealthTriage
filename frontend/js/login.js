document
    .getElementById("loginForm")
    .addEventListener("submit", function (event) {

        event.preventDefault();

        const role = document.querySelector(
            'input[name="role"]:checked'
        ).value;


        if (role === "patient") {

            window.location.href = "patient.html";

        } else {

            window.location.href = "dashboard.html";

        }

    });
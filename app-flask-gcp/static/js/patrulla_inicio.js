const toggleThemeButton = document.getElementById("toggle-theme");
        const settingsButton = document.getElementById("settings");
        const body = document.body;

        toggleThemeButton.addEventListener("click", () => {
            if (body.classList.contains("dark")) {
                // Cambiar a modo claro
                body.classList.replace("dark", "light");
                toggleThemeButton.textContent = "🌞"; // Sol para modo claro
                toggleThemeButton.classList.replace("dark", "light");
                settingsButton.classList.replace("dark", "light");

                document.querySelectorAll('.button').forEach(button => {
                    button.classList.replace("dark", "light");
                });
            } else {
                // Cambiar a modo oscuro
                body.classList.replace("light", "dark");
                toggleThemeButton.textContent = "🌙"; // Luna para modo oscuro
                toggleThemeButton.classList.replace("light", "dark");
                settingsButton.classList.replace("light", "dark");

                document.querySelectorAll('.button').forEach(button => {
                    button.classList.replace("light", "dark");
                });
            }
        });

        settingsButton.addEventListener("click", () => {
            alert("Ir a la configuración");
        });



        
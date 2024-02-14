function hideFields() {
            document.getElementById("first_name").style.display = "none";
            document.getElementById("last_name").style.display = "none";
            document.getElementById("email").style.display = "none";
            document.getElementById("phone").style.display = "none";
            document.getElementById("street").style.display = "none";
            document.getElementById("city").style.display = "none";
            document.getElementById("postal_code").style.display = "none";
            document.getElementById("birth_date").style.display = "none";
            document.getElementById("login").style.display = "inline-block";
            document.getElementById("register").style.display = "none";
            document.getElementById("register_button").style.display = "inline-block"; // Show the Register button
            document.getElementById("login_button").style.display = "none"; // Hide the Register button
            document.getElementById("form").action = "/login"
        }

        function showAllFields() {
            document.getElementById("first_name").style.display = "inline-block";
            document.getElementById("last_name").style.display = "inline-block";
            document.getElementById("email").style.display = "inline-block";
            document.getElementById("phone").style.display = "inline-block";
            document.getElementById("street").style.display = "inline-block";
            document.getElementById("city").style.display = "inline-block";
            document.getElementById("postal_code").style.display = "inline-block";
            document.getElementById("birth_date").style.display = "inline-block";
            document.getElementById("login").style.display = "none";
            document.getElementById("register").style.display = "inline-block";
            document.getElementById("login_button").style.display = "inline-block"; // Show the Register button
            document.getElementById("register_button").style.display = "none"
            document.getElementById("form").action = "/register"
        }
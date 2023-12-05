<script>
    let username = "";
    let password = "";

    const handleSubmit = async () => {
        // Handle login logic here
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        // Handle the response, e.g., redirect on success
        if (response.ok) {
            window.location.href = "/index2";
        } else {
            alert("Invalid username or password");
        }
    };
</script>


<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Вход</title>
</head>
<body>
    <h1>Вход</h1>
    <form method="POST" action="/">
        <label for="username">Name:</label>
        <input type="text" id="username" name="username" required /><br />

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required /><br />

        <button type="submit">Sign in</button>
    </form>
</body>

<style>
    input, button {
    font-family: inherit;
    font-size: inherit;
    -webkit-padding: 0.4em 0;
    padding: 0.4em;
    margin: 0 0 0.5em 0;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 2px;
}
</style>

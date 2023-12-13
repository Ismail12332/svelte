<script>
    import { onMount } from 'svelte';

    let username = '';
    let password = '';

    const handleSubmit = async (event) => {
        event.preventDefault();

        const response = await fetch('http://127.0.0.1:5000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ username, password }),
        });

        const result = await response.text();
        console.log(result);
    };
</script>

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Вход</title>
</head>

<body>
    <h1>Survzila</h1>
    <h1>Please</h1>
    <form on:submit={handleSubmit}>
        <label for="username">Name:</label>
        <input type="text" id="username" name="username" bind:value={username} required /><br />

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" bind:value={password} required /><br />

        <button type="submit">Sign in</button>
    </form>
</body>


<style>
    h1 {
	color: #ff3e00;
	text-transform: uppercase;
	font-size: 4em;
	font-weight: 100;
    margin: 20px;
    }

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

    body {
	color: #333;
	margin: 0;
	padding: 8px;
	box-sizing: border-box;
	font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    }

    body {
	position: relative;
	width: 100%;
	height: 100%;
    }
    
    label {
	display: block;
    }

</style>

<script>
    import { createEventDispatcher } from "svelte";
    import { onMount } from "svelte";
    import { navigate } from "svelte-navigator";
    import Register from "./Register.svelte";

    const dispatch = createEventDispatcher();
    let showModal = false

    function close() {
    dispatch("close");
    }

    let username = '';
    let password = '';

    const handleSubmit = async (event) => {
        event.preventDefault();

        const response = await fetch('http://127.0.0.1:5000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                password,
            }),
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === 'success') {
                // Save user ID or authentication token to localStorage
                localStorage.setItem('user_id', data.user_id);
                console.log(data.user_id)

                // Notify the parent component about the successful login
                dispatch('loginSuccess', { user_id: data.user_id });
                navigate('/glav');
            } else {
                console.error('Incorrect username or password.');
            }
        } else {
            console.error('Failed to authenticate.');
        }
    };
</script>

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Вход</title>
</head>

<body>
    <div class="for-login">
        <h1>Survzila</h1>
        <h1>Please</h1>
        <form on:submit={handleSubmit}>
            <label for="username">Name:</label>
            <input type="text" id="username" name="username" bind:value={username} required /><br />

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" bind:value={password} required /><br />

            <button type="submit">Sign in</button>
        </form>
        <button class="for-fxod" on:click={() => (showModal = true)}>Register</button>
                {#if showModal}
                    <Register on:close={() => (showModal = false)} />
                {/if}
    </div>
</body>


<style>
    .for-login {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
    }

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
	width: 100%;
	height: 100%;
    }
    
    label {
	display: block;
    }

</style>

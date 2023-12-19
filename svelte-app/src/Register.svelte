<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    function close() {
        dispatch("close");
    }

    let username = '';
    let password = '';
    let email = '';

    const handleSubmit = async (event) => {
        const response = await fetch('http://127.0.0.1:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Изменили Content-Type
            },
            body: JSON.stringify({
                username,
                password,
                email
            }),
        });

        const result = await response.text();
        console.log(result);
    };
</script>

<body>
    <div class="modal">
        <h1>Register</h1>
        <form on:submit={handleSubmit}>
            <label for="username">Name:</label>
            <input type="text" id="username" bind:value={username} required /><br />

            <label for="password">password:</label>
            <input type="password" id="password" bind:value={password} required /><br />

            <label for="email">Email:</label>
            <input type="email" id="email" bind:value={email} required /><br />

            <button type="submit">Register</button>
        </form>
        <button on:click={close}>Close</button>
    </div>
</body>
<style>
    .modal {
        padding: 1rem;
        position: fixed;
        top: 48%;
        left: 50%;
        transform: translate(-50%, -50%);
        max-height: 45vh;
        max-width: 30vh;
        background: white;
        border-radius: 5px;
        z-index: 100;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
        display: block; /* Ensure the modal is displayed */
        opacity: 1; /* Ensure the opacity is non-zero */
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

    input:disabled {
    color: #ccc;
    }

    button {
    color: #333;
    background-color: #f4f4f4;
    outline: none;
    }
    
    label {
	display: block;
    }

</style>

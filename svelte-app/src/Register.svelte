<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    function close() {
        dispatch("close");
    }
</script>
<body>
    

    <div class="modal">
        <h1>Register</h1>
        <form method="POST" action="/register">
            <label for="username">Name:</label>
            <input type="text" id="username" name="username" required /><br />

            <label for="password">password:</label>
            <input type="password" id="password" name="password" required /><br />

            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required /><br />

            <button type="submit">Register</button>
        </form>
        <button on:click={close}>Close</button>
    </div>
</body>
<style>
    .modal {
        padding: 1rem;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        max-height: 80vh;
        background: white;
        border-radius: 5px;
        z-index: 100;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
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

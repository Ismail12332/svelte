<script>
	import Login from './Login.svelte';
	import Register from './Register.svelte';
	let showModal = false;
</script>

<main>
	<Login />
	{#if showModal}
		<Register on:click="{() => showModal = false}" on:close="{() => showModal = false}"/>
	{/if}
	<!-- Добавьте ссылку на страницу регистрации -->
    <button on:click={() => (showModal = true)}>Register</button>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

	button {
    color: #333;
    background-color: #f4f4f4;
    outline: none;
	font-family: inherit;
    font-size: inherit;
    -webkit-padding: 0.4em 0;
    padding: 0.4em;
    margin: 0 0 0.5em 0;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 2px;
	font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    }
</style>
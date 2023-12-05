<script>
	import Login from './Login.svelte';
	import Register from './Register.svelte';
	export let name;
	let showModal = false;
</script>

<main>
	<h1>Hello {name}!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
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

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
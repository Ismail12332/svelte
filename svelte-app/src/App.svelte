<script>
	import { fetchData } from './api';
	import Glav from "./glav/glav.svelte";
	import Login from "./Login.svelte";
	import Register from "./Register.svelte";
	import { onMount } from "svelte";

	let showModal = false;
</script>

<body>
	
	<main>
		
		<Login />
		<button on:click={() => (showModal = true)}>Register</button>
		{#if showModal}
		<Register
		on:click={() => (showModal = false)} 
		on:close={() => (showModal = false)}/>
		{/if}
	</main>
	
</body>

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
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
      Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
  }
</style>

<script>
    import { onMount } from "svelte";
    import { goto } from '$app/navigation';
    import { writable } from 'svelte/store';

    let first_name = writable("");
    let last_name = writable("");
    let city = writable("");
    let phone = writable("");
    let post = writable("");
    let vessel_name = writable("");

    let projects = [];
    let user_id;

    onMount(async () => {
        try {
            const projectsResponse = await fetch('http://127.0.0.1:5000/index2', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        });

            if (projectsResponse.ok) {
            const responseData = await projectsResponse.json();
            projects = responseData.projects;
            user_id = responseData.user_id;
            console.log("User ID:", user_id);
            console.log("Projects:", projects);
            } else {
            const text = await projectsResponse.text();
            console.error('Unexpected response:', text);
            }
        } catch (error) {
            console.error('Error fetching projects:', error);
        }
        });

    async function createProject() {
        // Log user_id before making the request
        console.log("User ID (Create Project):", user_id);

        try {
            const response = await fetch('http://127.0.0.1:5000/index2', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    first_name: $first_name,
                    last_name: $last_name,
                    city: $city,
                    phone: $phone,
                    post: $post,
                    vessel_name: $vessel_name,
                }),
            });

            if (response.ok) {
                const newProject = await response.json();
                projects = [...projects, newProject];
            }
        } catch (error) {
            console.error('Error creating project:', error);
        }
    }

    function goToEditProject(projectId) {
        goto(`/edit_project/${projectId}`);
    }
</script>

<style>

@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css');
    

form {
    width: 100%;

}

main {
    width: 100%;
    height: 1200px;
    background: linear-gradient(to bottom, #011a2b, #011529);
}

h1,h2 {
    color: #fff;
}

label {
    color: #fff;
}

p,ul {
    color: #fff;
}



.project-info {
    display: flex;
    margin: 3%;
    flex: 1; /* Равное распределение доступного пространства между дочерними элементами */
    border: 1px solid #000; /* Добавьте границу, чтобы лучше видеть разделение */
    padding: 10px;
    background-color: #191d32;
    justify-content: space-around;
}
    
</style>

<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
</head>


    <main>
        <h1>Survzilla</h1>
        <a href="/logout" class="btn btn-danger">Выйти</a>
        <form class="row g-3 needs-validation"  method="POST"  novalidate action="/index2">
                <div class="col-md-4">
                    <label for="validationCustom01" class="form-label">First name</label>
                    <input type="text" class="form-control" id="validationCustom01"  name="first_name" bind:value={$first_name} required>
                    <div class="valid-feedback">
                    Looks good!
                </div>
                </div>
                <div class="col-md-4">
                    <label for="validationCustom02" class="form-label">Last name</label>
                    <input type="text" class="form-control" id="validationCustom02" name="last_name" bind:value={$last_name} required>
                    <div class="valid-feedback">
                    Looks good!
                </div>
                </div>
                <div class="col-md-4">
                    <label for="validationCustomUsername" class="form-label">post</label>
                    <div class="input-group has-validation">
                    <span class="input-group-text" id="inputGroupPrepend">@</span>
                    <input type="text" class="form-control" id="validationCustomUsername" name="post" bind:value={$post} aria-describedby="inputGroupPrepend" required>
                    <div class="invalid-feedback">
                        Please choose a username.
                    </div>
                </div>
                </div>
                <div class="col-md-6">
                    <label for="validationCustom03" class="form-label">City</label>
                    <input type="text" class="form-control" id="validationCustom03" name="city" bind:value={$city} required>
                    <div class="invalid-feedback">
                    Please provide a valid city.
                </div>
                </div>
                <div class="col-md-3">
                    <label for="validationCustom04" class="form-label">Vessel Name</label>
                    <input type="text" class="form-control" id="validationCustom04" name="vessel_name" bind:value={$vessel_name} required>
                    <div class="invalid-feedback">
                        Please enter a valid vessel name.
                </div>
                </div>
                <div class="col-md-3">
                    <label for="validationCustom05" class="form-label">Phone</label>
                    <input type="text" class="form-control" id="validationCustom05" name="phone" bind:value={$phone} required>
                    <div class="invalid-feedback">
                    Please provide a valid phone.
                </div>
                </div>
                <div class="col-12">
                    <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" id="invalidCheck" required>
                    <label class="form-check-label" for="invalidCheck">
                        Agree to terms and conditions
                    </label>
                    <div class="invalid-feedback">
                        You must agree before submitting.
                    </div>
                </div>
                </div>
                <div class="col-12">
                    <button id="createProjectBtn" class="btn btn-primary" type="submit">Create a new Project</button>
                </div>
            </form>
            <h1>Добро пожаловать!</h1>
            <h2>Ваши проекты:</h2>

            <ul>
            {#if projects.length > 0}
                {#each projects as project (project._id)}
                <li class="project-info">
                    <a href="/edit_project/{project._id}" on:click={() => goToEditProject(project._id)}>Sign in</a>
                    <strong>Name:</strong> {project.first_name} {project.last_name}<br>
                    <strong>City: </strong> {project.city}<br>
                    <strong>Phone: </strong> {project.phone}<br>
                    <strong>Post: </strong> {project.post}<br>
                    <strong>Time create: </strong> {project.created_at}<br>
                    <p><strong>Vessel name: </strong> {project.vessel_name}</p>
                </li>
                {/each}
            {:else}
                <p>У вас пока нет проектов.</p>
            {/if}

            <button on:click={createProject}>Create a new Project</button>
            </ul>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm" crossorigin="anonymous"></script>
    </main>       




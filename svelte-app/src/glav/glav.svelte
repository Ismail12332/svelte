<script>
    import { onMount } from "svelte";

    let projects = [];
    let user_id;

  // Simulate a form submission
    const handleSubmit = async () => {
    // Simulate form data
    const formData = new FormData(document.getElementById("projectForm"));

    try {
        const response = await fetch("/index2", {
        method: "POST",
        body: formData,
    });

    if (response.ok) {
        const result = await response.json();
        window.location.href = `/edit_project/${result.project_id}`;
    } else {
        console.error("Error submitting form");
    }
    } catch (error) {
    console.error("Error submitting form:", error);
    }
};

  // Simulate onMount lifecycle hook
    onMount(async () => {
    // Simulate fetching projects data
    const response = await fetch("/get_projects");
    const data = await response.json();
    projects = data.projects;
    user_id = data.user_id;
});
</script>


<body>
    <h1>Survzilla</h1>
    <a href="/logout" class="btn btn-danger">Выйти</a>
    <form class="row g-3 needs-validation"  method="POST"  novalidate action="/index2">
            <div class="col-md-4">
                <label for="validationCustom01" class="form-label">First name</label>
                <input type="text" class="form-control" id="validationCustom01" name="first_name" value="" required>
                <div class="valid-feedback">
                Looks good!
            </div>
            </div>
            <div class="col-md-4">
                <label for="validationCustom02" class="form-label">Last name</label>
                <input type="text" class="form-control" id="validationCustom02" name="last_name" value="" required>
                <div class="valid-feedback">
                Looks good!
            </div>
            </div>
            <div class="col-md-4">
                <label for="validationCustomUsername" class="form-label">post</label>
                <div class="input-group has-validation">
                <span class="input-group-text" id="inputGroupPrepend">@</span>
                <input type="text" class="form-control" id="validationCustomUsername" name="post" aria-describedby="inputGroupPrepend" required>
                <div class="invalid-feedback">
                    Please choose a username.
                </div>
            </div>
            </div>
            <div class="col-md-6">
                <label for="validationCustom03" class="form-label">City</label>
                <input type="text" class="form-control" id="validationCustom03" name="city" required>
                <div class="invalid-feedback">
                Please provide a valid city.
            </div>
            </div>
            <div class="col-md-3">
                <label for="validationCustom04" class="form-label">Vessel Name</label>
                <input type="text" class="form-control" id="validationCustom04" name="vessel_name" required>
                <div class="invalid-feedback">
                    Please enter a valid vessel name.
            </div>
            </div>
            <div class="col-md-3">
                <label for="validationCustom05" class="form-label">Phone</label>
                <input type="text" class="form-control" id="validationCustom05" name="phone" required>
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
                    <div class="project-info">
                        <a href={`/edit_project/${project._id}`}>
                            <strong>Name:</strong>
                            {project.first_name}
                            {project.last_name}<br />
                        </a>
                        <strong>City: </strong>
                        {project.city}<br />
                        <strong>Phone: </strong>
                        {project.phone}<br />
                        <strong>Post: </strong>
                        {project.post}<br />
                        <strong>Time create: </strong>
                        {project.created_at}<br />
                        <p><strong>Vessel name: </strong> {project.vessel_name}</p>
                    </div>
                {/each}
            {:else}
                <p>У вас пока нет проектов.</p>
            {/if}

            <form id="projectForm" class="row g-3" method="POST" action="/index2">
                <!-- Your form fields go here, make sure to include the required attributes -->
                <div class="col-12">
                    <button type="button" on:click={handleSubmit} class="btn btn-primary"
                    >Create a new Project</button>
                </div>
            </form>
        </ul>
</body>

<style>
  /* Your styles go here */
    /* 1 page */
body {
    width: 100%;
    background: linear-gradient(to bottom, #011a2b, #011529);
}

h1,h2,h3,h4 {
    color: #fff;
}

label {
    color: #fff;
}

p,ul {
    color: #fff;
}

.g-3 {
    --bs-gutter-y: 1rem;
    width: 100%;
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

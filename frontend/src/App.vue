<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useRouter } from 'vue-router';

const router = useRouter();

async function logout() {
  const response = await fetch('http://127.0.0.1:5000/logout-user', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authentication-Token': localStorage.getItem("auth_token")
    }
  });
  if (response.ok) {

    const result = await response.json();
    console.log(result);

    localStorage.removeItem("auth_token");
    router.push('/login');

    alert(result.message);

  } else {
    alert("Logout failed!");
  }
}
function is_loggedin(){
  return localStorage.getItem("auth_token") !== null;
}

</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" to="/">Dashboard</RouterLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink class="nav-link active" aria-current="page" to="/">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/signup">Sign Up</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/studentdashboard">Student Dashboard</RouterLink>
            </li>
            <li class="nav-item">
              <button class="btn btn-outline-danger" @click="logout" v-show="is_loggedin()">Logout</button>
            </li>
          </ul>
          <form class="d-flex" role="search">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
        </div>
      </div>
    </nav>
    <RouterView />
  </div>
</template>

<style scoped></style>

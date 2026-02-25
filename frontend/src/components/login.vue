<template>
    <div class="container-fluid">
        <form @submit.prevent="submitForm">
            <div class="mb-3">
                <label for="username" class="form-label">Username: </label>
                <input type="text" class="form-control" id="username" aria-describedby="username" v-model="username"
                    @input="checkusername">
                <div id="usernameHelp" class="form-text">{{ usernameHelp }}</div>
            </div>

            <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label">Password</label>
                <input type="password" class="form-control" id="exampleInputPassword1" v-model="password"
                    @input="checkpw">
                <div id="passwordHelp" class="form-text">{{ passwordHelp }}</div>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const username = ref('');
const password = ref('');
const passwordHelp = ref('');
const usernameHelp = ref('');

function checkusername() {
    if (username.value.length === 0) {
        usernameHelp.value = "username should be a valid name!!!";
        return false;
    } else {
        usernameHelp.value = "";
        return true;
    }
}

function checkpw() {
    if (password.value.length < 6) {
        passwordHelp.value = "Password must be at least 6 characters long";
        return false;
    }
    else {
        passwordHelp.value = "";
        return true;
    }
}

async function submitForm() {
    if (!checkusername() || !checkpw()) {
        alert("Please check the input again!!!!");
        return;
    }

    const response = await fetch('http://127.0.0.1:5000/login-user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username.value,
            password: password.value
        })
    });
    if (response.ok) {
        const result = await response.json();
        console.log(result);
        alert(result.message);
        localStorage.setItem("auth_token", result.auth_token);
        router.push('/studentdashboard');


    } else {
        const result = await response.json();
        alert("Login failed!: " + result.message);
    }

    console.log(response);
}
</script>
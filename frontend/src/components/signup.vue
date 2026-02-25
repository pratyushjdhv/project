<template>
    <div class="container-fluid">
        <form @submit.prevent="submitForm">
            <div class="mb-3">
                <label for="username" class="form-label">Username: </label>
                <input type="text" class="form-control" id="username" aria-describedby="username" v-model="username" @input="checkusername">
                <div id="usernameHelp" class="form-text">{{ usernameHelp }}</div>
            </div>
            <div class="mb-3">
                <label for="exampleInputEmail1" class="form-label">Email address</label>
                <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp"
                    v-model="email" @input="checkemail">
                <div id="emailHelp" class="form-text">{{ emailHelp }}</div>
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

const username = ref('');
const email = ref('');
const password = ref('');
const passwordHelp = ref('');
const emailHelp = ref('');

function checkusername(){
    if (username.value.length !== 0) {
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

function checkemail() {
    if (email.value.includes("@gmail.com") && email.value.length > 10) {
        emailHelp.value = "";
        return true;
    } else {
        emailHelp.value = "Please enter a valid Gmail address";
        return false;
    }
}

async function submitForm() {
    if (!checkusername() || !checkpw() || !checkemail()) {
        alert("please check the input again!!!!");
        return;
    }
    
    const response = await fetch('http://127.0.0.1:5000/signup-user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username.value,
            email: email.value,
            password: password.value
        })
    });
    
    
    if (response.ok) {
        const result = await response.json();
        alert(result.message);
    } else {
        const result = await response.json();
        alert("Registration failed!: " + result.message);
    }

    console.log(result);
}



</script>
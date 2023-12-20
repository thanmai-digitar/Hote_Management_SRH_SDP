function checkLogin() {
    const token = localStorage.getItem('token');
    console.log('Token:', token); // For debugging

    if (!token) {
        console.log('Redirecting to login...'); // For debugging
        window.location.href = '/login.html';
    }
}

window.onload = checkLogin;

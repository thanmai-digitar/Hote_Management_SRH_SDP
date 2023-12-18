fetch('http://localhost:8000/customers', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        firstName: "Test",
        lastName: "User",
        phone: "1234567890",
        email: "test@example.com",
        password: "password123"
    }),
})
.then(response => response.json())
.then(data => {
    console.log('Success:', data);
})
.catch((error) => {
    console.error('Error:', error);
});
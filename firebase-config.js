// Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
	apiKey: "AIzaSyD_oJ3yZ2Xh19xhGwFOUYdeCVK7fWGIE7Y",
	authDomain: "biometrer-6e571.firebaseapp.com",
	projectId: "biometrer-6e571",
	storageBucket: "biometrer-6e571.firebasestorage.app",
	messagingSenderId: "234629306776",
	appId: "1:234629306776:web:13226c0c8f19afe55d33ed",
	measurementId: "G-3Q6FXV1M9M"
  };

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

// Handle login
async function handleLogin(event) {
	event.preventDefault();
	const email = document.getElementById('email').value;
	const password = document.getElementById('password').value;

	try {
		// Sign in with Firebase
		const userCredential = await auth.signInWithEmailAndPassword(email, password);
		const user = userCredential.user;
		
		// Get ID token
		const idToken = await user.getIdToken();
		
		// Verify token with backend
		const response = await fetch('/verify-token', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ idToken: idToken })
		});

		if (response.ok) {
			window.location.href = '/';
		} else {
			const data = await response.json();
			alert(data.message || 'Authentication failed');
		}
	} catch (error) {
		alert(error.message);
	}
}

// Add event listener to login form
document.getElementById('loginForm').addEventListener('submit', handleLogin);

// Handle logout
auth.onAuthStateChanged((user) => {
	if (!user && window.location.pathname !== '/login') {
		window.location.href = '/login';
	}
});
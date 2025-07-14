// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    // If a base URL is found in local storage, load the posts
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    // Retrieve the base URL from the input field and save it to local storage
    var postTitle = document.getElementById('post-title');
    var postContent = document.getElementById('post-content');
    var addOrUpdatePostBtn = document.getElementById('addOrUpdatePostBtn')
    postTitle.value = ''
    postContent.value = ''
    addOrUpdatePostBtn.textContent ='Add Post'
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    // Use the Fetch API to send a GET request to the /posts endpoint
    fetch(baseUrl + '/posts')
        .then(response => response.json())  // Parse the JSON data from the response
        .then(data => {  // Once the data is ready, we can use it
            // Clear out the post container first
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            // For each post in the response, create a new post element and add it to the page
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `<h2>${post.title}</h2><p>${post.content}</p>
                <button onclick="editPost(${post.id})">Update</button>
                <button onclick="deletePost(${post.id})">Delete</button>
                `;

                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a POST request to the API to add a new post
function addPost() {
    // Retrieve the values from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;

    // Use the Fetch API to send a POST request to the /posts endpoint
    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, content: postContent })
    })
    .then(response => response.json())  // Parse the JSON data from the response
    .then(post => {
        console.log('Post added:', post);
        loadPosts(); // Reload the posts after adding a new one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    console.log(postId)
    var baseUrl = document.getElementById('api-base-url').value;

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Post deleted:', postId);
        loadPosts(); // Reload the posts after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

function editPost(postId){
    console.log(postId)
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title')
    var postContent = document.getElementById('post-content')
    var hidden_post_id = document.getElementById('hidden_post_id')
    var addOrUpdatePostBtn = document.getElementById('addOrUpdatePostBtn')
    postTitle.value = ''
    postContent.value = ''
    addOrUpdatePostBtn.textContent = 'Save Post'
    fetch(baseUrl + '/posts/' + postId, {
        method: 'GET',
    })
    .then(response => response.json())  // Parse the JSON data from the response
    .then(post => {
        postTitle.value = post.title
        postContent.value = post.content
        hidden_post_id.value = post.id
        addOrUpdatePostBtn.onclick = updatePost
    })
    .catch(error => console.error('Error:', error));
}

function updatePost() {
    // Retrieve the values from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var hidden_post_id = document.getElementById('hidden_post_id').value;

    // Use the Fetch API to send a POST request to the /posts endpoint
    fetch(baseUrl + '/posts/' + hidden_post_id, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, content: postContent })
    })
    .then(response => response.json())  // Parse the JSON data from the response
    .then(post => {
        console.log('Post updated:', post);
        loadPosts(); // Reload the posts after adding a new one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}


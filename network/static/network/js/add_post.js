document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#all-posts-link').addEventListener('click', () => load_posts('all_posts'));

    if (document.querySelector('#add-post-form') !== null) {
        document.querySelector('#add-post-form').onsubmit = send_post
    }
    if (document.querySelector('#all-posts') !== null) {
        load_posts('all_posts')
    }

});

const load_posts = (nav_bar) => {
    document.querySelector('#all-posts').innerHTML = ''

    fetch(`/${nav_bar}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.length === 0) {
                return document.querySelector('#all-posts').innerHTML = 'No posts.'
            }
            data.forEach(post => {
                display_posts(post);
            })
        });
}

const display_posts = (post) => {

    const postCard = document.createElement('div');
    postCard.className = 'post-card';

    document.getElementById('all-posts').appendChild(postCard);

    const postUser = document.createElement('div');
    postUser.className = 'post-user';
    postUser.innerHTML = post.original_poster;

    const postDate = document.createElement('div');
    postDate.className = 'post-date';
    postDate.innerHTML = post.timestamp;

    const postContent = document.createElement('div');
    postContent.className = 'post-content';
    postContent.innerHTML = post.content;

    const postLikes = document.createElement('div');
    postLikes.className = 'post-likes';
    postLikes.innerHTML = post.likes;

    [postUser, postDate, postContent, postLikes]
        .forEach(element => postCard.appendChild(element));

    postCard.appendChild(postLikes);
}

const clear_form = () => {
    document.querySelector('#add-content').value = '';
}

const send_post = () => {
    const csrftoken = getCookie('csrftoken');
    fetch('/add_post', {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#add-content').value
        }),
        headers: { "X-CSRFToken": csrftoken }
    }).then(response => response.json()).then(result => console.log(result)); // Print result
    setTimeout(() => load_posts('all_posts'), 1000);
    clear_form()
    return false;
}

// Set up CSRF_token from Django DOCS
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

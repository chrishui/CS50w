// Edit posts
function edit(post_id) {
  var edit_box = document.querySelector(`#edit-box-${post_id}`);
  var edit_btn = document.querySelector(`#edit-btn-${post_id}`);
  // Show edit box and button
  edit_box.style.display = 'block';
  edit_btn.style.display = 'block';

  // PUT request
  edit_btn.addEventListener('click', () => {
    fetch(`/edit/${post_id}`,{
      method: 'PUT',
      body: JSON.stringify({
        content: edit_box.value
      })
    })
    // Hide edit box and button
    edit_box.style.display = 'none';
    edit_btn.style.display = 'none';
    // Update content section of edited post
    document.querySelector(`#post-${post_id}`).innerHTML = edit_box.value;

  });
}

// Like/unlike posts
function like(post_id) {
  var like_btn = document.querySelector(`#like-${post_id}`);

  // POST request
  fetch(`/like/${post_id}`, {
    method: 'POST'
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    // Change button from 'like' to 'unlike'
    if (result['message'] == 'Liked') {
      like_btn.style.backgroundColor = '#F0F8FF'
      like_btn.innerHTML = 'Unlike'
    }
    // Change button from 'like' to 'unlike'
    if (result['message'] == 'Unliked') {
      like_btn.style.backgroundColor = 'White'
      like_btn.innerHTML = 'Like'
    }

  })


}

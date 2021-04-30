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
  like_btn.addEventListener('click', () => {
    fetch(`/like/${post_id}`,{
      method: 'POST'
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      // Change button from 'like' to 'unlike'
      document.querySelector(`#like-${post_id}`).innerHTML = 'Unlike';
    })


  });
}








// Like or unlike posts
// function like(post_id) {
//   var like_btn = document.querySelector(`#like-btn-${post_id}`);
//
//   // POST request
//   // Like/Unlike post
//   like_btn.addEventListener('click', () => {
//     fetch(`/liked/${post_id}`,{
//       method: 'POST',
//     })
//     .then(repsonse => response.json())
//     .then(result => {
//       console.log(result);
//       // Post is liked, change button to 'unlike'
//       if ('li' in result) {
//         document.querySelector(`#like-btn-${post_id}`).innerHTML = 'Unlike';
//       }
//       else if ('ul' in result) {
//         document.querySelector(`#unlike-btn-${post_id}`).innerHTML = 'like';
//       }
//     })
//   });
// }

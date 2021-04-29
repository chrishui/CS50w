// Edit posts
function edit(post_id) {
  var edit_box = document.querySelector(`#edit-box-${post_id}`);
  var edit_btn = document.querySelector(`#edit-btn-${post_id}`);
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
    edit_box.style.display = 'none';
    edit_btn.style.display = 'none';

    document.querySelector(`#post-${post_id}`).innerHTML = edit_box.value;

  });

}

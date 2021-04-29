document.addEventListener('DOMContentLoaded', function() {
  // Test
  document.querySelector('#test-count').onclick = count;

  // Hide editor by default?
  // document.querySelector('#editor-view').style.display = 'none';

  // Use button to toggle post view
  // TODO
  document.querySelector('#editor').addEventListener('click', () => load_editor());

});

// Test
let counter = 0;
function count() {
  counter++;
  document.querySelector('#test').innerHTML = counter;
}

// Post editor
// TODO
function load_editor() {
  document.querySelector('#editor-view').style.display = 'block';
}

// Display posts

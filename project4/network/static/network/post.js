document.addEventLister('DOMContentLoaded', function() {

  document.querySelector('#button-test').onclick = count;

  // Hide editor by default?
  // document.querySelector('#editor-view').style.display = 'none';

  // Use button to toggle post view
  document.querySelector('#editor').addEventListener('click', () => load_editor());

  document.querySelector('#test').addEventListener('click', () => test());

  test();





});

// Post editor
function load_editor() {
  document.querySelector('#editor-view').style.display = 'block';
  document.querySelector('#editor-view').innerHTML = `<h3>test</h3>`;
}

// Test
function test() {
  document.querySelector('#editor-view').style.display = 'none';
  document.querySelector('#emails-view').innerHTML = `<h3>Test!!</h3>`;
}

let counter = 0
function count() {
  counter ++;
  document.querySelector('#counter-test').innerHTML = counter;
}

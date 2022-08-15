// ----------- edit post ------------

function toggle_content_ui(postId) {
  let editButtonEl = document.querySelector(`#edit_post_button_${postId}`);
  let postContentEl = document.querySelector(`#post_content_${postId}`);
  let postContentFormEl = document.querySelector(`#edit_post_form_${postId}`);
  let postContentTextareaEl = postContentFormEl.querySelector('textarea');
  if (editButtonEl.disabled) {
    editButtonEl.disabled = false;
    postContentEl.style.display = "block"
    postContentFormEl.style.display = "none"
  } else {
    editButtonEl.disabled = true;
    postContentEl.style.display = "none"
    postContentFormEl.style.display = "block"
    postContentTextareaEl.value = postContentEl.innerHTML.trim()
    
    let selection = postContentTextareaEl.value.length
    postContentTextareaEl.setSelectionRange(selection,selection)
    postContentTextareaEl.focus() 
  }
}

function edit(event,postId) {
  event.preventDefault()
  let postContentEl = document.querySelector(`#post_content_${postId}`);
  let postContentFormEl = document.querySelector(`#edit_post_form_${postId}`);
  let postContentTextareaEl = postContentFormEl.querySelector('textarea');
  let fieldsetEl = postContentFormEl.querySelector('fieldset');
  fieldsetEl.disabled = true;
  fetch("/post/edit", {
    method: "post",
    body: JSON.stringify({
      post_id: postId,
      content: postContentTextareaEl.value,
    }),
  })
    .then((res) => {
      if (res.status == 200) {
        postContentEl.innerHTML = postContentTextareaEl.value.trim()
      }

      fieldsetEl.disabled = false;
      toggle_content_ui(postId)
    })
    .catch((e) => {
      console.log(e)
      fieldsetEl.disabled = false;
      toggle_content_ui(postId)
    });
}

// ----------- like ------------

function like(button, postId) {
  toggle_like_ui(button);
  button.disabled = true;
  fetch("/like", {
    method: "post",
    body: JSON.stringify({
      id: postId,
    }),
  })
    .then((res) => {
      if (res.status != 200) {
        toggle_like_ui(button);
      }
      button.disabled = false;
    })
    .catch((e) => {
      console.log(e)
      button.disabled = false;
    });
}

function toggle_like_ui(button) {
  iconEl = button.querySelector(".fa-heart");
  countEl = button.querySelector(".likes_count");
  if (button.querySelector(".fa-heart").classList.contains("fa-solid")) {
    countEl.innerHTML = `${parseInt(countEl.innerHTML) - 1}`;
    iconEl.classList.remove("fa-solid", "text-danger");
  } else {
    countEl.innerHTML = `${parseInt(countEl.innerHTML) + 1}`;
    iconEl.classList.add("fa-solid", "text-danger");
  }
}


// ----------- follow ------------

function follow(button, userId) {
  toggle_follow_ui(button);
  button.disabled = true;
  fetch("/follow", {
    method: "post",
    body: JSON.stringify({
      id: userId,
    }),
  })
    .then((res) => {
      if (res.status != 200) {
        toggle_follow_ui(button);
      }
      button.disabled = false;
    })
    .catch((e) => {
      console.log(e)
      button.disabled = false;
    });
}

function toggle_follow_ui(button) {
  let followers = document.querySelector("#followers")
  if (button.innerHTML.trim() == 'Follow') {
    button.innerHTML = 'Unfollow';
    followers.innerHTML = `${parseInt(followers.innerHTML) + 1}`
  } else {
    button.innerHTML = 'Follow';
    followers.innerHTML = `${parseInt(followers.innerHTML) - 1}`
  }
}
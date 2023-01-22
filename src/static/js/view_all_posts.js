function like(postId){
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const upButton = document.getElementById(`up-button-${postId}`);
    const downButton = document.getElementById(`down-button-${postId}`)

    console.log(likeCount.value);

    fetch(`/like-post/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      likeCount.innerHTML = data["likes"];

      if (data["liked"] === true) {
        upButton.className = "fas fa-caret-square-up fa-3x";
        downButton.className = "far fa-caret-square-down fa-3x"
      } else {
        upButton.className = "far fa-caret-square-up fa-3x";
        downButton.className = "fas fa-caret-square-down fa-3x"
      }
      
    })
    .catch((e) => alert("Could not like post. You need to Login!"));
}
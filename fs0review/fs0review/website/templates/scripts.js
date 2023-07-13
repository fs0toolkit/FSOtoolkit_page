function addComment() {
    var nameInput = document.getElementById("name-input");
    var commentInput = document.getElementById("comment-input");
    var nameText = nameInput.value.trim();
    var commentText = commentInput.value.trim();

    if (nameText !== "" && commentText !== "") {
        var commentList = document.getElementById("comment-list");
        var newComment = document.createElement("li");
        var userElement = document.createElement("span");
        userElement.className = "comment-user";
        userElement.innerText = nameText + ": ";
        var contentElement = document.createElement("span");
        contentElement.className = "comment-content";
        contentElement.innerText = commentText;
        newComment.appendChild(userElement);
        newComment.appendChild(contentElement);
        commentList.appendChild(newComment);
        nameInput.value = "";
        commentInput.value = "";
    }
}
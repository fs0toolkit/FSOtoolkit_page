function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  }).catch((error) => {
    // Handle the error here, for example, log it or show a message to the user
    console.error('Error deleting note:', error);
  });
}

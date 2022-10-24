document.getElementById('id_show_answer').addEventListener('click', function () {
    document.getElementById('id_question').hidden = true;
    document.getElementById('id_show_answer').hidden = true;
    document.getElementById('id_answer').hidden = false;
    document.getElementById('id_next_question').hidden = false;
})
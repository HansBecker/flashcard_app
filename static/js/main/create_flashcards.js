const newEditor = (element) => {
    var toolbarOptions = [['bold', 'italic', 'underline', 'strike'], ['blockquote', 'code', 'code-block'], ['image']];
    var options = {
        theme: 'snow',
        modules: {
            toolbar: toolbarOptions,
        },
        placeholder: "",
        readOnly: false,
    };

    var editor = new Quill(element, options);
}

$("#id_flashcard_form").submit(function (e) {
    let editors = document.getElementsByClassName('editor')
    for (let i = 0; i < editors.length; i++) {
        let for_id = editors[i].getAttribute('for')
        let textarea = document.getElementById(for_id)
        textarea.innerHTML = editors[i].children[0].innerHTML;
    }
})

const deleteExistingFlashcard = (element, flashcard_id) => {
    element.parentElement.parentElement.remove();
    $.ajax({
        type: 'POST',
        url: url_delete_flashcard,
        data: {
            'flashcard_id': flashcard_id,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        },
        onsuccess: function (data) {
            console.log('worked')
        }
    })
}

const initEditors = (form_number) => {
    newEditor(document.getElementById(`id_question_editor_${form_number}`));
    newEditor(document.getElementById(`id_answer_editor_${form_number}`));
}

const deleteFormRow = (element) => {
    element.parentElement.parentElement.remove();
    decrementForms();
    updateFormIds();
}

const addRow = () => {
    let form_number = totalForms();
    document.getElementById('flashcard-container').innerHTML += flashCardRow(form_number);
    initEditors(form_number);
    incrementForms();
}

const flashCardRow = (form_number) => {
        return `
        <div>
            <div class="row mb-3 flashcard-row">
                <div class="col-6 mb-3">
                    <div>
                        <div 
                            id="id_question_editor_${form_number}" 
                            class="editor"
                            for="id_form-${form_number}-question">
                            
                        </div>
                        <textarea
                            id="id_form-${form_number}-question"
                            name="form-${form_number}-question"
                            class="d-none"></textarea>
                    </div>
                </div>
                <div class="col-6 mb-3">
                    <div>
                        <div 
                            id="id_answer_editor_${form_number}" 
                            class="editor"
                            for="id_form-${form_number}-answer">
                            
                        </div>
                        <textarea
                            id="id_form-${form_number}-answer"
                            class="d-none"
                            name="form-${form_number}-answer"></textarea>
                    </div>
                </div>
            </div>
            <div class="mb-3">
                <a type="button" class="btn btn-outline-danger delete-button" onclick="deleteFormRow(this)">Delete</a>
            </div>
            <hr>
        </div>
        `
}

const totalForms = () => {
    return parseInt(document.getElementById('id_form-TOTAL_FORMS').value)
}

const incrementForms = () => {
    var nForms = totalForms();
    document.getElementById('id_form-TOTAL_FORMS').value = nForms + 1
}

const decrementForms = () => {
    var nForms = totalForms();
    document.getElementById('id_form-TOTAL_FORMS').value = nForms - 1
}

const updateFormIds = () => {
    var question_fields = document.getElementsByClassName('question-editor');
    var n_fields = question_fields.length;
    for (let i = 0; i < n_fields; i++){
        question_fields[i].setAttribute('name', `form-${i}-question`);
        question_fields[i].setAttribute('id', `id_form-${i}-question`);
    }
    var answer_fields = document.getElementsByClassName('answer-editor');
    for (let i = 0; i < n_fields; i++){
        answer_fields[i].setAttribute('name', `form-${i}-answer`);
        answer_fields[i].setAttribute('id', `id_form-${i}-answer`);
    }

}





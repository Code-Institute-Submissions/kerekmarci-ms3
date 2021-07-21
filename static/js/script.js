const ingredientInputContainer = document.getElementById("ingredientInputContainer");
const ingredientsInput = document.getElementsByName("ingredients");
const methodInputContainer = document.getElementById("methodInputContainer");
const methodInput = document.getElementsByName("method");

function addField(container, inputName) {
    event.preventDefault();
    let input = document.createElement("input");
    input.type = "text";
    input.name = inputName;
    input.className = "form-control mt-3";
    input.required = true;
    container.appendChild(input);
}

function removeField(container) {
    event.preventDefault();
    container.removeChild(container.lastChild);
}
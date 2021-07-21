const ingredientInputContainer = document.getElementById("ingredientInputContainer");
const ingredientsInput = document.getElementsByName("ingredients");
const methodInputContainer = document.getElementById("methodInputContainer");
const methodInput = document.getElementsByName("method");
const receipeName = document.getElementById("recipename");


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

function maxInput(formId, maxChar, outputName) {
    var name = document.getElementById(formId).value;
    let remainingChar = maxChar-name.length;
    if (remainingChar < 6) {
        document.getElementById(outputName).innerHTML = remainingChar + " characters left";
        remainingChar == 0 ? document.getElementById(outputName).style.color = "#DC3545" : document.getElementById(outputName).style.color = "#212529";
    } else {
        document.getElementById(outputName).innerHTML = "";
    }
}
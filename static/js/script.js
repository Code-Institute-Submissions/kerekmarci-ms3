let ingredientInputContainer = document.getElementById("ingredientInputContainer");
let ingredientsInput = document.getElementsByName("ingredients");
let methodInputContainer = document.getElementById("methodInputContainer");
let methodInput = document.getElementsByName("method");
firstIngredient = ingredientInputContainer.children[1];
firstMethod = methodInputContainer.children[1];

function addIngredientField() {
    event.preventDefault();
    let input = document.createElement("input");
    input.type = "text";
    input.name = "ingredients";
    input.className = "form-control mt-3";
    input.required = true;
    ingredientInputContainer.appendChild(input);    
}

function removeIngredientField() {
    event.preventDefault();
    ingredientInputContainer.removeChild(ingredientInputContainer.lastChild);
}

function addMethodField() {
    event.preventDefault();
    let input = document.createElement("input");
    input.type = "text";
    input.name = "method";
    input.className = "form-control mt-3";
    input.required = true;
    methodInputContainer.appendChild(input);    
}

function removeMethodField() {
    event.preventDefault();
    methodInputContainer.removeChild(methodInputContainer.lastChild);
}
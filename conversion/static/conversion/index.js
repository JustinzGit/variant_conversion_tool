document.addEventListener("DOMContentLoaded", function() {
    variant_form = document.getElementById("variant_form")
    coding_button = document.getElementById("coding_button")
    protein_button = document.getElementById("protein_button")

    // If coding button is clicked submit form to protein view
    coding_button.addEventListener("click", function() {
        variant_form.addEventListener("submit", function() {
            variant_form.setAttribute("action", "protein")
        })
    })

    // If protein button is clicked submit form to coding view
    protein_button.addEventListener("click", function() {
        variant_form.addEventListener("submit", function() {
            variant_form.setAttribute("action", "coding")
        })
    })
})
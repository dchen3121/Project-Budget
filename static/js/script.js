income_button = document.getElementById('radioIncome');
expense_button = document.getElementById('radioExpenditure');
category_select = document.getElementById('category');

income_button.addEventListener('click', function () {
    expenses = document.querySelectorAll('.exp-option');
    for (var i = 0; i < expenses.length; i++) {
        expenses[i].style.display = "none";
    }
    income = document.querySelectorAll('.income-option');
    for (var i = 0; i < income.length; i++) {
        income[i].style.display = "block";
    }
    category_select.value = "";
})
expense_button.addEventListener('click', function () {
    income = document.querySelectorAll('.income-option');
    for (var i = 0; i < income.length; i++) {
        income[i].style.display = "none";
    }
    expenses = document.querySelectorAll('.exp-option');
    for (var i = 0; i < expenses.length; i++) {
        expenses[i].style.display = "block";
    }
    category_select.value = "";
})
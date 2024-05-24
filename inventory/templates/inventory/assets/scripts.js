
function dropdownmenu(products) {
    var datalist = document.getElementById("browsers");
    datalist.innerHTML = ""; // Clear previous options

    if (Array.isArray(products) && products.length > 0) {
        products.forEach(function (product) {
            var option = document.createElement("option");
            option.value = product.name;
            datalist.appendChild(option);
        });
    } else {
        var messageOption = document.createElement("option");
        messageOption.text = "Данные о товарах не найдены";
        datalist.appendChild(messageOption);
    }
}


function loadProductsByDates() {
    var startDate = document.getElementById("start_date").value;
    var endDate = document.getElementById("end_date").value;

    fetch(`/api/products/?start_date=${startDate}&end_date=${endDate}`)
        .then(response => response.json())
        .then(data => {
            console.log(data); // Проверяем, что получен корректный JSON
            displayProducts(data); // Отображаем полученные данные
        })
        .catch(error => console.error('Ошибка при загрузке данных:', error));
}

function myFunction() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("inventoryTable")
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            }
            else {
                tr[i].style.display = "none";
            }
        }
    }
}

function loadProducts() {
    fetch('/api/products/')
        .then(response => response.json())
        .then(data => {
            let products = data;
            dropdownmenu(data);
            //console.log(data);
            displayProducts(data);
            // Отображаем полученные данные
        })
        .catch(error => console.error('Ошибка при загрузке данных:', error));
    console.log(products);
    return (products)
}

function displayProducts(products) {
    var tableBody = document.getElementById("inventoryBody");
    tableBody.innerHTML = "";

    // Проверяем, что products - это массив и он не пустой
    if (Array.isArray(products) && products.length > 0) {
        products.forEach(function (product) {
            var row = "<tr>" +
                "<td>" + product.name + "</td>" +
                "<td>" + product.description + "</td>" +
                "<td>" + product.quantity + "</td>" +
                "<td>" + product.price + "</td>" +
                "</tr>";
            tableBody.innerHTML += row;
        });
    } else {
        var messageRow = "<tr><td colspan='4'>Данные о товарах не найдены</td></tr>";
        tableBody.innerHTML = messageRow;
    }
}
// Функция для отправки формы
function submitForm() {
    var form = document.getElementById("yourForm"); // Замените "yourForm" на ID вашей формы
    var formData = new FormData(form);

    fetch("api/add_product/", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (response.ok) {
            showNotification("Товар успешно добавлен");
            loadProducts();
            form.reset(); // Очистить форму после успешной отправки
        } else {
            throw new Error("Ошибка при добавлении товара");
        }
    })
    .catch(error => console.error("Ошибка:", error));
}

// Функция для отображения уведомления
function showNotification(message) {
    var notification = document.getElementById("notification");
    notification.innerHTML = message;
    notification.classList.add("show");
    setTimeout(function () {
        notification.classList.remove("show");
    }, 3000); // Скрыть уведомление через 3 секунды (или другой необходимый интервал)
}
loadProducts();
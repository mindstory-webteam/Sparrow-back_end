// ✅ Fix: Ensure logout nav item uses POST or direct redirect
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("a[href*='logout']").forEach(function (el) {
        el.addEventListener("click", function (e) {
            e.preventDefault();
            // Submit a logout form via POST (Django requires POST for logout)
            const form = document.createElement("form");
            form.method = "POST";
            form.action = "/admin/logout/";
            const csrf = document.createElement("input");
            csrf.type = "hidden";
            csrf.name = "csrfmiddlewaretoken";
            csrf.value = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || "";
            form.appendChild(csrf);
            document.body.appendChild(form);
            form.submit();
        });
    });
});
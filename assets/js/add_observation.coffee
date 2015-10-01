document.addEventListener "DOMContentLoaded", ->
    current_jd = +document.getElementById("current-jd").textContent
    document.getElementById("id_jd").value = current_jd

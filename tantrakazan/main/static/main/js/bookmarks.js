$(document).ready(function () {
  $("#bookmark-form").submit(function (event) {
    event.preventDefault();

    var form = $(this);
    var url = form.attr("action");

    $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(),
      dataType: "json",
      success: function (data) {
        // Обновите отображаемые результаты на странице
        $("#bookmark-data").val(data.result);
        $("#bookmark-count").text(data.count); // Обновление количества

        // Обновите изображение на кнопке
        var button = $("#bookmark-button");
        if (data.result) {
          button.attr("src", "/static/main/images/bookmark-on-icon.png");
          button.attr("alt", "Удалить из закладок");
        } else {
          button.attr("src", "{% static 'main/images/bookmark-off-icon.png' %}");
          button.attr("alt", "Добавить в закладки");
        }
      },
      error: function (xhr, textStatus, errorThrown) {
        // Обработка ошибки, если не удалось отправить запрос
        console.error("Произошла ошибка: " + errorThrown);
      }
    });
  });
});

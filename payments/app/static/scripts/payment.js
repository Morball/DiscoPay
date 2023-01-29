let pid = 0;
let discord = "";

function create_subscription(pid, username, days) {

  $.ajax({
    type: "POST",
    url: `http://127.0.0.1:5000/api/v1/subscriptions/create`,
    headers: { "content-type": "application/json" },
    data: JSON.stringify({ "payment_id": pid, "discord": username, "days": days }),
    success: function (data) {
      window.location = "http://127.0.0.1:5000/success";
    },
    error: function () {

      window.location = "http://127.0.0.1:5000/cancelled";

    }



  });





}



function check_payment() {

  $.ajax(
    {
    type: "GET",
    url: `http://127.0.0.1:5000/api/v1/payments/${pid}`,
    dataType: 'json',
    success: function (response) {
      jsonObj = $.parseJSON(response);
      if (jsonObj["payment_status"] == "confirmed") {
        clearInterval(countdown);
        create_subscription(jsonObj["payment_id"], discord, 30)
      }
      else if (jsonObj["payment_status"] == "cancelled") {
        window.location = "http://127.0.0.1:5000/cancelled";

      }
      
  }}
  );


}





function create_timer() {

  var count = 1200; // start the timer at 20 minutes (1200 seconds)
  let countdown = setInterval(function () {
    count--; // decrease the count by 1 every second

    if (count == 1) {
      clearInterval(countdown);
      window.location = "http://127.0.0.1:5000/cancelled";
    } else {
      var minutes = Math.floor(count / 60);
      var seconds = count % 60;
      if (seconds < 10) {
        document.getElementById("time").innerHTML = `00:${minutes}:0${seconds}`
      }
      else {
        document.getElementById("time").innerHTML = `00:${minutes}:${seconds}`

      }


    }
    check_payment();

  }, 1000); // run the countdown function every 1000 milliseconds (1 second)


}

$(document).ready(function () {
  $(".box-payment").hide();

});

$(".submit-discord").click(function () {
  discord = $(".discord-tag").val()

  if (discord !== "" && discord.match("^.{3,32}#[0-9]{4}$")) {



    data = {
      "price": 30
    }
    $.ajax({
      url: "http://127.0.0.1:5000/api/v1/payments/",
      type: "POST",
      data: JSON.stringify(data),
      headers: { "Content-Type": "application/json" },
      dataType: 'json',



      success: function (response) {
        var jsonObject = $.parseJSON(response);
        $('#ada-amount').html(`${jsonObject["pay_amount"]} ADA`)
        $("#address").html(jsonObject['pay_address']);
        pid = jsonObject['payment_id'];
        create_timer();
      },



      error: function () { alert("sa-mi bag pula in ma-ta ca nu merge") }

    });
    $(".discord-box").hide();
    $(".box-payment").show();



  }



});
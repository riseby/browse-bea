  var beaRegex = /b[eéè][aáà]/gi;
  var beaDishExeption =  new Map([
    ['Londoner', /black angus|burgare/gi]
  ])
  var hideDishes = false

  var jsonLunchData = "";
  var jsonAddData = "";

  function isBeaDish(dishText, restaurant){
    return dishText.match(beaRegex)
  }

  function isExceptionDish(dishText, restaurant){
    var pattern = beaDishExeption.get(restaurant)
    if(pattern){
      return dishText.match(pattern)
    } else {
      return false
    }
  }

  $.getJSON("data/lunchData.txt", function(json) {
    jsonLunchData = json
    var tempD = json.additionalData.dates[0]
    visualizeLunchDate(jsonLunchData, tempD)

  });

  $.getJSON("data/addData.txt", function(json) {
    jsonAddData = json
    json.dates.forEach(function(d){
      var a = document.createElement("a")
      a.id = d.date
      a.className = "nav-item nav-link text-secondary"
      a.href = "#"
      a.dataset.toggle = "tab"
      a.role = "tab"
      a.appendChild(document.createTextNode(getDayNameOrTodayMenu(d.date)))
      document.getElementById("navDays").appendChild(a)
    })
    var c = document.getElementById("navDays").children[0].className += " active"
    addListener(jsonAddData)
  })

  function addListener(json){
    json.dates.forEach(function(d){
      $("#" + d.date).click(function(){ visualizeLunchDate(jsonLunchData,d) })
    })
  }

  function getHolidayByDateInJson(data, date) {
    return data.filter(
      function(data){return data.date == date }
    );
  }

  function capitalizeFirstLetter(string) {
    return string[0].toUpperCase() + string.slice(1);
  }

  function clearDomLunchDate(){
    document.getElementById("houseColumns").innerHTML = ""
    document.getElementById("dayTitle").innerHTML = ""
    document.getElementById("dayHeader").innerHTML = ""
  }

  function getDayNameOrToday(inputDate){
      var options = { weekday: 'long'};
      var day = new Date(inputDate).toLocaleDateString("sv-SE",options)
      var today = new Date().toLocaleDateString("sv-SE",options)
      if(day == today){
        return "dag"
      } else {
        return day
      }

  }

  function getDayNameOrTodayMenu(inputDate){
      var options = { weekday: 'long'};
      var day = new Date(inputDate).toLocaleDateString("sv-SE",options)
      var today = new Date().toLocaleDateString("sv-SE",options)
      if(day == today){
        return "idag"
      } else {
        return day
      }

  }

  function visualizeLunchDate(json, inputDate){
    clearDomLunchDate()
    setBeaLogoColors(false)
    var bDay = false
    var options = { weekday: 'long'};
    var options2 = { weekday: 'long', month: 'long', day: 'numeric' };
    document.getElementById("dayTitle").innerHTML = capitalizeFirstLetter(getDayNameOrToday(inputDate.date)) + "ens"
    document.getElementById("dayHeader").innerHTML+=" " + new Date(inputDate.date).toLocaleDateString("sv-SE",options2) + " "

      document.getElementById("timestamp").innerHTML=json.created
      json.houses.forEach(function(e){
          var card = document.createElement("div")
          card.className="card shadow"

          var cardBody = document.createElement("div")
          cardBody.className = "card-body"

          var cardTitle = document.createElement("div")
          cardTitle.className = "card-header"

          var textnode = document.createTextNode(e.house)

          var cardBody2 = document.createElement("div")
          cardBody2.className = "card-body"
          var a = document.createElement("a")
          a.href = e.url
          a.target = "_blank"
          a.className = "text-secondary"
          a.appendChild(document.createTextNode("Till menyn"))

          var list = document.createElement("ul")
          list.className = "list-group list-group-flush"

          if(!hideDishes && e.dishesPerDate[inputDate.date]){
            e.dishesPerDate[inputDate.date].forEach(function(d){
              var li = document.createElement("li")
              var text = document.createTextNode(d + " ")
              li.className = "list-group-item"
              if(!isExceptionDish(d, e.house)){
                li.appendChild(text)
                if (isBeaDish(d, e.house)) {
                  bDay = true
                  var beaBadge = document.createElement("span")
                  beaBadge.className = "badge badge-warning"
                  var text = document.createTextNode("BEA!")
                  beaBadge.appendChild(text)
                  li.appendChild(beaBadge)
                }
                list.appendChild(li)
              }
            });
          } else {
            var li = document.createElement("li")
            li.className = "list-group-item"
            var text = document.createTextNode("Information saknas")
            li.appendChild(text)
            list.appendChild(li)
          }

          cardTitle.appendChild(textnode)
          cardBody2.appendChild(a)
          card.appendChild(cardTitle)
          card.appendChild(list)
          card.appendChild(cardBody2)
          document.getElementById("houseColumns").appendChild(card)
    });
    var foundHoliday = getHolidayByDateInJson(json.additionalData.dates,inputDate.date)
    if(foundHoliday != null && foundHoliday[0].holiday != null){
      var holidayBadge = document.createElement("span")
      holidayBadge.className = "badge badge-danger"

      var textnode = document.createTextNode(foundHoliday[0].holiday)
      holidayBadge.appendChild(textnode)
      document.getElementById("dayHeader").appendChild(holidayBadge)
      setBeaLogoColors('h')
    }

    if(bDay){
      var beaBadge = document.createElement("span")
      beaBadge.className = "badge badge-warning"

      var textnode = document.createTextNode("Bearnaisesås!")
      beaBadge.appendChild(textnode)
      document.getElementById("dayHeader").appendChild(beaBadge)
      setBeaLogoColors('b')
    }
  }

  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

function ready(callback){
    // in case the document is already rendered
    if (document.readyState!='loading') {
      // modern browsers
      callback();
    } else if (document.addEventListener) {
      // IE <= 8
      document.addEventListener('DOMContentLoaded', callback);
    } else {
      document.attachEvent('onreadystatechange', function(){
          if (document.readyState=='complete') {
            callback();
          }
      });
    }
}

sizecell = 90;
sizecellh = 50;
fieldsofimport = [];

doAjax = function(url, cb){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      let data = JSON.parse(this.response);
      cb(data);
    }
  }
  xhttp.open("GET", url, true);
  xhttp.send();
}

doAjaxPost = function(url, data, cb){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      let data = JSON.parse(this.response);
      cb(data);
    }
  }
  xhttp.open("POST", url, true);
  xhttp.send(data);
}


let shadow
function dragit(event){
  shadow=event.target;
}

function dragover(e){
  let children=Array.from(e.target.parentNode.parentNode.children);
  if (e.target.parentNode.parentNode.id != "draggabletr") {
    return false;
  }

  if (children.indexOf(e.target.parentNode)>children.indexOf(shadow)) {
    e.target.parentNode.after(shadow);
  } else {
    e.target.parentNode.before(shadow);
  }
}


let load = function(){
  let result = document.getElementById("result");
  let file = document.getElementById("file");
  let drtr = document.getElementById("draggabletr");
  let chtr = document.getElementById("checktr");

  outfields = [];
  let i = 0;

  for (let child of drtr.children) {
    if (chtr.children.item(i).children.length > 0) {
      if (chtr.children.item(i).children.item(0).checked){
        outfields.push({from: chtr.children.item(i).children.item(0).name, to: drtr.children.item(i).children.item(0).innerHTML})
      }
    }
    i += 1;
  }


  let data = new FormData();

  data.append("filerun", file.value);

  for (let i of outfields){
    data.append(i.to, i.from);
  }

  doAjaxPost("/catalog/in/", data, function(data){
      if (data.finished) {
        result.innerHTML = "Готово!";
        setTimeout(function(){
            result.innerHTML = "";
        }, 2000)
      }
  });
}

/*
function dblclicked(e){
  e.target.innerHTML = '<input type="text" value="' + e.target.innerHTML + '" onfocusout="focusouted(event)"></input>';
}

function focusouted(e){
  e.target.parentNode.innerHTML = e.target.value;
}
*/

ready(function(){
    const elem = document.getElementById("run");
    const clear = document.getElementById("clear");
    const file = document.getElementById("file");
    const fields = document.getElementById("fields");

    if (elem) {
      elem.addEventListener('click', function(){
        let data = new FormData();
        data.append("file", file.value);

        doAjaxPost("/catalog/in/", data, function(data){
            let max = Math.max(data['fields-config'].length, data['fields-file'].length);

            html = "<table class='fields-table'><tr><td class='tdtitle'>Свойства каталога:</td>";

            for (item of data["fields-config"]) {
                html += "<td class='table-item'><div class='field-item row-second'><label>'" + item + "'</label></div></td>"
            }

            if (data["fields-config"].length < max) {
              for (let i=data["fields-config"].length;i<max; i += 1){
                  html += "<td></td>"
              }
            }

            html += "</tr><br/><tr id='draggabletr'><td class='tdtitle'>Свойства файла:</td>"

            for (item of data["fields-file"]) {
                html += "<td class='table-item' draggable='true' ondragstart='dragit(event)' ondragover='dragover(event)' ondblclick='dblclicked(event)'>'<label>" + item + "</label>'</td>"
                fieldsofimport.push(item)
            }

            if (data["fields-file"].length < max) {
              for (let i=data["fields-file"].length;i<max; i += 1){
                  html += "<td></td>"
              }
            }

            html += "</tr><tr id='checktr' class='rowcheck'><td></td>"
            for (item of data["fields-config"]) {
                html += "<td class='table-item'><input type='checkbox' checked='true' name='"+item+"'></input></td>"
            }

            if (data["fields-config"].length < max) {
              for (let i=data["fields-config"].length;i<max; i += 1){
                  html += "<td></td>"
              }
            }

            html += "</tr></table><input id='load' type='submit' value='Загрузить' onclick='load()'></input>"

            fields.innerHTML = html;
        })
      });
    }

    if (clear) {
      clear.addEventListener('click', function(){
          let data = new FormData();
          data.append("clear", true);

          doAjaxPost("/catalog/in/", data, function(data){
            location.reload();
          })
      });
    }
  });

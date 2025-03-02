let AjaxService = {
  doAjax: function(url, cb){
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        let data = JSON.parse(this.response);
        cb(data);
      }
    }

    xhttp.open("GET", url, true);
    xhttp.send();
  },
  doAjaxPost: function(url, data, cb){
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
}

export { AjaxService };

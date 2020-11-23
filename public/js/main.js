var url_count = 1;
let url_list = [];
function make_delete_div() {
    const url = document.getElementById('url').value;
    save_url(url);
    var heder = document.getElementById('heder');
    var make_container = document.createElement('div');
    var make_div = document.createElement('div');
    var make_x_btn = document.createElement('button');

    make_x_btn.innerHTML = "X";
    make_div.innerHTML = url;

    make_div.setAttribute("class", "url-div");
    make_x_btn.setAttribute("id", "x_button");
    make_x_btn.onclick=function(){
        con = this.parentNode;
        pa = con.parentNode;
        pa.removeChild(con);
        delete_url(url);
    };
    if (document.getElementById("container" + url_count)){url_count += 1;}
    make_container.setAttribute("id", "container" + url_count);
    make_container.setAttribute("class", "con");

    heder.appendChild(make_container);
    var con = document.getElementById('container' + url_count);
    con.appendChild(make_div);
    con.appendChild(make_x_btn);
    
    document.getElementById('url').value = null;
}

function save_url(url) {
    url_list.push(url);
}

function delete_url(url) {
    url_list.splice(url_list.indexOf(url),1);
}

function print_url() {
   url = url_list[0] + ' ' + url_list[1];
   alert(url);
}

function result_page() {
    var urlForm = document.send_url;
    urlForm.have_url.value = url_list;
    urlForm.submit();
}


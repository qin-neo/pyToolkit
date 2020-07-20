function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

var xmlHttp = new XMLHttpRequest();
function post_url_ID_content(url, content) {
    xmlHttp.open("POST", url, true);
    xmlHttp.setRequestHeader('X-CSRFToken',getCookie('_xsrf'));
    xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    //value=encodeURIComponent(value); 
    xmlHttp.send(content)
    window.location.reload(false);   
}

function get_offset(el) {
    var rect = el.getBoundingClientRect(),
    scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
    scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    return { top: rect.top + scrollTop, left: rect.left + scrollLeft }
}

function create_textarea(url, parent_node,stock_id,key,default_text) {
    var input_text = document.createElement('textarea');
    parent_node.appendChild(input_text);
    input_text.type = 'text';
    input_text.style.display = 'none';
    input_text.style.backgroundColor = 'transparent';
    input_text.stock_id = stock_id;
    input_text.key = key;
    if (default_text) {input_text.value = default_text;}
    input_text.addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode == 13) {post_url_ID_content(url,'id='+this.stock_id+'&key='+this.key+'&value='+encodeURIComponent(this.value));}
    });
    return input_text;
}

function create_dropdown(url, parent_node, option_list, stock_id, default_val) {
    var tmp_td = document.createElement('td');
    parent_node.appendChild(tmp_td);
    var tmp_s = document.createElement('select');
    tmp_td.appendChild(tmp_s);
    for (var iii=0;iii<option_list.length;iii++) {
        var tmp_o = document.createElement('option');
        tmp_s.appendChild(tmp_o);  
        tmp_o.value = iii;
        tmp_o.innerHTML = option_list[iii];
    }
    tmp_s.selectedIndex  = option_list.indexOf(default_val)//default_val;
    tmp_s.stock_id = stock_id;
    tmp_s.onchange = function () {post_url_ID_content(url,'id='+this.stock_id+'&key=action&value='+option_list[this.value]);}
}

var var_str_title ="沪深~名字~代码~当前~昨收~今开~成交量~外盘~内盘~买5~买5量~买4~买4量~买3~买3量~买2~买2量~买1~买1量~卖1~卖1量~卖2~卖2量~卖3~卖3量~卖4~卖4量~卖5~卖5量~最近逐笔~时间~涨_跌~涨跌%~最_高~最_低~价格/量手/额~成交_手~成交万~换手率~市盈率~~最-高~最-低~振幅%~流通市值~总市值~市净率~涨停价~跌停价~";
var var_show_keys = "名字~当前~涨跌%~换手率~成交万~振幅%~流通市值~总市值~市净率~市盈率~";
var all_keys_list = var_str_title.replace(/~~/g, "~-~").match(/([^~]+)/g);
var show_keys_list = var_show_keys.replace(/~~/g, "~-~").match(/([^~]+)/g);

function insert_web_url(parent_node, s_text, web_url, s_width) {
    var tmp_td = document.createElement('td');
    tmp_td.innerHTML = '<a href="'+web_url+'" target="_blank">'+s_text+'</a>';
    if (s_width){
        tmp_td.style.width = s_width;
    }else{
        tmp_td.style.paddingLeft = '10px';
    }
    parent_node.appendChild(tmp_td);
    return tmp_td;
}

function tr_append_td(parent_node, s_text, s_width) {
    var tmp_td = document.createElement('td');
    if (s_width){
        tmp_td.style.width = s_width;
    }else{
        tmp_td.style.paddingLeft = '10px';
    }
    tmp_td.innerHTML = s_text;
    parent_node.appendChild(tmp_td);
    return tmp_td;
}

function tr_append_del_follow(url, parent_node, identifier) {
    var div_add = document.createElement('td');
    parent_node.appendChild(div_add);
    div_add.innerHTML = 'Follow';
    div_add.style.display = 'none';
    div_add.style.width = '2em';
    div_add.identifier = identifier;

    var div_del = document.createElement('td');
    parent_node.appendChild(div_del);
    div_del.innerHTML = 'DEL';
    div_del.style.display = 'none';
    div_del.style.width = '2em';
    div_del.identifier = identifier;

    var tmp_td = document.createElement('td');
    parent_node.appendChild(tmp_td);
    tmp_td.innerHTML = 'M';
    tmp_td.style.width = '2em';
    tmp_td.div_del = div_del;
    tmp_td.div_add = div_add;
    div_del.onclick = function(){post_url_ID_content(url,'id='+this.identifier+'&key=delete');};
    div_add.onclick = function(){post_url_ID_content(url,'id='+this.identifier+'&key=follow');};
    tmp_td.onclick = function(){this.div_del.style.display = 'table-cell';this.div_add.style.display = 'table-cell';this.style.display = 'none';};
}

var img_down_right = document.getElementById('img_down_right');
function attach_down_right_img(parentNode,img0_path,img1_path,img2_path) {
    if (!img_down_right) {
        img_down_right = document.createElement('img');
        img_down_right.id = 'img_down_right';
        document.body.appendChild(img_down_right);
        img_down_right.className = 'down-right';
    }
   var img0= document.createElement('img');
   parentNode.appendChild(img0);
   img0.src_bak = img0_path;
   img0.className='down-right-bottom';
   img0.style.display = 'none';
   parentNode.img0 = img0;

   var img1= document.createElement('img');
   parentNode.appendChild(img1);
   img1.src_bak = img1_path;
   img1.className='down-right';
   img1.style.display = 'none';
   parentNode.img1 = img1;

   var img2= document.createElement('img');
   parentNode.appendChild(img2);
   img2.src_bak = img2_path;
   img2.className='down-right-right';
   img2.style.display = 'none';
   parentNode.img2 = img2;

    parentNode.onmouseover=function(e) {
        this.img0.src=this.img0.src_bak;
        this.img0.style.display = 'block';
        this.img1.src=this.img1.src_bak;
        this.img1.style.display = 'block';
        this.img2.src=this.img2.src_bak;
        this.img2.style.display = 'block';}
    parentNode.onmouseout = function(e) {
        this.img0.style.display = 'none';
        this.img0.src='';
        this.img1.style.display = 'none';
        this.img1.src='';
        this.img2.style.display = 'none';
        this.img2.src='';}
}

var g_color=0, g_s_type='';
function create_tr_stock(url,table, info_str, s_type, sina_id) {
    if (!info_str) info_str = var_str_title;
    var sohu_id = 'cn_'+sina_id.slice(2);
    var tmp_tr = document.createElement('tr');
    table.appendChild(tmp_tr);
    if (g_s_type!=s_type){
        g_s_type = s_type;
        g_color++;
    }
    if (g_color%2==0){tmp_tr.className='stock-list-tr-group';}else{tmp_tr.className='stock-list-tr';}

    if (s_type == 'bankuai'){
       var div_type = tr_append_td(tmp_tr,bankuai_dict[s_type]);
       var img2_url='';
       if (!sina_id) {tmp_tr.style.color='blue';tmp_tr.style.textShadow='0.2px 0.5px';};
    }else{
       var div_type = insert_web_url(tmp_tr, bankuai_dict[s_type], 'http://quote.eastmoney.com/web/'+s_type+'.html','4.5em');
       var img2_url ='http://pifm3.eastmoney.com/EM_Finance2014PictureInterface/Index.aspx?UnitWidth=-6&imageType=KXL&EF=&Formula=RSI&type=&token=44c9d251add88e27b65ed86506f6e5da&r=0.0&ID='+s_type;
       if(sina_id[1]=='z'){div_type.style.textShadow='0.2px 0.5px #000';}
    }
    div_type.title = s_type+','+sina_id;

    attach_down_right_img(div_type,'http://image.sinajs.cn/newchart/png/min/new_min/n/'+sina_id+'.png',
      'http://image.sinajs.cn/newchart/daily/n/'+sina_id+'.gif',img2_url);
    
    var info_list = info_str.replace(/~~/g, "~-~").replace(/~~/g, "~-~").match(/([^~]+)/g);

    var tmp_json={};
    for (var iii=0; iii < info_list.length; iii++) {
        tmp_json[all_keys_list[iii]] = info_list[iii];
    }
    
    for (var iii=0; iii < show_keys_list.length; iii++) {
        div_tmp=tr_append_td(tmp_tr, tmp_json[show_keys_list[iii]]||show_keys_list[iii]);
        if (sina_id){
           div_tmp.onclick = function(){window.open('http://finance.sina.com.cn/realstock/company/'+sina_id+'/nc.shtml', '_blank');};
        }
    }
    var diff = parseFloat(tmp_json['涨_跌']);
    if (diff > 0)
        tmp_tr.style.color = 'red';
    else if (diff < 0)
        tmp_tr.style.color = 'green';

    if (s_type == 'bankuai') {
        if (sina_id){var title_list = ['','','','','','','','','','','',];}
        else {var title_list = ['PE','BK_PE','ROE','BK_ROE','狐研','浪研','浪评','东研','狐','QQ','浪',];}
        for (var jjj=0;jjj<title_list.length;jjj++){
            tr_append_td(tmp_tr, title_list[jjj]);
        }
        if (sina_id){tr_append_del_follow(url,tmp_tr,sina_id);}
        return;
    } else {
        tr_append_td(tmp_tr, json_dict[sina_id]['pe']||'PE');
        tr_append_td(tmp_tr, json_dict[sina_id]['bk_pe']||'BK_PE');
        insert_web_url(tmp_tr, json_dict[sina_id]['roe']||'杜邦', 'http://emweb.securities.eastmoney.com/f10_v2/FinanceAnalysis.aspx?type=web&code='+sina_id+'#dbfx-0');
        insert_web_url(tmp_tr, json_dict[sina_id]['bk_roe']||'东', 'http://quote.eastmoney.com/'+sina_id+'.html');
    }

    if (json_dict[sina_id]['follow']){tmp_tr.style.textShadow='0.2px 0.5px #000';tmp_tr.style.fontWeight='bold';}
    insert_web_url(tmp_tr, '狐研', 'http://q.stock.sohu.com/jlp/res/listresv2.up?query.secCode='+sina_id.substr(2));
    insert_web_url(tmp_tr, '浪研', 'http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/search/index.phtml?t1=all&symbol='+sina_id);
    insert_web_url(tmp_tr, '浪评', 'http://vip.stock.finance.sina.com.cn/q/go.php/vIR_StockSearch/key/'+sina_id.substr(2)+'.phtml');
    insert_web_url(tmp_tr, '东研', 'http://data.eastmoney.com/report/'+sina_id.substr(2)+'.html');
    insert_web_url(tmp_tr, '狐', 'http://q.stock.sohu.com/cn/'+sina_id.substr(2)+'/index.shtml');
    insert_web_url(tmp_tr, 'QQ', 'http://gu.qq.com/'+sina_id+'/gp');

    var div_sina = tr_append_td(tmp_tr, '浪');
    div_sina.onclick = function(){
        var tmp_window = window.open('', '_blank', "width=500,resizable=yes,scrollbars=yes");
        tmp_window.document.write('<title>'+sina_id+'</title><iframe src="http://quotes.sina.cn/hs/company/quotes/view/'+sina_id+'" width="500" height="900"></iframe>');
    };
    tr_append_del_follow(url,tmp_tr,sina_id);
}

function stock_info_from_163(url,table, stock_list, gOnlyShowFollowed) {
    var script_url = 'https://qt.gtimg.cn/q=';
    for (var iii=0; iii<stock_list.length;iii++) {
        script_url = script_url+stock_list[iii]+',';
    }
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = script_url;
    script.table = table;
    document.body.appendChild(script);
    script.onload = function () {
        while(table.hasChildNodes()) {
            table.removeChild(table.firstChild);
        }
        create_tr_stock(url,this.table, '', 'bankuai', '');
        for (var iii=0; iii<stock_list.length;iii++){
            var stock_id = stock_list[iii];
            if ((gOnlyShowFollowed == true) && (json_dict[stock_id]['bankuai'] != 'bankuai') && (json_dict[stock_id]['follow'] != 1)) {
                continue;
            }
            try{
                create_tr_stock(url,this.table, eval('v_'+stock_id), json_dict[stock_id]['bankuai'], stock_id);}
            catch(err){
                console.error(err);
                create_tr_stock(url,this.table, '', stock_id, stock_id);
            }
        }
        if (stock_list.length>1) {create_tr_stock(url,this.table, '', 'bankuai', '');}
    };
}

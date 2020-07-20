var g_table;

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
var g_key_dict = {
    "name": "name",
    "price":"price",
    "percent":"percent",
    "arrow":"arrow",
    "high":"high",
    "low":"low",
    "time":"time",
    };

function create_tr_stock(table, stock_dict, s_type, sina_id) {
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

    for (var key in g_key_dict) {
        if (key == 'percent') {
            stock_dict[key] = (stock_dict[key]*100).toFixed(2);
        } else         if (key == 'time') {
            stock_dict[key] = stock_dict[key].slice(11);
        }
        div_tmp=tr_append_td(tmp_tr, stock_dict[key]);
        if (sina_id){
           div_tmp.onclick = function(){window.open('http://finance.sina.com.cn/realstock/company/'+sina_id+'/nc.shtml', '_blank');};
        }
    }

    if (stock_dict['percent'] > 0)
        tmp_tr.style.color = 'red';
    else if (stock_dict['percent'] < 0)
        tmp_tr.style.color = 'green';

    if (s_type == 'bankuai') {
        if (sina_id){var title_list = ['','','','','','','','','',];}
        else {var title_list = ['ROE','BK_ROE','狐研','浪研','浪评','东研','狐','QQ','浪',];}
        for (var jjj=0;jjj<title_list.length;jjj++){
            tr_append_td(tmp_tr, title_list[jjj]);
        }
        return;
    } else {
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
}

function sina_id_2_163_id(stock_id) {
    if (stock_id[1] == 'h') {
        stock_id = '0'+stock_id.slice(2);
    } else if (stock_id[1] == 'z') {
        stock_id = '1'+stock_id.slice(2);
    }
    return(stock_id);
}

function _ntes_quote_callback(stocks_163_json) {
    while(g_table.hasChildNodes()) {
        g_table.removeChild(g_table.firstChild);
    }
    for (var iii=0; iii<stock_list.length;iii++){
        var sina_id = stock_list[iii];
        var stock_id = sina_id_2_163_id(sina_id);
        create_tr_stock(g_table, stocks_163_json[stock_id], json_dict[sina_id]['bankuai'], sina_id)
    }
}

function stock_info_from_163(url, table, stock_list, gOnlyShowFollowed) {
    var script_url = 'https://api.money.126.net/data/feed/';
    for (var iii=0; iii<stock_list.length;iii++) {
        var stock_id = sina_id_2_163_id(stock_list[iii]);
        script_url = script_url+stock_id+',';
    }
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = script_url;
    g_table = table;
    document.body.appendChild(script);
}

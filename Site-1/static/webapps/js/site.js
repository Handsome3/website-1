/**
 * Created by Alienware on 2017/6/30.
 */

$('.my-search-option').click(function(){
		$(this).parent().find('.my-search-option-active').attr('class','my-search-option');
		$(this).attr('class','my-search-option-active');
		search($(this));
	});

function initOption() {
    $('.my-search-option-body').each(function(){$(this).children().first().attr('class','my-search-option-active')});
}

// Search fucntions
function loadMoreDeal(){
    sconfig.end=end;
    sendRequest('loadmore');
}

function search(obj){
		var field = obj.data('field'), type = obj.data('type'), format = obj.data('format');
		if (type=="exact")
			sconfig[field]=[type, format, obj.data('value')];
		if (type=="between")
			sconfig[field]=[type, format, obj.data('min'), obj.data('max')];
		sconfig.end=0;
        sendRequest('search');
}


// Ajax functions
$(document).ajaxStart(function(){
		NProgress.start();
	});

$(document).ajaxStop(function(){
		NProgress.done();
	});

function sendRequest(type) {
	has_next= false;
    $.ajax({
			url : surl,
			data: sconfig,
			type : 'GET',
			dataType: 'JSON',
			success: function(data){
			    has_next= data.has_next;
			    end= data.end;
			    if (type == 'search')
                    $('#result').empty();
			    switch (data.type) {
                    case "useditem":
                    case "usedcar":
                    case "houserent":
                    case "sublease":for (i in data.records) {
                                        var txt = "<div class='col-sm-6 col-md-4 col-lg-3'>\
                                                            <div class='thumbnail' style='cursor: pointer;' onClick=\"window.open('/deal/" + data.records[i].id + "/detail')\" onMouseOver=\"this.style.border='1px solid black'\" onMouseOut=\"this.style.border='1px solid #ddd'\">\
                                                            <img src='" + data.records[i].img_url + "' style='width: 100%; height: 225px;'>\
                                                            <div class='caption'>\
                                                                <h4 style='color: #6f5499'>$" + data.records[i].caption + "</h4>\
                                                                <p class='col-sm-3' align='left' style='padding: 0px; color: #999' >描述:<br><br>日期:</p>\
                                                            <p class='col-sm-9' align='right'>\
                                                                " + data.records[i].title + "<br>\
                                                                " + data.records[i].post_date + "\
                                                            </p>\<div class='clearfix'></div>\
                                                            </div></div></div>";
                                        $('#result').append(txt);
                                    };
                                    break;
                    case "carpool":for (i in data.records) {
                                            var txt="<blockquote class='my-blockquote' onClick=\"window.open('/deal/" + data.records[i].id + "/detail')\">\
                                            <p>\
                                                <span style=\"color: #6f5499;\" class=\"col-sm-3\"><label>$"+ data.records[i].caption +"</label></span><span class=\"col-sm-9\">"+data.records[i].title+"</span><span class=\"clearfix\"></span>\
                                            </p> <small>发布于"+data.records[i].post_date+"<cite>Source Title</cite></small>\
                                            </blockquote>";
                                            $('#result').append(txt);
                                        };
                                    break;
                    case "mergeorder": for (i in data.records) {
                                            var txt="<blockquote class='my-blockquote' onClick=\"window.open('/deal/" + data.records[i].id + "/detail')\">\
                                            <p>\
                                                <span style=\"color: #6f5499;\" class=\"col-sm-3\"><label>"+ data.records[i].caption +"</label></span><span class=\"col-sm-9\">"+data.records[i].title+"</span><span class=\"clearfix\"></span>\
                                            </p> <small>发布于"+data.records[i].post_date+"<cite>Source Title</cite></small>\
                                            </blockquote>";
                                            $('#result').append(txt);
                                        };
                                    break;
                }
                if (has_next==false){
                    $('#loadmore').css('display', 'none');
                    $('#nomore').css('display', '');
                }
                else{
                    $('#loadmore').css('display', '');
                    $('#nomore').css('display', 'none');
                    }
                },
		});
}
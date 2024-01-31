    console.debug("loaded util_load.js");

    var data_idx = 0;
    var pollData_delay = 0;
    var keys_visible_default = " img img_lnk price ";

    //addToggleButton(  ); // util_gui-function
    function addToggleButton( data ) {
        // add toggler button - if not already existing
        for ( var k in data ) {
            key = "ctrl_"+k;
            if ( null == document.getElementById( key )) {
                newElement = document.createElement('div');
                newElement.id = key;
                newElement.classList.add("ctrlDiv");
                newElement.classList.add("button");
                newElement.setAttribute("srcId","d_" + k );
                newElement.setAttribute("onclick","ctrl_clk( event, this, 'd_" + k + "');");
                // newElement.setAttribute("onclick","changeClassCss( '.d_" + k + "', 'display', 'none', 'block');");
                newElement.innerHTML = k;
                document.getElementById("ctrl").appendChild(newElement);
                // preset ...
                if ( !keys_visible_default.includes( " " + k + " " ) ) {
                    ctrl_clk( null, newElement, "d_" + k );
                }
            }
        }
    }


    function pollData_() {
        var d = new Date();
        var datestring = ("0" + d.getDate()).slice(-2) + "-" + ("0"+(d.getMonth()+1)).slice(-2) + "-" +
                d.getFullYear() + " " + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2) +
                ":" + ("0" + d.getSeconds()).slice(-2);
        document.getElementById('liveUpdateLabel').innerHTML="liveUpdate " + datestring + " (" + data_idx + ")";
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                if (xhr.responseText.length < 10) {
                    console.debug('pollData:: "' + xhr.responseText+ '" (nothing new)');
                    pollData_delay = 5000;
                } else if ( xhr.responseText.startsWith("{") && xhr.responseText.endsWith("}")) { // expect json
                    addData( xhr.responseText);
                    // data_idx=data_idx+1; // fails if called multiple times before 1st response
                    pollData_delay = 10;
                } else if ( xhr.responseText.startsWith("[") && xhr.responseText.endsWith("]")) { // expect json
                    addDataMsg( xhr.responseText);
                    pollData_delay = 1000;
                } else {
                    console.debug('pollData:: "' + xhr.responseText+ '" (unknown content-type)');
                    pollData_delay = 5000;
                }
            }
        };
        ref= "refresh=" + (document.getElementById('refresh').checked ?  "1" : "0") ;
        qry= "qry=" + document.getElementById("lname2").value;
        xhr.open("GET", "/json?idx=" + data_idx + ".." + (data_idx+100) + "&" + qry + "&" +  ref, true);
        xhr.send();
    }

    function pollData_single() {
        var d = new Date();
        var datestring = ("0" + d.getDate()).slice(-2) + "-" + ("0"+(d.getMonth()+1)).slice(-2) + "-" +
                d.getFullYear() + " " + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2) +
                ":" + ("0" + d.getSeconds()).slice(-2);
        document.getElementById('liveUpdateLabel').innerHTML="liveUpdate " + datestring + " (" + data_idx + ")";
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                if (xhr.responseText.length < 10) {
                    console.debug('pollData:: "' + xhr.responseText+ '" (nothing new)');
                    pollData_delay = 5000;
                } else if ( xhr.responseText.startsWith("{") && xhr.responseText.endsWith("}")) { // expect json
                    addDataMsg( xhr.responseText);
                    // data_idx=data_idx+1; // fails if called multiple times before 1st response
                    pollData_delay = 10;
                } else if ( xhr.responseText.startsWith("[") && xhr.responseText.endsWith("]")) { // expect json
                    addDataMsg( xhr.responseText);
                    pollData_delay = 10;
                } else {
                    console.debug('pollData:: "' + xhr.responseText+ '" (unknown content-type)');
                    pollData_delay = 5000;
                }
            }
        };
        ref= "refresh=" + (document.getElementById('refresh').checked ?  "1" : "0") ;
        qry= "qry=" + document.getElementById("lname2").value;
        xhr.open("GET", "/json?idx=" + data_idx + "&" + qry + "&" +  ref, true);
        xhr.send();
    }


    function pollData__(){
        /*
        // pollData_delay  -1 == wait for answer ... / 0 == off / >0 query server ...    (onreadystatechange will change -1 to X )
        if (-1 == pollData_delay) { // called my self via timer - no answer so far
            setTimeout(pollData__, 500);
        } else if (0 == pollData_delay) { // disabled by user
        } else if (1 == pollData_delay) { // called by user - or on repeat
            pollData_delay= -1;
            pollData_();
            setTimeout(pollData__, 100);
        } else if ( 0 < pollData_delay) { // called my self via timer - and answer was processed ...
            // pollData_delay = 1;
            setTimeout(pollData__, pollData_delay);
        }
        */
        //pollData_delay = 50;
        pollData_();
        if (pollData_delay<5000) {
            setTimeout(pollData__, pollData_delay);
        }
    }


    function pollData() {
        // pollData_delay  -1 == wait for answer ... / 0 == off / >0 query server ...    (onreadystatechange will change -1 to X )
        if (document.getElementById('liveUpdate').checked || 0 == document.getElementById('datas').children.length ) {
            if (0 == pollData_delay) { // just enabled
                pollData_delay = 1;
                pollData__();
            }
        } else {
            pollData_delay = 0;
        }
    }


    setInterval(pollData, 5000);


    function addDataMsg( responseText ) { // id img_lnk descr price hash
        console.debug( responseText );
        var data = JSON.parse( responseText);

        if (Array.isArray(data)){
            for (let i in data) {
                addData( data[i] );
            }
        } else {
            addData( data );
        }
    }

    function addData( data ) { // id img_lnk descr price hash
        key_idx = 0 ; img_src_idx=1; img_lnk_idx=2; descr_idx=3; price_idx=4;
        var val = data;

        itm_div = '';
        data.priceVB = data.price.includes("VB") ? "VB":"";
        data.price = data.price.replace(" VB","");
        k="href";
        itm_div += '<a class="d_' + k + '" href="' + data.img_lnk + '">';
        for ( var k in data ) {
            if ( null == data[k] ) {
            } else if ( "img_lnk" == k ) {
                /* skipp */
            } else if ( "img" == k ) {
                itm_div += '<img class="d_' + k + '" src="' + data[k] + '"/>';
            } else if ( data[k] && (""+data[k]).startsWith("http") ) {
                itm_div += '<a class="d_' + k + '" href="' + data[k] + '"></a>';
            } else  {
                itm_div += '<div class="d_' + k + '">' + data[k] + '</div>';
            }
            // console.debug( k + " -> " + data[k] );
        }
        itm_div += '</a>';
        //
        var newElement = document.createElement('div');
        newElement.classList.add("d_offer");
        newElement.classList.add("sortableDiv");
        newElement.innerHTML = itm_div;
        newElement.id = data['key'];
        old = document.getElementById(newElement.id);
        if (old) {
            console.warn("uti_load::addData replace existing key (" + newElement.id + ")" );
            old.parentNode.replaceChild( newElement, old);
        }
        document.getElementById("datas").appendChild(newElement);
        // update buttons if needed
        addToggleButton( data );
        //
        data_idx = parseInt( data.idx ) + 1;

    }
